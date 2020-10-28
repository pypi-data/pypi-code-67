# https://github.com/django/asgiref/issues/179
from asgiref.sync import SyncToAsync

old_init = SyncToAsync.__init__


def _thread_sensitive_init(self, func, thread_sensitive=True):
    return old_init(self, func, thread_sensitive=True)


SyncToAsync.__init__ = _thread_sensitive_init

import json
import logging
import django.core.management
import django.conf
import os
import sys
from sys import argv
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Optional

# avoid confusion with otree_startup.settings
from django.conf import settings as django_settings
from importlib import import_module
from django.core.management import get_commands, load_command_class
import django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import autoreload

# "from .settings import ..." actually imports the whole settings module
# confused me, it was overwriting django.conf.settings above
# https://docs.python.org/3/reference/import.html#submodules
from otree_startup.settings import augment_settings
from otree import __version__
from . import zipserver

# REMEMBER TO ALSO UPDATE THE PROJECT TEMPLATE
from otree_startup.settings import get_default_settings

logger = logging.getLogger(__name__)


MAIN_HELP_TEXT = '''
Type 'otree help <subcommand>' for help on a specific subcommand.

Available subcommands:

browser_bots
create_session
devserver
django_test
resetdb
prodserver
prodserver1of2
prodserver2of2
shell
startapp
startproject
test
unzip
zip
zipserver
'''


def execute_from_command_line(*args, **kwargs):
    '''
    Top-level entry point.

    - figures out which subcommand is being run
    - sets up django & configures settings
    - runs the subcommand

    We have to ignore the args to this function.
    If the user runs "python manage.py [subcommand]",
    then argv is indeed passed, but if they run "otree [subcommand]",
    it executes the autogenerated console_scripts shim,
    which does not pass any args to this function,
    just:

    load_entry_point('otree', 'console_scripts', 'otree')()

    This is called if people use manage.py,
    or if people use the otree script.
    script_file is no longer used, but we need it for compat

    '''

    if len(argv) == 1:
        # default command
        argv.append('help')

    subcommand = argv[1]

    if subcommand in ['runzip', 'zipserver']:
        zipserver.main(argv[2:])
        # better to return than sys.exit because testing is complicated
        # with sys.exit -- if you mock it, then the function keeps executing.
        return

    # Add the current directory to sys.path so that Python can find
    # the settings module.
    # when using "python manage.py" this is not necessary because
    # the entry-point script's dir is automatically added to sys.path.
    # but the 'otree' command script is located outside of the project
    # directory.
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    # to match manage.py:
    # make it configurable so i can test it.
    # and it must be an env var, because
    # note: we will never get ImproperlyConfigured,
    # because that only happens when DJANGO_SETTINGS_MODULE is not set
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    DJANGO_SETTINGS_MODULE = os.environ['DJANGO_SETTINGS_MODULE']

    if subcommand in ['help', '--help', '-h'] and len(argv) == 2:
        sys.stdout.write(MAIN_HELP_TEXT)
        return

    # this env var is necessary because if the botworker submits a wait page,
    # it needs to broadcast to redis channel layer, not in-memory.
    # this caused an obscure bug on 2019-09-21.
    # prodserver1of2, 2of2, etc
    # we now require REDIS_URL to be defined even if using default localhost:6379
    # that is to avoid piling up stuff in redis if it's not being used.
    if (
        'prodserver' in subcommand
        or 'webandworkers' in subcommand
        or 'timeoutworker' in subcommand
    ) and os.environ.get('REDIS_URL'):
        os.environ['OTREE_USE_REDIS'] = '1'

    if subcommand in [
        'startproject',
        'version',
        '--version',
        'compilemessages',
        'makemessages',
        'unzip',
        'zip',
    ]:
        django_settings.configure(**get_default_settings({}))
    else:
        try:
            configure_settings(DJANGO_SETTINGS_MODULE)
        except ModuleNotFoundError as exc:
            if exc.name == DJANGO_SETTINGS_MODULE.split('.')[-1]:
                msg = (
                    "Cannot find oTree settings. "
                    "Please 'cd' to your oTree project folder, "
                    "which contains a settings.py file."
                )
                logger.warning(msg)
                return
            raise
        warning = check_update_needed(
            Path('.').resolve().joinpath('requirements_base.txt')
        )
        if warning:
            logger.warning(warning)

    is_devserver = subcommand == 'devserver'

    if is_devserver:
        # apparently required by restart_with_reloader
        # otherwise, i get:
        # python.exe: can't open file 'C:\oTree\venv\Scripts\otree':
        # [Errno 2] No such file or directory

        # this doesn't work if you start runserver from another dir
        # like python my_project/manage.py runserver. but that doesn't seem
        # high-priority now.
        sys.argv = ['manage.py'] + argv[1:]

        # previous solution here was using subprocess.Popen,
        # but changing it to modifying sys.argv changed average
        # startup time on my machine from 2.7s to 2.3s.

    # Start the auto-reloading dev server even if the code is broken.
    # The hardcoded condition is a code smell but we can't rely on a
    # flag on the command class because we haven't located it yet.

    if is_devserver and '--noreload' not in argv:
        try:
            autoreload.check_errors(do_django_setup)()
        except Exception:
            # The exception will be raised later in the child process
            # started by the autoreloader. Pretend it didn't happen by
            # loading an empty list of applications.
            apps.all_models = defaultdict(OrderedDict)
            apps.app_configs = OrderedDict()
            apps.apps_ready = apps.models_ready = apps.ready = True
    else:
        do_django_setup()

    if subcommand == 'help' and len(argv) >= 3:
        command_to_explain = argv[2]
        fetch_command(command_to_explain).print_help('otree', command_to_explain)
    elif subcommand in ("version", "--version"):
        sys.stdout.write(__version__ + '\n')
    else:
        fetch_command(subcommand).run_from_argv(argv)


def configure_settings(DJANGO_SETTINGS_MODULE: str = 'settings'):
    user_settings_module = import_module(DJANGO_SETTINGS_MODULE)
    user_settings_dict = {}
    user_settings_dict['BASE_DIR'] = os.path.dirname(
        os.path.abspath(user_settings_module.__file__)
    )
    # this is how Django reads settings from a settings module
    for setting_name in dir(user_settings_module):
        if setting_name.isupper():
            setting_value = getattr(user_settings_module, setting_name)
            user_settings_dict[setting_name] = setting_value
    augment_settings(user_settings_dict)
    django_settings.configure(**user_settings_dict)


def do_django_setup():
    try:
        django.setup()
    except Exception as exc:
        # it would be nice to catch ModuleNotFoundError but need a good way
        # to differentiate between the app being in SESSION_CONFIGS vs
        # EXTENSION_APPS vs a regular import statement.
        import colorama

        colorama.init(autoreset=True)
        print_colored_traceback_and_exit(exc)


def fetch_command(subcommand: str) -> BaseCommand:
    """
    Tries to fetch the given subcommand, printing a message with the
    appropriate command called from the command line (usually
    "django-admin" or "manage.py") if it can't be found.
    override a few django commands in the case where settings not loaded.
    hard to test this because we need to simulate settings not being
    configured
    """
    if subcommand in ['startapp', 'startproject', 'unzip', 'zip']:
        command_module = import_module(
            'otree.management.commands.{}'.format(subcommand)
        )
        return command_module.Command()

    commands = get_commands()
    try:
        app_name = commands[subcommand]
    except KeyError:
        sys.stderr.write(
            "Unknown command: %r\nType 'otree help' for usage.\n" % subcommand
        )
        sys.exit(1)
    if isinstance(app_name, BaseCommand):
        # If the command is already loaded, use it directly.
        klass = app_name
    else:
        klass = load_command_class(app_name, subcommand)
    return klass


def check_update_needed(requirements_path: Path) -> Optional[str]:
    try:
        import pkg_resources as pkg
    except ModuleNotFoundError:
        return
    try:
        # ignore all weird things like "-r foo.txt"
        req_lines = [
            r
            for r in requirements_path.read_text('utf8').split('\n')
            if r.strip().startswith('otree')
        ]
    except FileNotFoundError:
        return
    reqs = pkg.parse_requirements(req_lines)
    for req in reqs:
        if req.project_name == 'otree':
            try:
                pkg.require(str(req))
            except pkg.DistributionNotFound:
                # if you require otree[mturk], then the mturk packages
                # will be missing and you get:
                # The 's3transfer==0.1.10' distribution was not found and is required by otree
                # which is very confusing.
                # all we care about is otree.
                pass
            except pkg.VersionConflict as exc:
                # can't say to install requirements_base.txt because if they are using zipserver,
                # that file doesn't exist.
                # used to tell people to install exc.req, but then they got:
                # ... Enter: pip3 install "botocore==1.12.235; extra == "mturk""
                return f'{exc.report()}. Enter: pip3 install "{req}"'


def highlight(string):
    from termcolor import colored

    return colored(string, 'white', 'on_blue')


def print_colored_traceback_and_exit(exc):
    import traceback
    import sys

    # before we used BASE_DIR but apparently that setting was not set yet
    # (not sure why)
    # so use os.getcwd() instead.
    # also, with BASE_DIR, I got "unknown command: devserver", as if
    # the list of commands was not loaded.
    current_dir = os.getcwd()

    frames = traceback.extract_tb(exc.__traceback__)
    new_frames = []
    for frame in frames:
        filename, lineno, name, line = frame
        if current_dir in filename:
            filename = highlight(filename)
            line = highlight(line)
        new_frames.append([filename, lineno, name, line])
    # taken from django source?
    lines = ['Traceback (most recent call last):\n']
    lines += traceback.format_list(new_frames)
    final_lines = traceback.format_exception_only(type(exc), exc)
    # filename is only available for SyntaxError
    if isinstance(exc, SyntaxError) and current_dir in exc.filename:
        final_lines = [highlight(line) for line in final_lines]
    lines += final_lines
    for line in lines:
        sys.stdout.write(line)

    sys.exit(-1)
