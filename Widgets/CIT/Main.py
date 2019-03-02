import gi, sys, logging
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from GUI.AppWindow import AppWindow

        
class Application(Gtk.Application):

    def __init__(self):
        super(Application, self).__init__()
	self.win = AppWindow(self)
	self.win.show_all()

    def do_activate(self):
        self.win = AppWindow(self)
        self.win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


"""
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program at main application")
    app = Application()
    app.run(sys.argv)


logging.debug("Starting Program as non-main application")
app = Application()
app.run(sys.argv)
"""


