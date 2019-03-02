import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from platformsBox import platformsBox
from userBox import userBox

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        logging.debug("Creating Application")
        super(AppWindow, self).__init__(title="ARL CIT System", application=app)

        # Acts as the main container to hold other containers
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.mainBox)   

        # Creates the upper box area that includes the ARL Logo, username, and search bar
        self.topBox = userBox(self)
        self.mainBox.pack_start(self.topBox, False, False, 0)

        # Menu Bar that contains the platforms and news area
        self.menuBar = platformsBox(self)
        self.mainBox.pack_start(self.menuBar, True, True, 0)      # Add to main window area
