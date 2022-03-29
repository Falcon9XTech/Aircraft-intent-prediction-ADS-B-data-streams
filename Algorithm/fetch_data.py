#!/usr/bin/env python

"""
Name: Automatic Fetch Data from OpenSky Network 
Author: Harris Hollevas
Copyright: University of Liverpool © 2021
License: MIT 
Version: 1.0
Status: Operational
Description: The source code fetches dataset from OpenSky Network at a specific location or Airspace and time interval.
"""


from socket import timeout
import subprocess
from sys import stderr
import os
import datetime
import time


class opensky():
# Define how to retrieve data from OpenSky Network
    def __init__(self, filename, USERNAME, PASSWORD):
        self.filename = filename  # Assign dataset name

        self.USERNAME = USERNAME  # used on OpenSky Network account (create a config. file to hide credentials)
        self.PASSWORD = PASSWORD  # used to login


    def flight_data(self):
        # Recall attritubes used
        self.filename

        self.USERNAME
        self.PASSWORD
        
        # Commands used in the SSH Shell Terminal
        command = [f"script {self.filename}.txt ssh -o StrictHostKeyChecking=no -p 2230 -l {self.USERNAME} data.opensky-network.org"]

        # Extended input if needed. Case study, London Heathrow Airspace (Fixed Parameters)
        self.command1 = f"select * from state_vectors_data4 where lat<={51.65} and lat>={51.25} and lon<={0.15} and lon>=-{0.85} and hour<={1616148000} and hour>={1616137200};"
         
        # Convert txt. file to csv. file       
        self.command2 = f"""cat {self.filename}.txt | grep "^|.*" | sed -e 's/\s*|\s*/,/g' -e 's/^,\|,$//g' -e 's/NULL//g' | awk '!seen[$0]++' >> {self.filename}.csv"""
        
        
        # Initiate time execution
        t = datetime.datetime.now()
        now = t.strftime("%H:%M:%S")
        
        
        print(f"\n Command submitted at {now}.")
        print("******************************")
        
        
        def send_command(process, cmd):
            time.sleep(3)
            process.stdin.write(str(cmd + "\n")) # Write the input to STDIN
            process.stdin.flush() # Run the command
            #process.wait() # until process is finished
            time.sleep(1)
        
        
        # Open Terminal and execute commands
        p = subprocess.Popen(command, bufsize=0, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        
        send_command(p, self.PASSWORD)
        send_command(p, self.command1)
       
        p.stdin.flush()
        p.wait()
        p.terminate()
        
        #send_command(p, 'terminate;')
        
        # Terminate the above process
        #p.kill()
        
        # Process to convert txt. to csv. file
        p1 = subprocess.Popen(self.command2, bufsize=0, shell=True, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        
        
           
        print("Process is complete. Data fetched and converted successfully")
        
        return opensky
           