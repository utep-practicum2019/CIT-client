import subprocess
import sys
import time

# Function to add a VPN to address book.
def addConnectionProcess(name, serverIP):
    process=subprocess.Popen(["powershell","Add-VpnConnection -Name %s -ServerAddress %s -PassThru -TunnelType Pptp" % (name, serverIP)], stdout=subprocess.PIPE);
    result=process.communicate()[0]
    #sys.stdout.write(str(result.decode("utf-8")))
    print("VPN %s created successfully" % name)

# Function to remove a VPN to address book.
def removeConnProcess(name):
    process = subprocess.Popen(["powershell", "Remove-VpnConnection -Name %s -Force -PassThru " % name], stdout=subprocess.PIPE);
    result = process.communicate()[0]
    #sys.stdout.write(str(result.decode("utf-8")))
    print("VPN %s removed successfully" % name)

# Function to list all VPN connections.
def getAllConnProcess():
    process = subprocess.Popen(["powershell", "(Get-VpnConnection)"], stdout=subprocess.PIPE);
    result = process.communicate()[0]
    sys.stdout.write(str(result.decode("utf-8")))

# Function to list a single VPN connection.
def getConnProcess(name):
    process = subprocess.Popen(["powershell", "(Get-VpnConnection -Name %s)" % name], stdout=subprocess.PIPE);
    result = process.communicate()[0]
    sys.stdout.write(str(result.decode("utf-8")))

# Function to return the status of a single VPN connection. Possible values: Connected, Disconnected.
def getConnStatus(name):
    process = subprocess.Popen(["powershell", "(Get-VpnConnection -Name %s).ConnectionStatus" % name], stdout=subprocess.PIPE);
    result = process.communicate()[0]
    #sys.stdout.write(str(result.decode("utf-8")))
    return str(result.decode("utf-8").strip())


# Function to check and return the existence of a VPN.
def doesExist(name):
    if str(getConnStatus(name)) == "Connected" or str(getConnStatus(name)) == "Disconnected":
        return True
    else:
        return False


# Function to establish a VPN connection.
def connVPN(name, username, password):
    if doesExist(name) == False:
        print("error this connection does not exist.")
        exit(1)
    process = subprocess.Popen(["powershell", "rasdial %s %s %s" % (name, username, password)],
                               stdout=subprocess.PIPE);


# Function to disconnect from a VPN.
def disconnVPN(name):
    if doesExist(name) == False:
        print("error this connection does not exist.")
        exit(1)
    process = subprocess.Popen(["powershell", "rasdial %s /DISCONNECT" % name],
                               stdout=subprocess.PIPE);


# Function to establish create and connect to a VPN.
def createVPNConnection(name, username, password, serverIP):
    if doesExist(name):
        removeConnProcess(name)

    addConnectionProcess(name, serverIP)

    connVPN(name, username, password)

    time.sleep(5)

    if getConnStatus(name) == "Connected":
        print("Connection Successful")
    else:
        print("Connection Failed")


# Function to disconnect and remove a VPN.
def removeConnection(name):
    if doesExist(name) == False:
        print("No VPN to destroy.")
        exit(1)
    if getConnStatus(name) == "Connected":
        disconnVPN(name)
        time.sleep(5)
    removeConnProcess(name)
    print("VPN removed.")

createVPNConnection("citclient", "test3", "test3", "192.168.197.3")
removeConnection("citclient")
