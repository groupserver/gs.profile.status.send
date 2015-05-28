:mod:`gs.profile.status.send` Internals
=======================================

.. currentmodule:: gs.profile.status.send

The :mod:`gs.profile.status.send` does not have a public API,
other than what is provided by the script itself. However, the
internals are documented below.

The script
----------

The :program:`sendprofile` script is provided by the module
:mod:`.script`. The :func:`main` function takes the name of the
default configuration file a single argument, which is normally
supplied by ``buildout`` when it generates the
:program:`sendprofile` script from the entry point.

The list of people
~~~~~~~~~~~~~~~~~~

.. autodata:: gs.profile.status.send.script.PROFILE_URI

.. autofunction:: gs.profile.status.send.script.get_userIds

Sending the notification
~~~~~~~~~~~~~~~~~~~~~~~~

.. autodata:: gs.profile.status.send.script.SEND_STATUS_URI

.. autofunction:: gs.profile.status.send.script.send_status

The script proper
~~~~~~~~~~~~~~~~~

.. autofunction:: gs.profile.status.send.script.main

.. autofunction:: gs.profile.status.send.script.show_progress

.. autofunction:: gs.profile.status.send.script.show_done
