import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class HackathonPlatforms(Gtk.ListBoxRow):
    def __init__(self, parent):
        super(HackathonPlatforms, self).__init__()
        logging.debug("Creating Hackathon Platforms")
        self.parent = parent

        self.hackathonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hackathonBox.set_border_width(10)
        self.add(self.hackathonBox)

        # Creates the hackathon subplatforms using gtk paned widget
        self.hackathonPlatforms = Gtk.Notebook()
        self.hackathonPlatforms.set_tab_pos(0)
        self.hackathonBox.pack_start(self.hackathonPlatforms, True, True, 0)

        hackathonChatPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hackathonChatPage.set_border_width(10)
        hackathonChatPage.add(Gtk.Label('Hackathon Chat System Page from the hackathonPlatforms class'))
        self.hackathonPlatforms.append_page(hackathonChatPage, Gtk.Label('Chat'))

        hackathonConfigPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hackathonConfigPage.set_border_width(10)
        hackathonConfigPage.add(Gtk.Label('Hackathon Configuration Page'))
        self.hackathonPlatforms.append_page(hackathonConfigPage, Gtk.Label('Configuration'))