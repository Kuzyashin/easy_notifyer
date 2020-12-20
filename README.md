# Easy Notifyer
###Install
`pip install easy-notifyer`
###Example usage:
```python
from easy_notifyer import telegram_reporter


@telegram_reporter(
    token="123456789:QweRtyuWErtyZxcdsG",  
    chat_id=123456789  # may be list of chat_id: [123456789, 876522345]
)
def foo():
    ...
    raise OSError
```

token and chad_id can be used from environment variables:
`export EASY_NOTIFYER_TELEGRAM_TOKEN=123456789:QweRtyuWErtyZxcdsG`  
`export EASY_NOTIFYER_TELEGRAM_CHAT_ID=123456789, 876522345`
```python
from easy_notifyer import async_telegram_reporter


@async_telegram_reporter(
    exceptions=OSError,        # may be tuple of exceptions
    as_attached=True,          # to send traceback as file
    filename='bar_report.log'  # filename of attach
    header='Testing for bar',  # first line in message-report
)
async def bar():
    ...
    raise OSError
```


may be using params:  [`parse_mode`](https://core.telegram.org/bots/api#formatting-options), `disable_web_page_preview` and `disable_notification`:
```python
from easy_notifyer import telegram_reporter

@telegram_reporter(
    header='*Test request to http://example.com*', 
    disable_web_page_preview=True,  # not worked if as_attach=True
    disable_notification=True,
    parse_mode='MarkdownV2',
)
def foo():
    ...
    raise ValueError
```
