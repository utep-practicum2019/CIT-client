import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from HackathonPlatforms import HackathonPlatforms

class HackathonPage(Gtk.ListBoxRow):
    def __init__(self, parent):
        super(HackathonPage, self).__init__()
        logging.debug("Creating Hackathon Page")
        self.parent = parent

        # Hackathon Page Area
        self.hackathonPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
        self.hackathonPage.set_border_width(10)
        self.add(self.hackathonPage)

        # Inserts the hackathon subplatforms to Hackathon Page
        self.hackathonPlatforms = HackathonPlatforms(self)
        self.hackathonPage.pack_start(self.hackathonPlatforms, True, True, 0)