import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from HackathonPlatforms import HackathonPlatforms

class HelpPage(Gtk.ListBoxRow):
    def __init__(self, parent):
        super(HelpPage, self).__init__()
        logging.debug("Creating Help Page")
        self.parent = parent

        # Hackathon Page Area
        self.helpPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
        self.helpPage.set_border_width(10)
        self.helpPage.add(Gtk.Label('Contains information for the help page'))
        self.add(self.helpPage)