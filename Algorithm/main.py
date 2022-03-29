#!/usr/bin/env python

"""
Name: Main program for AID system 
Author: Harris Hollevas
Copyright: University of Liverpool © 2021
License: MIT 
Version: 1.0
Status: Development
Description: The source code calls all functions and methods derived from other python files to run as one.
"""

from fetch_data import *
from filter import *
from conditions import *
from intent_prediction import *
import appearance as apr
from configparser import ConfigParser


# Project Logo
print(apr.banner())

# Load credentials to log in OpenSky Network
config = ConfigParser()
config.read("credentials.cfg")

USERNAME, PASSWORD = config["Credentials"]["USERNAME"], config["Credentials"]["PASSWORD"]


filename = "flight_data" # input("Create filename for flight data: ")

p = opensky(filename, USERNAME, PASSWORD)

# Fetch Data
fetch = p.flight_data()

fetch

# Filter Data
filter = data.filter()

# Convert Data
convert = data.convert()

#Conditions
C1_outcome = airspace_infringement.airspace_class()

# Intent Prediction
time_series = prediction.time_series()
predict = prediction.machine_learning()
