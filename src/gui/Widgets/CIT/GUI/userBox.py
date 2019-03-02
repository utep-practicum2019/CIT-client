import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class userBox(Gtk.ListBoxRow):

    def __init__(self, parent):
        super(userBox, self).__init__()
        logging.debug("Creating User Box")
        self.parent = parent

        # Main box container to hold the widgets
        self.topBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=700)
        self.add(self.topBox)

        # Makes the ARL image smaller 
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filename="/home/practicum2019/Documents/cit-client/src/gui/Widgets/CIT/GUI/ARL.png", 
                    width=120, 
                    height=120, 
                    preserve_aspect_ratio=True)


        # Adds ARL Image to the top left corner
        self.image = Gtk.Image.new_from_pixbuf(self.pixbuf)
        self.topBox.pack_start(self.image, False, False, 0)


        # Creates Box container to hold username and search bar orientation
        self.userBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.topBox.pack_start(self.userBox, True, False, 0)

        # Display users' username
        self.username = Gtk.Label()
        self.username.set_markup("<big>Jane Doe</big>")
        self.userBox.pack_start(self.username, True, False, 0)

        # Search bar
        self.searchBar = Gtk.SearchEntry()
        #searchBar.connect("key-release-event", self.on_search_clicked)
        self.userBox.pack_start(self.searchBar, True, False, 0)
