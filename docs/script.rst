:program:`smtp2gs`
==================

.. program:: send_profile

Synopsis
--------

   :program:`send_profile` [:option:`-h`] [:option:`-c` <CONFIG>] [:option:`-i` <INSTANCE>] :option:`url`

Description
-----------

:program:`send_profile` sends the monthly profile-status
notification out to all the people with profiles in a GroupServer
instance. Normally it is called by :manpage:`cron(8)`.

Positional Arguments
--------------------

.. option:: url

  The URL for the GroupServer site.

Optional Arguments
------------------

.. option:: -h, --help

  Show a help message and exit

.. option:: -c <CONFIG>, --config <CONFIG>

  The name of the GroupServer :doc:`config` (default
  :file:`{INSTANCE_HOME}/etc/gsconfig.ini`) that contains the
  token that will be used to authenticate the script when it
  tries to add the email to the site.

.. option:: -i <INSTANCE>, --instance <INSTANCE>

  The identifier of the GroupServer instance configuration to use
  (default ``default``).

Returns
=======

:program:`send_profile` returns ``0`` on success, or a non-zero
value on an error (following the convention specified in
:file:`/usr/include/sysexits.h`).
