from ..libs import Gtk
from ..window import GtkViewport
from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = Gtk.ScrolledWindow()

        # Set this minimum size of scroll windows because we must reserve space for
        # scrollbars when splitter resized. See, https://gitlab.gnome.org/GNOME/gtk/-/issues/210
        self.native.set_min_content_width(70)
        self.native.set_min_content_height(70)

        self.native.set_overlay_scrolling(True)
        self.native.interface = self.interface

    def set_content(self, widget):
        self.inner_container = widget

        widget.viewport = GtkViewport(self.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        # Remove the old widget before add the new one
        if self.native.get_child():
            self.native.get_child().destroy()

        # Add the widget to ScrolledWindow as a scrollable widget
        self.native.add(self.inner_container.native)
        self.native.show_all()

    def set_app(self, app):
        if self.interface.content:
            self.interface.content.app = app

    def set_window(self, window):
        if self.interface.content:
            self.interface.content.window = window

    def set_horizontal(self, value):
        self.native.set_policy(
            Gtk.PolicyType.AUTOMATIC if self.interface.horizontal else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if self.interface.vertical else Gtk.PolicyType.NEVER,
        )

    def set_vertical(self, value):
        self.native.set_policy(
            Gtk.PolicyType.AUTOMATIC if self.interface.horizontal else Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC if self.interface.vertical else Gtk.PolicyType.NEVER,
        )
