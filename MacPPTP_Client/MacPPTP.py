import os
import sys
import signal
import subprocess
def connectToServer(username,password):
    os.system('sudo touch /etc/ppp/peers/129.108.7.159')
    # os.system('sudo echo "test input1" >> /etc/ppp/peers/129.108.7.159')
    PPTP_File=open("/etc/ppp/peers/129.108.7.159","r+")
    PPTP_TempFile=open("PPTP_ConfigTemplate.txt")
    # user=input("enter username: ")
    # password=input("enter password: ")
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
    subPro=subprocess.Popen(["pppd", "call", "129.108.7.159"],stdout=subprocess.PIPE)
    
    
    
    newpid=0
    inp="x"
    while inp!="exit":
        inp=input("\nEnter Command (Connect or Exit)->")
        sanitizedInp=inp.lower()
        validCommand=False
        if(inp==""):
            print("Enter valid command")
        elif inp != "exit":
            if sanitizedInp=="connect":
                validCommand=True

        if validCommand==True:
            newpid=os.fork()
            if newpid !=0:
                os.waitpid(newpid,0)
            if newpid==0:
                subPro=subprocess.Popen(["pppd", "call", "129.108.7.159"],stdout=subprocess.PIPE)
                # os.spawnl(os.P_NOWAIT,'pppd call 129.108.7.159')

    if inp=="exit":
        os.killpg(os.getpgid(subPro.pid), signal.SIGTERM)
        os.system('rm /etc/ppp/peers/129.108.7.159')
        os.kill(newpid,signal.SIGTERM)
        # os.system('rm /etc/ppp/peers/129.108.7.159.save')
        # print("got here")