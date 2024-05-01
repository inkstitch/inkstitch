# Authors: see git history
#
# Copyright (c) 2022 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
#
# The original Source can be found here:
# https://gitlab.com/inkscape/inkscape/uploads/ca84fa1092f8d6e81e49b99e659cd025/dbus_test.py

import sys
from time import sleep

import gi
from gi.repository import Gio, GLib

gi.require_version("Gio", "2.0")


class DBusActions:
    def __init__(self):
        try:
            bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        except BaseException:
            exit()

        name = 'org.inkscape.Inkscape'
        appGroupName = "/org/inkscape/Inkscape"
        self.applicationGroup = Gio.DBusActionGroup.get(
            bus,
            name,
            appGroupName)

    def run_action(self, action, param):
        self.applicationGroup.activate_action(action, param)


# start dbus
dbus = DBusActions()
# give it some time to start
sleep(0.5)
# clear previous selection
dbus.run_action('select-clear', None)
# select with the list of ids
dbus.run_action('select-by-id', GLib.Variant.new_string(sys.argv[1]))
