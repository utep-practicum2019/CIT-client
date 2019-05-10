# https://www.youtube.com/watch?v=Dmo8eZG5I2w
from PyQt5 import QtWidgets, uic
# from MacPPTP import connectToServer
import os
import sys
import signal
import subprocess
import webbrowser

username=""
password=""
connected=False
subProPid=1
# subPro=subprocess.Popen.pid
def connect_disconnectToServer(cORd):
    global subProPid
    global connected
    if(cORd==True and connected==False):
        username=dlg.userTextbox.toPlainText()
        password=dlg.passwordTextbox.toPlainText()
        os.system('sudo touch /etc/ppp/peers/PPTP_ConfigFile')
        # os.system('sudo echo "test input1" >> /etc/ppp/peers/129.108.7.159')
        PPTP_File=open("/etc/ppp/peers/PPTP_ConfigFile","r+")
        PPTP_TempFile=open("PPTP_ConfigTemplate.txt")
        # user=input("enter username: ")
        # password=input("enter password: ")
        PPTP_File.truncate(0)
        with PPTP_TempFile as oldfile, PPTP_File as newfile:
                    for line in oldfile:
                        if "remoteaddress" in line:
                            newfile.write("remoteaddress \"129.108.7.29\"\n")
                        elif "user" in line:
                            newfile.write("user "+'"'+username+'"'+"\n")
                        elif "password" in line and "hide-password" not in line:
                            newfile.write("password "+'"'+password+'"'+"\n")
                        else:    
                            newfile.write(line)
        # os.system('pppd call 129.108.7.159')
        subPro=subprocess.Popen(["pppd", "call", "PPTP_ConfigFile"],stdout=subprocess.PIPE)
        subProPid=subPro.pid
        connected=True
        # print(connected)
        webbrowser.open('http://129.108.7.29:5001/login')
        dlg.ConnectButton.setEnabled(False)
        dlg.DisconnectButton.setEnabled(True)
        dlg.RelaunchButton.setEnabled(True)

        # for line in out:
        #     if "PPTP: can't get interface" in str(line):
        #         # os.kill(subProPid,signal.SIGTERM)
        #         os.system('rm /etc/ppp/peers/PPTP_ConfigFile')
        #         connected=False
        #         print(connected)
        #         raise
        #     elif "Committed PPP store" in str(line):
                
        #         raise
        #         # webbrowser.open('facebook.com')
            
    elif(cORd==False and connected==True):
        # os.killpg(os.getpgid(subPro.pid), signal.SIGTERM)
        try:
            os.kill(subProPid,signal.SIGTERM)
        except ProcessLookupError:
            print("No process")
        os.system('rm /etc/ppp/peers/PPTP_ConfigFile')
        connected=False
        dlg.ConnectButton.setEnabled(True)
        dlg.DisconnectButton.setEnabled(False)
        dlg.RelaunchButton.setEnabled(False)
        # os.kill(os.getpgid(),signal.SIGTERM)
        # self.process.send_signal(signal.SIGTERM)
def relaunchBrowser():
    webbrowser.open('http://129.108.7.29:5001/login')
    
    
# def testFunc(boolean):
#     print("test")
    # print(dlg.userTextbox.toPlainText()) 

app=QtWidgets.QApplication([])
dlg=uic.loadUi("PPTP_GUII.ui")
dlg.DisconnectButton.setEnabled(False)
dlg.RelaunchButton.setEnabled(False)
#LoginConnect
# username=dlg.userTextbox.toPlainText()
# password=dlg.passwordTextbox.toPlainText()
# dlg.ConnectButton.clicked.connect(lambda: testFunc(True))
dlg.ConnectButton.clicked.connect(lambda: connect_disconnectToServer(True))
dlg.DisconnectButton.clicked.connect(lambda: connect_disconnectToServer(False))
dlg.RelaunchButton.clicked.connect(relaunchBrowser)
dlg.show()
app.exec()