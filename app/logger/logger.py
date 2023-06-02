import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import os
import inspect

class Logger(logging.Logger):

    def __init__(self, name=None, backupCount=5, output_to_cli=True, log_level='info'):
        
        if name == None:
            self.name = Path(inspect.currentframe().f_back.f_code.co_filename).stem
        else:
            self.name = Path(name).stem

        self.log_dir = Path(__file__).parent.parent.joinpath("log").resolve()

        super().__init__(self.name)
        self.backupCount = backupCount
        self.output_to_cli = output_to_cli
        self.assert_directory()
        self.file_name = f"{self.name}.log"
        self.file_path = f"{self.log_dir}/{self.file_name}"
        self.formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.addHandler(self.file_handler())
        level_map = {
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }      
        self.level = level_map[log_level.upper()]

        if output_to_cli:
            self.addHandler(self.stream_handler())

    def file_handler(self):
        file_handler = TimedRotatingFileHandler(
            filename=self.file_path,
            when="D",
            backupCount=self.backupCount,
        )
        file_handler.setFormatter(self.formatter)
        return file_handler

    def stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)
        return stream_handler

    def assert_directory(self):
        os.makedirs(self.log_dir, exist_ok=True)
    
    def set_log_level(self):
        level_map = {
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }        
        self.level = self.level_map[self.log_level.upper()]
    
if __name__ == '__main__':
    
    logger = Logger()
    logger.info('This is a testlog')
