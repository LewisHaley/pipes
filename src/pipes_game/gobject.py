"""Initialise and contain GObject (Gtk) support."""

# pylint: disable=unused-import, wrong-import-position

import gi

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, GdkPixbuf, Gtk, GLib
