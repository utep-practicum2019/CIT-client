import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from Platforms.HackathonPage import HackathonPage
from Platforms.RapidCyberPage import RapidCyberPage
from Platforms.HelpPage import HelpPage

class platformsBox(Gtk.ListBoxRow):
    def __init__(self, parent):
        super(platformsBox, self).__init__()
        logging.debug("Creating Platforms Box")
        self.parent = parent

        # Menu Bar that contains the platforms and news area
        self.menuBar = Gtk.Notebook()
        self.add(self.menuBar)   # Add to main window area

        # Hackathon Page Area
        hackathonPage = HackathonPage(self)
        self.menuBar.append_page(hackathonPage, Gtk.Label('Hackathon'))

        # Rapid Cyber Range Page Area
        rapidCyberPage = RapidCyberPage(self)
        self.menuBar.append_page(rapidCyberPage, Gtk.Label('Rapid Cyber Range'))

        # Help Page Area
        helpPage = HelpPage(self)
        self.menuBar.append_page(helpPage, Gtk.Label('Help'))
