import gi; gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import logging
from gui.Dialogs.LoginDialog import LoginDialog
from gui.Dialogs.LoginConnectingDialog import LoginConnectingDialog
from gui.Dialogs.DisconnectingDialog import DisconnectingDialog
from gui.Dialogs.LaunchCITDialog import LaunchCITDialog
from gui.Widgets.VMManageBox import VMManageBox
from engine.Engine import Engine
from engine.Connection.Connection import Connection
from time import sleep
import threading


import configparser
import os


# Additions for CIT
import subprocess
import sys
import re
import getpass


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class ConnectionBox(Gtk.ListBox):

    CONNECTION_NAME = "citclient"

    def __init__(self, parent, vmManageBox):
        super(ConnectionBox, self).__init__()

        self.connect('destroy', self.catchClosing)

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
        self.citConnectionLabel = Gtk.Label(xalign=0)
        self.citConnectionLabel.set_markup("Choose Connection Type: ")
        self.hbox.pack_start(self.citConnectionLabel, True, True, 0)

        connection_store = Gtk.ListStore(str)
        connections = ["PPTP", "L2TP"]
        for connection in connections:
            connection_store.append([connection])

        self.connection_combo = Gtk.ComboBox.new_with_model(connection_store)
        self.connection_combo.connect("changed", self.on_connection_combo_changed)
        self.renderer_text = Gtk.CellRendererText()
        self.connection_combo.pack_start(self.renderer_text, True)
        self.connection_combo.add_attribute(self.renderer_text, "text", 0)
        self.hbox.pack_start(self.connection_combo, False, False, 0)
        self.add(self.row)


        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.citLauchLabel = Gtk.Label(xalign=0)
        self.citLauchLabel.set_markup("Open CIT with default browser: ")
        self.hbox.pack_start(self.citLauchLabel, True, True, 0)
        self.citLaunchButton = Gtk.Button("Launch CIT")
        self.citLaunchButton.connect("clicked", self.openCITTab)
        self.citLaunchButton.props.valign = Gtk.Align.CENTER
        self.hbox.pack_start(self.citLaunchButton, False, True, 0)
        self.add(self.row)

        self.citLauchLabel.set_sensitive(False)
        self.citLaunchButton.set_sensitive(False)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.add(self.row)

        self.status = -1
        # self.QUIT_SIGNAL = False
        self.QUIT_SIGNAL = threading.Event()
        self.t = threading.Thread(target=self.watchStatus, args=(self.QUIT_SIGNAL, ))
        self.t.start()


    def on_connection_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            connection = model[tree_iter][0]
            print("Selected: country=%s" % connection)
            if connection == "PPTP":
                print("The logic for PPTP can go here...")
            if connection == "L2TP":
                print("The logic for L2TP can go here...")


    def openCITTab(self, button):
        logging.debug("openCITTab(): initiated")
        if button.get_label() != "Launch CIT":
            return

        command = "python -m webbrowser -n http://" + self.serverIPText
        if re.match('linux', sys.platform):
            import pwd
            for p in pwd.getpwall():
                if p[3] >= 999 and re.match('/home', p[5]):
                    user = p[0]
                    break
            process = subprocess.Popen(["su","-", user, "-c", command])
        elif re.match('win32', sys.platform):
            process = subprocess.Popen(command)
        else:
            process = None

        logging.debug("openCITTab(): launching dialog")
        launchDialog = LaunchCITDialog(self.parent, process)
        launchDialog.run()
        retVal = process.poll()
        while retVal is None:
            logging.debug("watchLaunchStatus(): polling launch process")
            logging.debug("watchLaunchStatus(): retVal: " + str(retVal))
            if retVal is None:
                launchDialog.setGUIStatus("Attempting Launch...", True, False)
                logging.debug("watchLaunchStatus(): process running")
            elif retVal == 0:
                launchDialog.setGUIStatus("Launch successful.", False, True)
                logging.debug("watchLaunchStatus(): browser launch success")
            else:
                launchDialog.setGUIStatus("Launch failed.", False, True)
                logging.debug("watchLaunchStatus(): browser launch failure")
            sleep(1)
            retVal = process.poll()
        launchDialog.destroy()
        logging.debug("openCITTab(): ended")

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
            # save the ip to open browser later
            self.serverIPText = serverIPText
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
                res = self.attemptLogin(serverIPText, usernameText, passwordText)

                if res["connStatus"] == Connection.CONNECTED:
                    button.set_label("Disconnect")
                    self.connStatusLabel.set_label("Connected.")
                    self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 1, 0, .5))
                    self.vmManageBox.setConnectionObject(res)
                    self.vmManageBox.set_sensitive(True)
                    self.citLaunchButton.set_sensitive(True)
                    self.citLauchLabel.set_sensitive(True)
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
                self.citLaunchButton.set_sensitive(False)
                self.citLauchLabel.set_sensitive(False)


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

    def watchStatus(self, control):
        logging.debug("watchDisconnStatus(): instantiated")
        #self.statusLabel.set_text("Checking connection")
        e = Engine.getInstance()
        #will check status every 1 second and will either display stopped or ongoing or connected
        #while(self.QUIT_SIGNAL == False):
        while not control.is_set():
            logging.debug("watchDisconnStatus(): running: pptp status " + ConnectionBox.CONNECTION_NAME)
            self.status = e.execute("pptp status " + ConnectionBox.CONNECTION_NAME)
            #connStatus" : self.connStatus, "disConnStatus" : self.disConnStatus, "refreshConnStatus
            if self.status != -1 and self.status["connStatus"] != Connection.CONNECTING and self.status["disConnStatus"] != Connection.DISCONNECTING and self.status["refreshConnStatus"] != Connection.REFRESHING:
                logging.debug("watchDisconnStatus(): running: pptp forcerefreshconnstatus  " + ConnectionBox.CONNECTION_NAME)
                self.status = e.execute("pptp forcerefreshconnstatus " + ConnectionBox.CONNECTION_NAME)
                #wait until it's done refreshing
                self.status = e.execute("pptp status " + ConnectionBox.CONNECTION_NAME)
                while self.status["refreshConnStatus"] == Connection.REFRESHING:
                    sleep(2)
                    self.status = e.execute("pptp status " + ConnectionBox.CONNECTION_NAME)
                #read the new state
                logging.debug("watchDisconnStatus(): running: pptp status " + ConnectionBox.CONNECTION_NAME)
                self.status = e.execute("pptp status " + ConnectionBox.CONNECTION_NAME)

                logging.debug("watchStatus(): result: " + str(self.status))
                if self.status["connStatus"] == Connection.NOT_CONNECTED or self.status["connStatus"] == Connection.CONNECTED:
                    GLib.idle_add(self.setGUIStatus, self.status)
                    #break
                else:
                    logging.debug("watchStatus(): Could not get status: " + str(self.status))
                #break
            sleep(5)

    def catchClosing(self, widget=None):
        logging.debug("ConnectionBox : catchClosing(): instantiated")
        logging.debug("ConnectionBox : connection status killing thread")
        if(self.t.isAlive()):
            self.QUIT_SIGNAL.set()
            self.t.join()
        return False

    #__gsignal__ = {"delete-event": "overide"}
    #def on_close_display(self, event, widget):
    #    self.catchClosing()
    #    return True

    def setGUIStatus(self, res):
        logging.debug("setGUIStatus(): instantiated: " + str(res))
        if res["connStatus"] == Connection.CONNECTED:
            self.connectionButton.set_label("Disconnect")
            self.connStatusLabel.set_label(" Connected ")
            self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 1, 0, .5))
            self.vmManageBox.setConnectionObject(res)
            self.vmManageBox.set_sensitive(True)
            if self.vmManageBox.vmStatusLabel.get_text() == " Configured ":
                self.vmManageBox.startVMButton.set_sensitive(True)
                self.vmManageBox.suspendVMButton.set_sensitive(True)
        if res["connStatus"] == Connection.NOT_CONNECTED:
            self.connectionButton.set_label("Connect")
            self.connStatusLabel.set_label(" Disconnected ")
            self.connEventBox.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1, 0, 0, .5))
            self.vmManageBox.set_sensitive(False)
            self.vmManageBox.startVMButton.set_sensitive(False)
            self.vmManageBox.suspendVMButton.set_sensitive(False)
