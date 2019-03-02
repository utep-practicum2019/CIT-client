import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.Widgets.VMTreeWidget import VMTreeWidget
from gui.Dialogs.VMRetrieveDialog import VMRetrieveDialog
from gui.Dialogs.ConfiguringVMDialog import ConfiguringVMDialog
from engine.Engine import Engine
import logging

class ConfigureVMDialog(Gtk.Dialog):
    def __init__(self, parent, connection):
        Gtk.Dialog.__init__(self, "Configure Virtual Machine", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.connName = "citclient"
        self.connection = connection
        self.vms = {}
        self.vmName = ""
        self.set_default_size(500, 300)
        self.status = None

        label = Gtk.Label("Select a VM and Adaptor")

        # Here we will place the tree view
        treeWidget = VMTreeWidget(self)
        self.connect("response", self.dialogResponseActionEvent)
            
        select = treeWidget.treeView.get_selection()
        select.connect("changed", self.onItemSelected)
        
        self.status = None

        box = self.get_content_area()
        box.add(label)
        box.add(treeWidget)
        
        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)
        
        self.show_all()
    
        vmRetrieveDialog = VMRetrieveDialog(self)
        vmRetrieveDialog.run()
        s = vmRetrieveDialog.getFinalData()
        self.vms = s["mgrStatus"]["vmstatus"]
        vmRetrieveDialog.destroy()
        
        treeWidget.populateTreeStore(self.vms)
        
    def onItemSelected(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter == None:
            return
        self.vmName = model[treeiter][0]
        self.adaptorSelected = model[treeiter][1]
        self.status = model[treeiter][2]
        if "\"none\"" in self.adaptorSelected or "adaptor disabled" in self.adaptorSelected:
            self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)
            return
        if "Running" in self.status:
            self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)
            return
            
        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(True)
            
    def dialogResponseActionEvent(self, dialog, responseID):
        # OK was clicked and there is text
        if responseID == Gtk.ResponseType.OK:
            #check to make sure the connection is still connected:
            logging.debug("dialogResponseActionEvent(): OK was pressed: " + self.vmName + " " + self.adaptorSelected)
            self.status = {"vmName" : self.vmName, "adaptorSelected" : self.adaptorSelected}
            #get the first value in adaptorSelected (should always be a number)
            adaptorNum = self.adaptorSelected[0]
            octetLocal = self.connection["localIP"].split(".")[3]
            #configuringVMDialog = ConfiguringVMDialog(self, self.vmName, self.connection["localIP"], self.connection["remoteIP"], octetLocal, adaptorNum, self.connName)
            configuringVMDialog = ConfiguringVMDialog(self, self.vmName, self.connection["localIP"], "192.168.0.1", octetLocal, adaptorNum, self.connName)
            configuringVMDialog.run()
            s = configuringVMDialog.getFinalData()
            configuringVMDialog.destroy()
    
    def getFinalStatus(self):
        return self.status
