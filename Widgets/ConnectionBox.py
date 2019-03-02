import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import logging
from gui.Dialogs.LoginDialog import LoginDialog
from gui.Dialogs.LoginConnectingDialog import LoginConnectingDialog
from gui.Dialogs.DisconnectingDialog import DisconnectingDialog
from gui.Widgets.VMManageBox import VMManageBox
from engine.Engine import Engine
from engine.Connection.Connection import Connection
from CIT.Main import Application
import configparser
import os

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class ConnectionBox(Gtk.ListBox):

    CONNECTION_NAME = "citclient"
    
    def __init__(self, parent, vmManageBox):
        super(ConnectionBox, self).__init__()
        
        logging.debug("Creating ConnectionBox")
        self.parent = parent
        self.vmManageBox = vmManageBox
        
        self.set_selection_mode(Gtk.SelectionMode.NONE)
        self.set_border_width(10)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.connectionBoxDescLabel = Gtk.Label(xalign=0)
        self.connectionBoxDescLabel.set_markup("<b>CIT Connection</b>")
        self.hbox.pack_start(self.connectionBoxDescLabel, True, True, 0)
        self.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.connStatusDescLabel = Gtk.Label("Connection Status: ", xalign=0)
        self.hbox.pack_start(self.connStatusDescLabel, True, True, 0)

        self.connStatusLabel = Gtk.Label(" Disconnected ", xalign=0)
        self.connEventBox = Gtk.EventBox()
        self.connEventBox.add(self.connStatusLabel)
        self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 0, 0, .5))
        self.hbox.pack_start(self.connEventBox, False, True, 0)
        self.connectionButton = Gtk.Button("Connect")
        self.connectionButton.connect("clicked", self.changeConnState)
        self.connectionButton.props.valign = Gtk.Align.CENTER
        self.hbox.pack_start(self.connectionButton, False, True, 0)
        self.add(self.row)
        
        self.vmManageBox.set_sensitive(False)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.label = Gtk.Label("Automatic Reconnect", xalign=0)
        self.check = Gtk.CheckButton()
        # disable for now
        self.check.set_sensitive(False)

        self.hbox.pack_start(self.label, True, True, 0)
        self.hbox.pack_start(self.check, False, True, 0)

        self.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.add(self.row)

    def changeConnState(self, button):
        logging.debug("changeConnState(): initiated")
        logging.debug("changeConnState(): Button Label: " + button.get_label())
        if button.get_label() == "Connect":
            #start the login dialog
            loginDialog = LoginDialog(self.parent)
            response = loginDialog.run()
            #get results from dialog
            serverIPText = loginDialog.getServerIPText()
            usernameText = loginDialog.getUsernameText()
            passwordText = loginDialog.getPasswordText()
            #close the dialog
            loginDialog.destroy()                
            #try to connect using supplied credentials
            if response == Gtk.ResponseType.OK:		
                #check if the input was filled
                if serverIPText.strip() == "" or usernameText.strip() == "" or passwordText.strip() == "":
                    logging.error("Parameter was empty!")
                    inputErrorDialog = Gtk.MessageDialog(self.parent, 0, Gtk.MessageType.ERROR,
                    Gtk.ButtonsType.OK, "All fields must be non-empty...")
                    inputErrorDialog.run()
                    inputErrorDialog.destroy()
                    return
                #process the input from the login dialog
                #TODO: also remember for later
                res = self.attemptLogin(serverIPText, usernameText, passwordText)

                if res["connStatus"] == Connection.CONNECTED:
                    button.set_label("Disconnect")
                    self.connStatusLabel.set_label(" Connected ")
                    self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 1, 0, .5))
                    self.vmManageBox.setConnectionObject(res)
                    self.vmManageBox.set_sensitive(True)
		    #from CIT.Main import Application
		    logging.debug("Starting the client side program")
		    self.citApplication = Application()
                    if self.vmManageBox.vmStatusLabel.get_text() == " Configured ":
                        self.vmManageBox.startVMButton.set_sensitive(True)
                        self.vmManageBox.suspendVMButton.set_sensitive(True)
    
            elif response == Gtk.ResponseType.CANCEL:
                #just clear out the dialog
                loginDialog.clearEntries()
                loginDialog.destroy()

        else:
            #call disconnect logic
            res = self.attemptDisconnect()
            if res["connStatus"] == Connection.NOT_CONNECTED:
                button.set_label("Connect")
                self.connStatusLabel.set_label(" Disconnected ")
                self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 0, 0, .5))
                self.vmManageBox.set_sensitive(False)
                self.vmManageBox.startVMButton.set_sensitive(False)
                self.vmManageBox.suspendVMButton.set_sensitive(False)
    
    def attemptLogin(self, serverIP, username, password):
        logging.debug("attemptLogin(): initiated")
        #need to create a thread (probably a dialog box with disabled ok button until connection either times out (5 seconds), connection good
        e = Engine.getInstance()
        e.execute("pptp start " + ConnectionBox.CONNECTION_NAME + " " + serverIP + " " + username + " " + password)
        loginConnectingDialog = LoginConnectingDialog(self.parent, ConnectionBox.CONNECTION_NAME)
        loginConnectingDialog.run()
        s = loginConnectingDialog.getFinalStatus()
        loginConnectingDialog.destroy()
        return s
        
    def attemptDisconnect(self):
        logging.debug("attemptDisconnect(): initiated")
        #need to create a thread (probably a dialog box with disabled ok button until connection either times out (5 seconds), connection good
        e = Engine.getInstance()
        e.execute("pptp stop " + ConnectionBox.CONNECTION_NAME)
        disconnectingDialog = DisconnectingDialog(self.parent, ConnectionBox.CONNECTION_NAME)
        disconnectingDialog.run()
        s = disconnectingDialog.getFinalStatus()
        disconnectingDialog.destroy()
        return s
