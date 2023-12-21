"""Display and interaction handling."""

from typing import Callable, Mapping, Tuple, Union

import numpy

from .gobject import Gdk, GdkPixbuf, Gtk


class Display(Gtk.Window):
    """Display and interaction logic."""

    def __init__(self, size: Tuple[int, int], window_name: str) -> None:
        """Create a new instance of `Display`.

        :param size: the size of the display
        :param window_name: the name to give the window display
        """
        super().__init__()
        self.set_title(window_name)
        self.set_default_size(*size)
        self.connect("destroy", Gtk.main_quit)
        self.image = Gtk.Image()
        self.add(self.image)

        self.connect("key-press-event", self.on_key_press)
        self._callback_map = {
            "q": self.close,
            "Q": self.close,
        }

    def set_key_press_callbacks(
        self,
        callback_map: Mapping[Union[str, Tuple[str]], Callable],
    ) -> None:
        """Set the mapping of key-presses to callbacks.

        :param callback_map: a map of key-presses to callable functions.
        """
        fixed_map = {}
        for key, callback in callback_map.items():
            if isinstance(key, tuple):
                for key_ in key:
                    fixed_map[key_] = callback
            else:
                fixed_map[key] = callback
        self._callback_map.update(fixed_map)

    def on_key_press(  # pylint: disable=unused-argument
        self,
        widget: Gtk.Window,
        event: Gdk.EventKey,
    ) -> None:
        """React to keypresses from the user.

        :param widget: the receiving widget
        :param event: the keypress event
        """
        if callback := self._callback_map.get(Gdk.keyval_name(event.keyval)):
            callback()

    def update(self, buf: numpy.array) -> None:
        """Update the window.

        :param buf: the image buffer, as a numpy array
        """
        bits_per_sample = numpy.dtype(buf.dtype).itemsize * 8
        height, width, channels = buf.shape
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            buf.tobytes(),
            colorspace=GdkPixbuf.Colorspace.RGB,
            has_alpha=channels == 4,
            bits_per_sample=bits_per_sample,
            width=width,
            height=height,
            rowstride=width * channels,
        )
        self.image.set_from_pixbuf(pixbuf)

    def start(self) -> None:
        """Start the display."""
        self.show_all()
        Gtk.main()
