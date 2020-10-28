
import argparse
import sys
import traceback
from typing import List

HELP_MSG = '''
surfing <command> [<args>]

The most commonly used commands are:
    init_raw                setup raw database
    init_basic              setup basic database
    init_derived            setup derived database
    init_view               setup view database
    download_raw            download raw data
    update_basic            update basic data base on raw data
    update_derived          update derived data based on basic and raw data
    update_view             update view data based on basic and derived data
    data_update             run download_raw, update_basic, update_derived and update_view in turn
    check_fund_list         check fund list to get new funds and delisted funds
    dump_tables_and_dfs     dump all tables and dfs of fund dm to s3
'''


class SurfingEntrance(object):
    # TODO: rename to Surfing and move parser out of __init__
    # Make this class usable in other scripts

    def __init__(self):
        parser = argparse.ArgumentParser(description='Fund Command Tool', usage=HELP_MSG)
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def _get_yesterday(self):
        import datetime
        yesterday = datetime.datetime.today() - datetime.timedelta(days = 1)
        yesterday_str = datetime.datetime.strftime(yesterday, '%Y%m%d')
        print(f'yesterday: {yesterday_str}')
        return yesterday_str

    def datetime_test(self):
        import datetime
        print(datetime.datetime.today())

    def init_raw(self):
        from .data.wrapper.mysql import RawDatabaseConnector
        from .data.view.raw_models import Base

        print('Begin to create tables for database: raw')
        Base.metadata.create_all(bind=RawDatabaseConnector().get_engine())
        print('done')

    def init_basic(self):
        from .data.wrapper.mysql import BasicDatabaseConnector
        from .data.view.basic_models import Base

        print('Begin to create tables for database: basic')
        Base.metadata.create_all(bind=BasicDatabaseConnector().get_engine())
        print('done')

    def init_derived(self):
        from .data.wrapper.mysql import DerivedDatabaseConnector
        from .data.view.derived_models import Base

        print('Begin to create tables for database: derived')
        Base.metadata.create_all(bind=DerivedDatabaseConnector().get_engine())
        print('done')

    def init_view(self):
        from .data.wrapper.mysql import ViewDatabaseConnector
        from .data.view.view_models import Base

        print('Begin to create tables for database: view')
        Base.metadata.create_all(bind=ViewDatabaseConnector().get_engine())
        print('done')

    def init_cas(self):
        from .data.wrapper.cas.cas_init import sync_cas_table

        print('Begin to create table for database: cas')
        sync_cas_table()
        print('done')

    def download_raw(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()

        from .data.fund.raw.raw_data_downloader import RawDataDownloader
        from .util.config import SurfingConfigurator

        rq_license = SurfingConfigurator().get_license_settings('rq')
        raw_data_downloader = RawDataDownloader(rq_license)
        return raw_data_downloader.download(yesterday, yesterday), raw_data_downloader.get_updated_count()

    def update_basic(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()

        from .data.fund.basic.basic_data_processor import BasicDataProcessor

        basic_data_processor = BasicDataProcessor()
        return basic_data_processor.process_all(yesterday, yesterday), basic_data_processor.get_updated_count()

    def update_derived(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()

        from .data.fund.derived.derived_data_processor import DerivedDataProcessor
        derived_data_processor = DerivedDataProcessor()
        return derived_data_processor.process_all(yesterday, yesterday), derived_data_processor.get_updated_count()

    def update_view(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()

        from .data.fund.view.view_data_processor import ViewDataProcessor
        return ViewDataProcessor().process_all(yesterday, yesterday)

    def data_update(self):
        print('Start data update')

        yesterday = self._get_yesterday()

        failed_tasks = {}
        updated_count = {}

        print('Step 1. Start raw data download')
        raw_failed_tasks, raw_updated_count = self.download_raw(yesterday)
        if 'em_tradedates' in raw_failed_tasks:
            print('Step 1. No raw data to download')
            print(f'Done data update, {yesterday} is not trading day')
            return
        if len(raw_failed_tasks) > 0:
            failed_tasks['raw'] = raw_failed_tasks
        updated_count['raw'] = raw_updated_count
        print('Step 1. Done raw data download')

        print('Step 2. Start update basic')
        basic_failed_tasks, basic_updated_count = self.update_basic(yesterday)
        if len(basic_failed_tasks) > 0:
            failed_tasks['basic'] = basic_failed_tasks
        updated_count['basic'] = basic_updated_count
        print('Step 2. Done update basic')

        print('Step 3. Start update derived')
        derived_failed_tasks, derived_updated_count = self.update_derived(yesterday)
        if len(derived_failed_tasks) > 0:
            failed_tasks['derived'] = derived_failed_tasks
        updated_count['derived'] = derived_updated_count
        print('Step 3. Done update derived')

        print('Step 4. Start update view')
        view_failed_tasks = self.update_view(yesterday)
        if len(view_failed_tasks) > 0:
            failed_tasks['view'] = view_failed_tasks
        print('Step 4. Done update view')

        print('Done data update')
        print(f'Failed tasks:\n{failed_tasks}')
        print(f'Updated count:\n{updated_count}')

        from .util.wechat_bot import WechatBot
        wechat_bot = WechatBot()
        wechat_bot.send_data_update_status(yesterday, failed_tasks, updated_count)

        self.check_fund_list(yesterday, wechat_bot)
        self.dump_tables_and_dfs(yesterday, wechat_bot)

    def calc_fund_estimated_nav(self):
        # Use Jenkins to call this function every hour
        import time
        import datetime
        from .util.config import SurfingConfigurator
        from .data.fund.raw.raw_data_helper import RawDataHelper
        from .data.fund.basic.fund_estimated_nav_processor import FundEstimatedNavProcessor

        USE_SINA_DATA = True
        
        fund_estimated_nav_processor = FundEstimatedNavProcessor()
        if not fund_estimated_nav_processor.init():
            return

        if USE_SINA_DATA:
            from .data.fund.raw.sina_stock_downloader import SinaStockDownloader
            sina = SinaStockDownloader(RawDataHelper(), fund_estimated_nav_processor.stock_list)
        else:
            from .data.fund.raw.rq_raw_data_downloader import RqRawDataDownloader
            rq_license = SurfingConfigurator().get_license_settings('rq')
            rq_raw_data_downloader = RqRawDataDownloader(rq_license, RawDataHelper())

        last_time_start = None
        while True:
            try:
                time_start = datetime.datetime.now()
                # # For test only
                # if not last_time_start:
                #     time_start = datetime.datetime.fromisoformat('2020-08-06T14:59:01')

                time_start_second = time_start.second
                time_start_str = time_start.strftime('%Y-%m-%d %H:%M')
                time_start = datetime.datetime.strptime(time_start_str, '%Y-%m-%d %H:%M')
                
                if time_start.hour < 9 or time_start.hour == 12 or time_start.hour > 15:
                    # Exit when time_start is in range [0:00, 8:59], [12:00, 12:59] and [16:00 23:59]
                    print(f'Current time {time_start} is not trading time. Will exit.')
                    return
                elif (time_start.hour == 11 and time_start.minute >= 31) or (time_start.hour == 15 and time_start.minute >= 1):
                    # Exit when time_start is in range [11:31, 11:59] and [15:01, 15:59]
                    print(f'Current time {time_start} is not trading time. Will exit.')
                    return
                elif time_start.hour == 9 and time_start.minute < 30:
                    # At 9:00, clear fund_estimated_nav calcculated at yesterday in Cassandra
                    if time_start.minute == 29:
                        from .data.view.cas.fund_estimated_nav import FundEstimatedNav
                        from .data.wrapper.cas.cas_base import CasClient
                        CasClient().truncate_table(model=FundEstimatedNav)
                        print(f'Truncated Cassandra table {FundEstimatedNav.__table_name__}')
                    # Sleep when time_start is in range [9:00, 9:29]
                    time.sleep(max(59 - time_start_second, 1))
                elif time_start.hour == 13 and time_start.minute == 0:
                    time.sleep(max(59 - time_start_second, 1))
                elif not last_time_start or time_start.minute > last_time_start.minute or (time_start - last_time_start).seconds >= 60:
                    last_time_start = time_start
                    to_save = not (time_start.hour == 9 and time_start.minute == 30)
                    if USE_SINA_DATA:
                        stock_minute_df = sina.sina_stock_minute(to_save)
                    else:
                        stock_minute_df = rq_raw_data_downloader.stock_minute(to_save)
                    if stock_minute_df is None or stock_minute_df.empty:
                        print(f'Failed to get stock_minute_df at {time_start}')
                        continue
                    fund_estimated_nav_processor.calc_fund_estimated_nav(stock_minute_df, time_start, USE_SINA_DATA)
                    time_end = datetime.datetime.now()
                    print(f'Time for calc_fund_estimated_nav is {(time_end - time_start).total_seconds()} seconds at {time_start}')
                    if time_start.minute == 59:
                        # Exit at the end of each hour
                        return
                else:
                    time.sleep(max(59 - time_start_second, 1))
            except Exception as e:
                print(e)
                traceback.print_exc()
                return False

    def calc_index_price(self):
        # Use Jenkins to call this function every hour
        import time
        import datetime
        from .util.config import SurfingConfigurator
        from .data.fund.raw.raw_data_helper import RawDataHelper
        from .data.fund.raw.em_raw_data_downloader import EmRawDataDownloader
        from .data.fund.basic.realtime_index_price_processor import RealtimeIndexPriceProcessor
        
        realtime_index_price_processor = RealtimeIndexPriceProcessor()
        if not realtime_index_price_processor.init():
            return

        em = EmRawDataDownloader(RawDataHelper())

        last_time_start = None
        while True:
            try:
                time_start = datetime.datetime.now()
                # # For test only
                # if not last_time_start:
                #     time_start = datetime.datetime.fromisoformat('2020-08-06T14:59:01')

                time_start_second = time_start.second
                time_start_str = time_start.strftime('%Y-%m-%d %H:%M')
                time_start = datetime.datetime.strptime(time_start_str, '%Y-%m-%d %H:%M')
                
                if time_start.hour < 9 or time_start.hour == 12 or time_start.hour > 15:
                    # Exit when time_start is in range [0:00, 8:59], [12:00, 12:59] and [16:00 23:59]
                    print(f'Current time {time_start} is not trading time. Will exit.')
                    return
                elif (time_start.hour == 11 and time_start.minute >= 31) or (time_start.hour == 15 and time_start.minute >= 1):
                    # Exit when time_start is in range [11:31, 11:59] and [15:01, 15:59]
                    print(f'Current time {time_start} is not trading time. Will exit.')
                    return
                elif time_start.hour == 9 and time_start.minute < 30:
                    # At 9:00, clear fund_estimated_nav calcculated at yesterday in Cassandra
                    if time_start.minute == 29:
                        from .data.view.cas.realtime_index_price import RealtimeIndexPrice
                        from .data.view.cas.realtime_index_price_snapshot import RealtimeIndexPriceSnapshot
                        from .data.wrapper.cas.cas_base import CasClient
                        CasClient().truncate_table(model=RealtimeIndexPrice)
                        CasClient().truncate_table(model=RealtimeIndexPriceSnapshot)
                        print(f'Truncated Cassandra table {RealtimeIndexPrice.__table_name__}')
                    # Sleep when time_start is in range [9:00, 9:29]
                    time.sleep(max(59 - time_start_second, 1))
                elif time_start.hour == 13 and time_start.minute == 0:
                    time.sleep(max(59 - time_start_second, 1))
                elif not last_time_start or time_start.minute > last_time_start.minute or (time_start - last_time_start).seconds >= 60:
                    data_start_time = last_time_start
                    if not data_start_time:
                        data_start_time = time_start - datetime.timedelta(seconds = 60)
                    last_time_start = time_start
                    to_save = not (time_start.hour == 9 and time_start.minute == 30)
                    realtime_index_price_df = em.em_realtime_index(realtime_index_price_processor.index_ids, data_start_time, to_save)
                    if realtime_index_price_df is None or realtime_index_price_df.empty:
                        print(f'Failed to get realtime_index_price_df at {time_start}')
                        continue
                    realtime_index_price_processor.calc_realtime_index_price(realtime_index_price_df, time_start)
                    time_end = datetime.datetime.now()
                    print(f'Time for calc_realtime_index_price is {(time_end - time_start).total_seconds()} seconds at {time_start}')
                    if time_start.minute == 59:
                        # Exit at the end of each hour
                        return
                else:
                    time.sleep(max(59 - time_start_second, 1))
            except Exception as e:
                print(e)
                traceback.print_exc()
                return False

    def check_fund_list(self, yesterday=None, wechat_bot=None):
        from .data.fund.raw.raw_data_helper import RawDataHelper
        from .data.api.raw import RawDataApi

        if yesterday is None:
            yesterday = self._get_yesterday()
        if wechat_bot is None:
            from .util.wechat_bot import WechatBot
            wechat_bot = WechatBot()
        new_funds_with_name = {}
        new_delisted_funds_with_name = {}
        new_funds, new_delisted_funds = RawDataHelper.get_new_and_delisted_fund_list(yesterday)
        if new_funds is not None and new_delisted_funds is not None:
            # 获取新增基金以及新摘牌基金列表
            agg_funds = new_funds.union(new_delisted_funds)
            if agg_funds:
                # 不是OF结尾的我们把它换成OF也去查一下
                agg_funds.update({one.split('.')[0] + '.OF' for one in agg_funds if not one.endswith('.OF')})

                api = RawDataApi()
                # 在已有的fund_info里找对应基金的信息
                wind_df = api.get_wind_fund_info(agg_funds)
                fund_name_got = {row.wind_id: row.desc_name for row in wind_df.itertuples(index=False)}
                # 在Choice的fund_info里找剩余还没找到的基金信息
                em_df = api.get_em_fund_info(agg_funds.difference(set(fund_name_got.keys())))
                fund_name_got.update({row.em_id: row.name for row in em_df.itertuples(index=False)})

                # 拆回到原来的两个列表里
                for fund_id in sorted(new_funds):
                    try:
                        new_funds_with_name[fund_id] = fund_name_got[fund_id]
                    except KeyError:
                        # 把结尾换成.OF再查一下
                        new_funds_with_name[fund_id] = fund_name_got.get(fund_id.split('.')[0] + '.OF', None)
                        if new_funds_with_name[fund_id] is not None:
                            new_funds_with_name[fund_id] += '(场内)'

                for fund_id in sorted(new_delisted_funds):
                    try:
                        new_delisted_funds_with_name[fund_id] = fund_name_got[fund_id]
                    except KeyError:
                        # 把结尾换成.OF再查一下
                        new_delisted_funds_with_name[fund_id] = fund_name_got.get(fund_id.split('.')[0] + '.OF', None)
                        if new_delisted_funds_with_name[fund_id] is not None:
                            new_delisted_funds_with_name[fund_id] += '(场内)'
        wechat_bot.send_new_fund_list(yesterday, new_funds_with_name, new_delisted_funds_with_name, RawDataHelper.get_indexes_that_become_invalid(yesterday))

    def dump_tables_and_dfs(self, yesterday=None, wechat_bot=None):
        from .data.manager.etl_tool import SynchronizerS3ForDM
        from .data.manager.manager_fund import FundDataManager

        print('to dump tables and dfs to s3')
        # 构建一个默认的DM
        try:
            fdm = FundDataManager()
            fdm.init(score_pre_calc=True, print_time=True, use_weekly_monthly_indicators=False, block_df_list=[])
        except Exception as e:
            print(f'init dm failed (err_msg){e}')

        if fdm.inited:
            # 默认DM初始化成功，用它的数据向S3同步所有df
            syncer = SynchronizerS3ForDM(dm=fdm)
            failed_dfs: List[str] = syncer.dump_all_dfs()
        else:
            print('init dm failed, dump tables only')
            syncer = SynchronizerS3ForDM()
            failed_dfs: List[str] = ['init dm']
        # 向S3同步所有table
        failed_tables: List[str] = syncer.dump_all_tables()

        # 发送同步结果
        if yesterday is None:
            yesterday = self._get_yesterday()
        if wechat_bot is None:
            from .util.wechat_bot import WechatBot
            wechat_bot = WechatBot()
        wechat_bot.send_dump_to_s3_result(yesterday, failed_tables, failed_dfs)


if __name__ == "__main__":
    entrance = SurfingEntrance()
