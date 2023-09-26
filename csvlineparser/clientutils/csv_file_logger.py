import gzip
import logging
import os
import sys
import time
from logging import handlers
from pathlib import Path

ROOT_LOCATION = os.path.dirname(Path(__file__).parent.parent)

logger = logging.getLogger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


# System-wide exception catch and routing it to logger
sys.excepthook = handle_exception


# https://stackoverflow.com/a/16461440/132396
class GZipRotator:
    def __call__(self, source, dest):
        os.rename(source, dest)
        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)


def init(log_file_path: str = ROOT_LOCATION + '/logs/debug.log') -> None:
    logging.Formatter.converter = time.gmtime
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s [%(filename)s:%(lineno)d]',
                                          datefmt='%Y-%m-%dT%H:%M:%S')
    console_log_handler = logging.StreamHandler(sys.stdout)
    console_log_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_log_handler)

    log_file_formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - '
                                           '%(message)s [%(filename)s:%(lineno)d]',
                                           datefmt='%Y-%m-%dT%H:%M:%S')

    full_path = os.path.abspath(log_file_path)
    directory = os.path.dirname(full_path)
    os.makedirs(directory, exist_ok=True)

    file_log_handler = handlers.TimedRotatingFileHandler(log_file_path, when='midnight',
                                                         backupCount=0, utc=True, encoding='utf8')
    file_log_handler.setFormatter(log_file_formatter)
    file_log_handler.rotator = GZipRotator()
    root_logger.addHandler(file_log_handler)

    # Config own loggers
    # logging.getLogger('csvlineparser.aware_csv_context_provider').setLevel(logging.WARNING)
    # Config 3rd-party loggers
    # logging.getLogger('paramiko').setLevel(logging.INFO)
