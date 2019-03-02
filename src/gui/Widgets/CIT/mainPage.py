import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class Window(Gtk.ApplicationWindow):

    def __init__(self, app):
        super(Window, self).__init__(title="ARL CIT System", application=app)

        # Acts as the main container to hold other containers
        self.mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.mainBox)   

        # Container for the ARL logo, username, and search bar
        topBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=700)
        self.mainBox.pack_start(topBox, False, False, 0)

        # Add ARL Image for top left corner
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filename="/home/practicum2019/Documents/cit-client/src/gui/Widgets/CIT/ARL.png", 
                    width=120, 
                    height=120, 
                    preserve_aspect_ratio=True)

        image = Gtk.Image.new_from_pixbuf(pixbuf)
        topBox.pack_start(image, False, False, 0)


        # Creates Box container to hold username and search bar orientation
        userBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        topBox.pack_start(userBox, True, False, 0)

        # Display users' username
        username = Gtk.Label()
        username.set_markup("<big>Jane Doe</big>")
        userBox.pack_start(username, True, True, 0)

        # Search bar
        searchBar = Gtk.SearchEntry()
        #searchBar.connect("key-release-event", self.on_search_clicked)
        userBox.pack_start(searchBar, True, True, 0)


        # Menu Bar that contains the platforms and news area
        menuBar = Gtk.Notebook()
        self.mainBox.pack_start(menuBar, True, True, 0)      # Add to main window area

        hackathonPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hackathonPage.set_border_width(10)
        # hackathonPage.add(Gtk.Label('Contains information for the hackathon platform'))
        menuBar.append_page(hackathonPage, Gtk.Label('Hackathon'))

        rapidCyberPage = Gtk.Box()
        rapidCyberPage.set_border_width(10)
        rapidCyberPage.add(Gtk.Label('Contains information for the rapid cyber range platform'))
        menuBar.append_page(rapidCyberPage, Gtk.Label('Rapid Cyber Range'))

        helpPage = Gtk.Box()
        helpPage.set_border_width(10)
        helpPage.add(Gtk.Label('Contains information for the help page'))
        menuBar.append_page(helpPage, Gtk.Label('Help'))


        # Creates the hackathon subplatforms using gtk paned widget
        hackathonPlatforms = Gtk.Notebook()
        hackathonPlatforms.set_tab_pos(0)
        hackathonPage.pack_start(hackathonPlatforms, True, True, 0)


        hackathonChatPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hackathonChatPage.set_border_width(10)
        hackathonChatPage.add(Gtk.Label('Hackathon Chat System Page'))
        hackathonPlatforms.append_page(hackathonChatPage, Gtk.Label('Chat'))

        hackathonConfigPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hackathonConfigPage.set_border_width(10)
        hackathonConfigPage.add(Gtk.Label('Hackathon Configuration Page'))
        hackathonPlatforms.append_page(hackathonConfigPage, Gtk.Label('Configuration'))


    def quitApp(self, par):
        app.quit()



class Application(Gtk.Application):

    def __init__(self):
        super(Application, self).__init__()

    def do_activate(self):
        self.win = Window(self)
        self.win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = Application()
app.run(sys.argv)


