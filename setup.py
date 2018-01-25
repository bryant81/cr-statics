# coding=utf-8

import os
from setuptools import setup, find_packages


__title__ = 'cr-statics'
__description__ = 'Python statics tools'
__url__ = 'https://github.com/bryant81/cr-statics'
__license__ = 'MIT'

__requires__ = ['requests >= 2.18',
                'pyecharts>=0.3.1',
                'demjson>=2.2.4'
                ]

__keywords__ = ['statics']

here = os.path.abspath(os.path.dirname(__file__))
about = {}

with open(os.path.join(here, __title__, '_version.py')) as f:
    exec(f.read(), about)

setup(
    name=__title__,
    version=about['__version__'],
    description=__description__,
    url=__url__,
    author=about['__author__'],
    license=__license__,
    packages=find_packages(exclude=('test',)),
    keywords=__keywords__,
    install_requires=__requires__,
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
