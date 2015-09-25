# -*- coding: utf-8 -*-
# See /usr/include/sysexits.h
EX_OK = 0
EX_USAGE = 64
EX_DATAERR = 65
EX_NOUSER = 67
EX_PROTOCOL = 76
EX_TEMPFAIL = 75
EX_CONFIG = 78
# Standard for Bash: <http://www.tldp.org/LDP/abs/html/exitcodes.html>
EX_CTRL_C = 130
exit_vals = {
    'success': EX_OK,
    'config_error': EX_CONFIG,
    'url_bung': EX_USAGE,
    'communication_failure': EX_PROTOCOL,
    'socket_error': EX_PROTOCOL,
    'json_decode_error': EX_PROTOCOL,
    'no_user': EX_NOUSER,
    'terminated': EX_CTRL_C, }
