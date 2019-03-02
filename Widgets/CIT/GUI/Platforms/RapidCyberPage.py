import gi, sys, logging
import webbrowser
import subprocess
import os
from GAsyncSpawn import GAsyncSpawn 
from gi.repository import Gtk, GdkPixbuf
from gi.repository import WebKit
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')



class RapidCyberPage(Gtk.ListBoxRow):
	
    def __init__(self, parent):
        super(RapidCyberPage, self).__init__()
        logging.debug("Creating Rapid Cyber Range Page")
        self.parent = parent
	self.is_clicked = False
	self.pid = 0

	webview = WebKit.WebView()
	webview.open("http://192.168.0.1:8080")

	self.add(webview)


"""
        # Hackathon Page Area
        self.rapidCyberPage = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
        self.rapidCyberPage.set_border_width(10)
        self.add(self.rapidCyberPage)


	self.button = Gtk.Button.new_with_label("Visit Rapid Cyber Range System")
	self.button.connect("clicked", self.on_click_me_clicked)
	self.rapidCyberPage.pack_start(self.button, False, False, 0)


	#self.command = ['/bin/su', '-', 'practicum2019',  '-c', 'firefox -new-window http://192.168.0.1:8080']
	self.command = ['/usr/bin/sudo', '-u', 'practicum2019', 'firefox -new-window http://192.168.0.1:8080']
	
	self.spawn = GAsyncSpawn()
        self.spawn.connect("process-done", self.on_process_done)
        self.spawn.connect("stdout-data", self.on_stdout_data)
	self.spawn.connect("stderr-data", self.on_stderr_data)
	

   
    def on_click_me_clicked(self, button):
	self.button.set_sensitive(False)
        pid = self.spawn.run(self.command)
	self.pid = pid
	print "Started as process #",pid
	

    def on_process_done(self, sender, retval):
        self.button.set_sensitive(True)
        print "Done. exit code:", retval       

        
    def on_stdout_data(self, sender, line):
        print "[STDOUT]", line.strip("\n")


    def on_stderr_data(self, sender, line):
	print "[STDERR]", line.strip("\n") 


#button.hide()
	p = subprocess.Popen("su - practicum2019 -c 'firefox -new-window http://192.168.0.1:8080/'", shell=True)
	
	print self.poll
	if not p.wait():
		button.hide()
		print p.wait()
		
    		#print("Still working...")
		#button.set_sensitive(True)
	print p.wait()
	if p.wait():
		button.show()
		#button.set_sensitive(False)	

	#button.set_sensitive(False)


	#subprocess.Popen(["su - practicum2019 -c firefox"])
	#p = subprocess.call("su - practicum2019 -c 'firefox -new-window http://192.168.0.1:8080/'", shell=True)
	#p = subprocess.check_output(["su - practicum2019 -c 'firefox -new-window http://192.168.0.1:8080/'"], shell=True, stderr=subprocess.STDOUT)
	self.is_clicked =  not self.is_clicked
	#print self.poll
	if self.is_clicked and self.poll != None:
		p = subprocess.Popen("su - practicum2019 -c 'firefox -new-window http://192.168.0.1:8080/'", shell=True)
		self.poll = p.poll()
		print self.poll
	else:
		if self.poll == None:
			button.set_sensitive(True)
		else:
			button.set_sensitive(False)
	#webbrowser.open_new('http://192.168.0.1:8080/')

"""
