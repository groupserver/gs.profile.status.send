# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
import sys
from setuptools import setup, find_packages
from version import get_version

version = get_version()

# The argparse library was added to core in Python 2.7
core = ['setuptools',
        'blessings',
        'gs.config',  # Note: without zope-support
        'gs.form', ]
if sys.version_info > (2, 6):
    requires = core
else:
    requires = core + ['argparse']

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(
    name='gs.profile.status.send',
    version=version,
    description="Send the profile-status notifications out",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Email :: Mailing List Servers',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='groupserver, profile, notification',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='https://github.com/groupserver/gs.profile.status.send/',
    license='ZPL 2.1',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['gs', 'gs.profile', 'gs.profile.status', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={'docs': ['Sphinx'], },
    entry_points={
        'console_scripts': [
            'sendprofile = gs.profile.status.send.script:main',
            ],
        # --=mpj17=-- Entry points are the work of the devil. Some time
        # you, me and Mr Soldering Iron are going to have a little chat
        # about how to do things better.
        },
)
