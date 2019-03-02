import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import logging
import configparser
import os

class LoginDialog(Gtk.Dialog):
    
    CONFIG_FILE = "config/config.ini"
    def __init__(self, parent):
        logging.debug("LoginDialog(): instantiated")
        Gtk.Dialog.__init__(self, "Login", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_resizable(False)
        
        self.config = configparser.ConfigParser()
        self.readConfig(LoginDialog.CONFIG_FILE)
		
        box = self.get_content_area()

        self.set_default_size(150, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

        self.label = Gtk.Label("Login to CIT")
        self.box_main.pack_start(self.label, True, True, 0)

        self.box_spacer01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.box_main.pack_start(self.box_spacer01, True, True, 0)

        self.box_serverIP = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.serverIPLabel = Gtk.Label("Server Address")
        self.box_serverIP.pack_start(self.serverIPLabel, True, True, 0)

        self.serverIPEntry = Gtk.Entry()
        self.serverIPEntry.set_text(self.config['SERVER']['SERVER_IP'])
        self.box_serverIP.pack_start(self.serverIPEntry, True, True, 0)
        self.box_main.pack_start(self.box_serverIP, True, True, 0)

        self.box_username = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.usernameLabel = Gtk.Label("Username")
        self.box_username.pack_start(self.usernameLabel, True, True, 0)

        self.usernameEntry = Gtk.Entry()
        self.usernameEntry.set_text(self.config['SERVER']['USERNAME'])
        self.box_username.pack_start(self.usernameEntry, True, True, 0)
        self.box_main.pack_start(self.box_username, True, True, 0)

        self.box_password = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.passwordLabel = Gtk.Label("Password")
        self.box_password.pack_start(self.passwordLabel, True, True, 0)

        self.passwordEntry = Gtk.Entry()
        self.passwordEntry.set_text("")
        self.passwordEntry.set_visibility(False)
        # enter key should trigger the default action
        self.passwordEntry.set_activates_default(True)
        # make OK button the default
        okButton = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        okButton.set_can_default(True)
        okButton.grab_default()
        
        #setup an intermediate function to call on response
        self.connect("response", self.dialog_response)
                        
        self.box_password.pack_start(self.passwordEntry, True, True, 0)
        self.box_main.pack_start(self.box_password, True, True, 0)
        
        box.pack_start(self.box_main, True, True, 0)
        self.show_all()
       
    def dialog_response(self, widget, response_id):
        logging.debug("dialog_response(): instantiated")
        if response_id == Gtk.ResponseType.OK:
            logging.debug("dialog_response(): OK was pressed, saving serverIP and username")
            self.writeConfig(LoginDialog.CONFIG_FILE, self.serverIPEntry.get_text(), self.usernameEntry.get_text())
        
    def readConfig(self, filename):
        logging.debug("readConfig(): instantiated")
        logging.debug("readConfig(): checking if file exists: " + filename)
        if os.path.exists(filename):
            logging.debug("readConfig(): file was found: " + filename)
            self.config.read(filename)
        else:
            logging.debug("readConfig(): file was NOT found: " + filename)
            self.config['SERVER']['SERVER_IP'] = ""
            self.config['SERVER']['USERNAME'] = ""

    def writeConfig(self, filename, serverIP, username):
        logging.debug("writeConfig(): instantiated")
        self.config['SERVER']['SERVER_IP'] = serverIP
        self.config['SERVER']['USERNAME'] = username   
        logging.debug("writeConfig(): writing to file: " + filename)
        with open(filename, 'w') as configfile:
			self.config.write(configfile)
       
    def clearPass(self):
        logging.debug("clearPass(): instantiated")
        self.passwordEntry.set_text("")

    def clearEntries(self):
        logging.debug("clearEntries(): instantiated")
        self.passwordEntry.set_text("")
        self.serverIPEntry.set_text("")
        self.usernameEntry.set_text("")
        self.passwordEntry.set_text("")

    def getServerIPText(self):
        logging.debug("getServerIPText(): instantiated")
        return self.serverIPEntry.get_text()
        
    def getUsernameText(self):
        logging.debug("getUsernameText(): instantiated")
        return self.usernameEntry.get_text()

    def getPasswordText(self):
        logging.debug("getPasswordText(): instantiated")
        return self.passwordEntry.get_text()
		
