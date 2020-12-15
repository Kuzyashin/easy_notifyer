from itertools import chain
from setuptools import setup


EXTRAS = {
    'telegram': ['httpx'],
    'dev': ['pytest', 'pylint', 'flake8']
}


setup(
    name='easy_notifyer',
    version='0.0.1',
    description='Easy notifyer from python to your messangers',
    author='strpc',
    url='https://github.com/strpc/easy_notifyer',
    extras_require={
        'telegram': EXTRAS['telegram'],
        'dev': EXTRAS['dev'],
        'all': list(chain.from_iterable(EXTRAS.values())),
    },
)
