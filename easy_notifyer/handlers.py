import functools
import traceback
from datetime import datetime
from typing import List, Optional, Tuple, Type, Union

from easy_notifyer.env import Env
from easy_notifyer.report import Report
from easy_notifyer.telegram import Telegram, TelegramAsync
from easy_notifyer.utils import run_sync


def telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[List[int], int]] = None,
        exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException], ...]]] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
        **params
):
    """
    Handler errors for sending report in telegram.
    Args:
        token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be use from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        exceptions(exception, tuple(exception), optional): Exceptions for handle. Two and more - in
        tuple. Default - Exception.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for sending as a file. Default - False.
        **params:
            filename(str, optional): filename for sending report as file.
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    exceptions = exceptions or Exception

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                func_name = func.__name__
                tback = traceback.format_exc()
                report = _report_maker(
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                _report_handler(report=report, token=token, chat_id=chat_id, **params)
                raise exc
        return wrapper
    return decorator


def async_telegram_reporter(
        *,
        token: Optional[str] = None,
        chat_id: Optional[Union[List[int], int]] = None,
        exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException], ...]]] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
        **params
):
    """
    Async handler errors for sending report in telegram.
    Args:
        token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be use from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        exceptions(exception, tuple(exception), optional): Exceptions for handle. Two and more - in
        tuple. Default - Exception.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for sending as a file. Default - False.
        **params:
            filename(str, optional): filename for sending report as file.
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    exceptions = exceptions or Exception

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as exc:
                func_name = func.__name__
                tback = traceback.format_exc()
                report = await run_sync(
                    _report_maker,
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                await _async_report_handler(report=report, token=token, chat_id=chat_id, **params)
                raise exc
        return wrapper
    return decorator


def _get_filename(filename: Optional[str] = None) -> str:
    """
    Generate of filename for sending report as a file.
    Args:
        filename(str, optional): filename, if exists. Else - "{datetime}.txt". Format of datetime
        can be set in environment variable `EASY_NOTIFYER_FILENAME_DT_FORMAT`.
        Default - "%Y-%m-%d %H_%M_%S"
    Returns:
        string of filename.
    """
    if filename is None:
        date = datetime.now().replace(microsecond=0).strftime(
            Env.EASY_NOTIFYER_FILENAME_DT_FORMAT
        )
        filename = f"{date}.txt"
    return filename


def _report_maker(
        *,
        tback: str,
        func_name: Optional[str] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
) -> Report:
    """
    Make report from
    Args:
        tback(str): traceback for report.
        func_name(str, optional): name of function when raised error.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for sending as a file. Default - False.

    Returns:
        isinstance of Report obj.
    """
    return Report(tback, func_name, header, as_attached)


def _report_handler(
        *,
        report: Report,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, List[int]]] = None,
        **kwargs
):
    """
    Send report.
    Args:
        report(Report): instance of ready to send report.
        token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be use from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        **kwargs:
            filename(str, optional): make report for sending as a file.
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    bot = Telegram(token=token, chat_id=chat_id)
    if report.attach is not None:
        filename = _get_filename(kwargs.pop('filename', None))
        bot.send_attach(msg=report.report, attach=report.attach, filename=filename, **kwargs)
    else:
        bot.send_message(report.report, **kwargs)


async def _async_report_handler(
        *,
        report: Report,
        token: Optional[str] = None,
        chat_id: Optional[Union[int, List[int]]] = None,
        **kwargs
):
    """
    Send report.
    Args:
        report(Report): instance of ready to send report.
        token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be use from environment
        variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        **kwargs:
            filename(str, optional): filename for sending report as file.
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    bot = TelegramAsync(token=token, chat_id=chat_id)
    if report.attach is not None:
        filename = await run_sync(_get_filename, kwargs.pop('filename', None))
        await bot.send_attach(msg=report.report, attach=report.attach, filename=filename, **kwargs)
    else:
        await bot.send_message(report.report, **kwargs)
