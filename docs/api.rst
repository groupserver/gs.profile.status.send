:mod:`gs.profile.status.send` Internals
==============================================

.. currentmodule:: gs.profile.status.send

The :mod:`gs.profile.status.send` does not have a public API,
other than what is provided by the script itself. However, the
internals are documented below.

The script
----------

The ``send_profile`` script is provided by the module
:mod:`.script`. The :func:`main` function takes the name of the
default configuration file a single argument, which is normally
supplied by ``buildout`` when it generates the ``send_profile``
script from the entry point.
