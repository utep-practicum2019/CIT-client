import configparser
import os
import logging

class ConfigurationFile():

    def __init__(self):
        self.filename = "config/config.ini"
        self.config = configparser.ConfigParser()
        self.readConfig()

    def readConfig(self):
        logging.debug("readConfig(): instantiated")
        logging.debug("readConfig(): checking if file exists: " + self.filename)
        if os.path.exists(self.filename):
            logging.debug("readConfig(): file was found: " + self.filename)
            self.config.read(self.filename)
        else:
            logging.debug("readConfig(): file was NOT found: " + self.filename)
            self.config['SERVER']['SERVER_IP'] = ""
            self.config['SERVER']['USERNAME'] = ""
            self.config['SERVER']['INTERNAL_IP'] = "10.0.0.1"

            self.config['VBOX_WIN']['VBOX_PATH'] = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
            self.config['VBOX_LINUX']['VBOX_PATH'] = "VBoxManage"

    def getConfig(self):
        return self.config

    #currently only accepts serverIP and username as saveable to the config file
    def writeConfig(self, filename, serverIP, username):
        logging.debug("writeConfig(): instantiated")
        self.config['SERVER']['SERVER_IP'] = serverIP
        self.config['SERVER']['USERNAME'] = username
        logging.debug("writeConfig(): writing to file: " + filename)
        with open(filename, 'w') as configfile:
            self.config.write(configfile)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting ConfigurationFile driver")

    #self.readConfig(ConfigurationFile.CONFIG_FILE)
