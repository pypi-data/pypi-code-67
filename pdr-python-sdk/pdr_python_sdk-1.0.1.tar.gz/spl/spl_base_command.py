import logging
import sys

from .spl_packet_utils import SplPacketUtils
from ..on_demand_action import OnDemandAction


class SplBaseCommand(OnDemandAction):
    def __init__(self):
        self.uri = 'http://127.0.0.1:9999'
        self.session = ''
        self.metaInfo = None
        self.isFinish = False
        self.require_fields = ['*']
        self.export_fields = []
        self.lines = []
        self.spl_args = []

    def on_request(self, argv=None, input_stream=sys.stdin.buffer, output_stream=sys.stdout.buffer):
        self.process_protocol(argv, input_stream, output_stream)

    def process_protocol(self, argv=None, input_stream=sys.stdin.buffer, output_stream=sys.stdout.buffer):
        if argv is None:
            argv = sys.argv
        logging.debug('execute script command: {}'.format(argv))
        parser = SplPacketUtils()
        try:
            self.process_protocol_info(input_stream, parser)
            self.init_env_by_getinfo()
            self.metaInfo['require_fields'] = self.config_require_fields()
            self.metaInfo['export_fields'] = self.config_export_fields()
            parser.send_packet(output_stream, self.metaInfo, [])
            self.after_getinfo()
            self.process_data(parser, argv, input_stream, output_stream)
        except Exception as error:
            logging.error("Failed to process protocol: {}".format(error))
            logging.exception(error)
            parser.send_packet(output_stream, [], [])

    def process_data(self, parser, argv=None, input_stream=sys.stdin.buffer, output_stream=sys.stdout.buffer):
        return

    def process_protocol_info(self, input_stream, parser):
        meta_length, body_length = parser.parse_head(input_stream)
        if meta_length <= 0:
            raise RuntimeError('GetInfo Protocol metaLength is invalid: {}'.format(meta_length))

        self.metaInfo = parser.parse_meta(input_stream, meta_length)

        # discard body in getinfo
        parser.parse_body(input_stream, body_length)

    def process_protocol_execute(self, input_stream, parser):
        meta_length, body_length = parser.parse_head(input_stream)
        if meta_length <= 0:
            raise RuntimeError('Execute Protocol metaLength is invalid: {}'.format(meta_length))

        execute_meta = parser.parse_meta(input_stream, meta_length)

        if execute_meta['action'] != "execute":
            raise RuntimeError('Execute Protocol action is invalid: {}'.format(execute_meta['action']))

        self.isFinish = execute_meta['finished']
        tmp = parser.parse_body(input_stream, body_length)
        if len(tmp) > 0:
            self.lines.extend(tmp)
        return execute_meta

    def after_getinfo(self):
        return

    def init_env_by_getinfo(self):
        return

    def config_require_fields(self, require_fields=None):
        if require_fields is None:
            require_fields = []
        if require_fields is None or len(require_fields) == 0:
            require_fields = ['*']
        return require_fields

    def config_export_fields(self, export_fields=None):
        if export_fields is None:
            export_fields = []
        if export_fields is None or len(export_fields) == 0:
            export_fields = ['*']
        return export_fields

    def streaming_handle(self, lines):
        return lines, True
