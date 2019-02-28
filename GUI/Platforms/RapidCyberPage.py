import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class RapidCyberPage(Gtk.ListBoxRow):
    def __init__(self, parent):
        super(RapidCyberPage, self).__init__()
        logging.debug("Creating Rapid Cyber Range Page")
        self.parent = parent

        # Hackathon Page Area
        self.rapidCyberPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
        self.rapidCyberPage.set_border_width(10)
        self.rapidCyberPage.add(Gtk.Label('Contains information for the rapid cyber range page'))
        self.add(self.rapidCyberPage)