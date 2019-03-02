import gi, sys, logging
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository import WebKit

class HackathonPlatforms(Gtk.ListBoxRow):
    def __init__(self, parent):
        super(HackathonPlatforms, self).__init__()
        logging.debug("Creating Hackathon Platforms")
        self.parent = parent

        self.hackathonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hackathonBox.set_border_width(10)
        self.add(self.hackathonBox)

	webview = WebKit.WebView()
	webview.open("http://192.168.0.1:3000")


        # Creates the hackathon subplatforms using gtk paned widget
        self.hackathonPlatforms = Gtk.Notebook()
        self.hackathonPlatforms.set_tab_pos(0)
        self.hackathonBox.pack_start(self.hackathonPlatforms, True, True, 0)

        hackathonChatPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hackathonChatPage.set_border_width(10)
        hackathonChatPage.pack_start(webview, True, True, 0)
        self.hackathonPlatforms.append_page(hackathonChatPage, Gtk.Label('Chat'))

	hackathonWikiPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
	hackathonWikiPage.set_border_width(10)
	hackathonWikiPage.add(Gtk.Label('Wiki Page Information'))
	self.hackathonPlatforms.append_page(hackathonWikiPage, Gtk.Label('Wiki'))

        hackathonConfigPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hackathonConfigPage.set_border_width(10)
        hackathonConfigPage.add(Gtk.Label('Hackathon Configuration Page'))
        self.hackathonPlatforms.append_page(hackathonConfigPage, Gtk.Label('Configuration'))
