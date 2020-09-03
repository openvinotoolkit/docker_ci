# -*- coding: utf-8 -*-
# Copyright (C) 2019-2020 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
"""Custom logger for this framework based on logging package from standard Python library"""
import inspect
import logging
import logging.config
import pathlib
import typing

LINE_SINGLE = '-' * 79
LINE_DOUBLE = '=' * 79


def init_logger(logdir: pathlib.Path = None) -> pathlib.Path:
    """Initializing the logger"""
    if logdir is None:
        logfile = pathlib.Path(__file__).parent.parent / 'logs' / 'summary.log'
    else:
        logfile = logdir / 'summary.log'

    if not logfile.parent.exists():
        logfile.parent.mkdir()

    logger_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)-8s %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'custom': {
                '()': 'utils.logger.CustomFormatter',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'custom',
            },
            'summary': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': logfile,
                'encoding': 'utf-8',
                'formatter': 'custom',
                'mode': 'w',
            },
        },
        'loggers': {
            'project': {
                'handlers': ['summary', 'console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

    logging.config.dictConfig(logger_config)

    # need for indentation in logs
    decorate_logger(logging.Logger, getattr(logging.Logger, '_log'))

    return logfile


def decorate_logger(logger: typing.Type[logging.Logger], func: typing.Callable[..., None]):
    """Handling custom indentations in logger"""

    def my_decorator(self, level, msg, args, exc_info=None, extra=None):
        msg = ' ' * self._indent + str(msg)
        func(self, level, msg, args, exc_info, extra)

    def increase_indent(self, inc=2):
        self._indent += inc

    def decrease_indent(self, inc=2):
        self._indent -= inc

    logger._indent = 0
    logger.increase_indent = increase_indent
    logger.decrease_indent = decrease_indent
    logger._log = my_decorator
    logger_project = logging.getLogger('project')
    logger._main_handlers = logger_project.handlers[:]


def switch_to_custom(name: typing.Union[str, pathlib.Path], logdir: typing.Optional[str] = 'logs'):
    """Switching between additional loggers"""
    logger = logging.getLogger('project')

    remove_summary()
    remove_customs()

    handler: UniqueFileHandler = UniqueFileHandler(name, logdir)
    logger.addHandler(handler)


def add_summary():
    """Adding main logger"""
    logger = logging.getLogger('project')

    if hasattr(logger, '_main_handlers'):
        main_handlers = getattr(logger, '_main_handlers')
        for handler in main_handlers:
            logger.addHandler(handler)


def remove_summary():
    """Removing main logger"""
    logger = logging.getLogger('project')

    handlers = logger.handlers[:]
    for handler in handlers:
        name = getattr(handler, '_name')
        if name in ('summary', 'console'):
            logger.removeHandler(handler)


def remove_customs():
    """Removing custom logger"""
    logger = logging.getLogger('project')

    handlers = logger.handlers[:]
    for handler in handlers:
        if isinstance(handler, UniqueFileHandler):
            logger.removeHandler(handler)


def switch_to_summary():
    """Switching from custom logger to main logger"""
    remove_customs()
    add_summary()


class UniqueFileHandler(logging.FileHandler):
    """Custom file handler that supports log file creation"""

    def __init__(self, filename, dir_=None, **kwargs):
        if not dir_:
            dir_ = pathlib.Path(__file__).parent / 'logs'
        if not pathlib.Path(dir_).exists():
            pathlib.Path(dir_).mkdir()
        super().__init__(str(pathlib.Path(dir_) / filename))
        kwargs['filename'] = pathlib.Path(dir_) / filename
        kwargs['mode'] = 'w+'

        self._handler = logging.FileHandler(**kwargs)
        self._handler.setFormatter(CustomFormatter(set_time=False))
        self._handler.setLevel(logging.DEBUG)

    def __getattr__(self, n):
        """Custom attribute handler for correct attribute access redirecting"""
        if hasattr(self._handler, n):
            return getattr(self._handler, n)
        raise AttributeError


class CustomFormatter(logging.Formatter):
    """Custom wrapper for logging.Formatter"""

    def __init__(self, set_time: typing.Optional[bool] = True, fmt: typing.Optional[str] = None,
                 datefmt: typing.Optional[str] = None):
        super().__init__(fmt, datefmt)
        self.baseline = len(inspect.stack())
        self.has_time = set_time

    def format(self, record: logging.LogRecord) -> str:  # noqa ignore=A003
        record.indent = ''
        record.message = record.getMessage().split('\n')
        s = ''
        for i in record.message:
            if len(i.strip()) > 0:
                msg = ' ' * 10 + '| ' + i if len(record.message) > 1 else i
                if self.has_time:
                    format_time = f'[{self.formatTime(record, "%Y-%m-%d %H:%M:%S")}]'
                    level = record.levelname.ljust(8)
                else:
                    format_time = ''
                    level = ''
                s += f'{format_time} {level} {record.indent} {msg}\n'
        s = s[:-1]
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                exc_text = self.formatException(record.exc_info)
                record.exc_text = self.format_exception_better(exc_text)
        if record.exc_text:
            if s[-1:] != '\n':
                s += '\n'
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != '\n':
                s += '\n'
            s = s + self.formatStack(record.stack_info)

        return s

    @staticmethod
    def format_exception_better(text: str) -> str:
        """Custom exception output formatter"""
        t = text.split('\n')
        s = ''
        for i in t:
            s += ' ' * 10 + f'| {i}\n'
        return s[:-1]
