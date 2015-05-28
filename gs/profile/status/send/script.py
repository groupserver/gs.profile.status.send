# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
# Standard libraries
from __future__ import (absolute_import, unicode_literals, print_function,
                        division)
from argparse import ArgumentParser  # Standard in Python 2.7
from httplib import OK as HTTP_OK
from json import loads as load_json
import sys
from textwrap import fill
from time import sleep
from urlparse import urlparse
# Extra libraries
from blessings import Terminal
# GroupServer libraries
from gs.config.config import Config, ConfigError
from gs.form import post_multipart
# Local libraries
from .errorvals import exit_vals


class NotOk(Exception):
    '''Raised when a web-hook does not return a 200 status code'''


def get_args(configFileName):
    p = ArgumentParser(
        description='Send the profile-status notification from '
                    'GroupServer.',
        epilog='Usually %(prog)s is called by cron(8) at the start of the '
               'month.')
    p.add_argument('url', metavar='url',
                   help='The URL for the GroupServer site.')
    p.add_argument(
        '-c', '--config', dest='config', default=configFileName, type=str,
        help='The name of the GroupServer configuration file (default '
             '"%(default)s") that contains the token that will be used to '
             'authenticate the script when it tries to send the '
             'notifications.')
    p.add_argument(
        '-i', '--instance', dest='instance', default='default', type=str,
        help='The identifier of the GroupServer instance configuration to '
             'use (default "%(default)s").')
    p.add_argument(
        '-t', '--throttle', dest='throttle', default=0, type=int,
        help='The time (in seconds) to pause when the notifications is successfully sent '
             '(default "%(default)s").')
    p.add_argument(
        '-v', '--verbose', dest='verbose', default=False,
        action='store_true',
        help='Turn on verbose output (feedback). Default %(default)s.')
    retval = p.parse_args()
    return retval


def get_token_from_config(configSet, configFileName):
    config = Config(configSet, configFileName)
    config.set_schema('webservice', {'token': str})
    ws = config.get('webservice')
    retval = ws['token']
    if not retval:
        m = 'The token was not set.'
        raise ValueError(m)
    return retval

#: The URL of the web-hook that returns (as a JSON blob) the list of
#: profile IDs
PROFILE_URI = '/gs-profile-status-members.html'


def get_userIds(hostname, token):
    '''Get the list of profiles to send the notification to.

:param str hostname: The name of the host to use.
:param str token: The token to use for authentication.
:raises NotOk: When the page does not return an HTTP 200 status code.
:returns: A list of strings
:rtype: list'''
    fields = {'token': token, 'get': '', }
    status, reason, data = post_multipart(hostname, PROFILE_URI,
                                          fields)  # port?
    if status != HTTP_OK:
        m = '{reason} ({status} <{host}>)'
        msg = m.format(reason=reason, status=status, host=hostname)
        raise NotOk(msg)

    retval = load_json(data)
    return retval


#: The URL of the web-hook used to send a digest to a group
SEND_STATUS_URI = '/gs-profile-status-send.html'


def send_status(hostname, userId, token):
    '''Send a profile-status notification for a particular person

:param str hostname: The name of the host to use.
:param str userId: The identifier for the person.
:param str token: The token to use for authentication.
:raises NotOk: When the page does not return an HTTP 200 status code.'''
    fields = {
        'profileId': userId,
        'token': token,
        'send': 'Send'}
    status, reason, data = post_multipart(hostname, SEND_STATUS_URI,
                                          fields)  # port?
    if status != HTTP_OK:
        m = '{reason} ({status} <{host}>)'
        msg = m.format(reason=reason, status=status, host=hostname)
        raise NotOk(msg)
    retval = load_json(data)
    return retval


def show_progress(profileId, curr, total):
    '''Show the progress for sending the profile

:param str profileId: The identifier for the profile.
:param int curr: The current index of the person.
:param int total: The total number of people.

:func:`show_progress` displays the *verbose* feedback. A progress bar is
also displayed if the terminal supports it.'''
    t = Terminal()
    # Write the site and group
    m = 'Sending status ({0})...\n'
    sys.stdout.write(t.white(m.format(profileId)))
    # Display the progress bar
    if t.does_styling:
        # Length of the bar = (width of term - the two brackets) * progress
        p = int(((t.width - 2) * (curr / total)))
        bar = '=' * (p + 1)  # +1 because Python is 0-indexed
        # Space at end = terminal width - bar width - brackets - 1
        # (0-indexed)
        space = ' ' * (t.width - p - 3)
        sys.stdout.write(t.bold('[' + bar + space + ']\n'))
    sys.stdout.flush()


def show_done(r):
    '''Show feedback when the notification is sent

:param dict r: The response from the server'''
    t = Terminal()
    # Write the site and group
    if t.does_styling:
        # Clear the line above (the progress bar)
        sys.stdout.write(t.move_up + t.move_x(0) + t.clear_eol)

        responseColours = {0: t.green, -2: t.red, }
        done = responseColours.get(r['status'], t.yellow)('    Done: ')
        m = t.white(fill(r['message'], t.width-10, subsequent_indent=' '*10))
    else:
        done = b'    Done: '
        m = r['message'].encode('ascii', 'ignore')
    msg = ''.join([done, m, '\n'])
    sys.stdout.write(msg)
    sys.stdout.flush()


def main(configFileName='etc/gsconfig.ini'):
    '''Send the profile status to all the members, using web-hooks

:param str configFileName: The name of the configuration file.'''
    args = get_args(configFileName)
    try:
        token = get_token_from_config(args.instance, args.config)
    except ConfigError as ce:
        m = 'Error with the configuration file "{config}":\n{error}\n'
        msg = m.format(config=args.config, error=ce.message)
        sys.stderr.write(msg)
        sys.exit(exit_vals['config_error'])

    parsedUrl = urlparse(args.url)
    if not parsedUrl.hostname:
        m = 'No host in the URL <{0}>\n'.format(args.url)
        sys.stderr.write(m)
        sys.exit(exit_vals['url_bung'])
    hostname = parsedUrl.hostname

    if args.verbose:
        sys.stdout.write('Retrieving the list of people...')
        sys.stdout.flush()
    try:
        userIds = get_userIds(hostname, token)
    except NotOk as no:
        m = '\nError communicating with the server while recieving the '\
            'list of people:\n{message}\n'
        msg = m.format(message=no)
        sys.stderr.write(msg)
        sys.exit(exit_vals['communication_failure'])

    if args.verbose:
        sys.stderr.write(' done\n')  # Getting the people
        sys.stdout.flush()
        sys.stdout.write('Sending the status notification to each person\n')
    for i, userId in enumerate(userIds):
        if args.verbose:
            show_progress(userId, i, len(userIds))

        try:
            r = send_status(hostname, userId, token)
        except NotOk, no:
            m = 'Error communicating with the server while sending the '\
                'status notification to {0}:\n{1}\n'
            msg = m.format(userId, no)
            r = {'status': -2, 'message': msg}
        show_done(r)
        if r['status'] == 0:
            sleep(args.throttle)

    sys.exit(exit_vals['success'])

if __name__ == '__main__':
    main()
