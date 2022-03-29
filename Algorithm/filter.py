#!/usr/bin/env python

"""
Name: Filter and Convert Fetched Data from OpenSky Network 
Author: Harris Hollevas
Copyright: University of Liverpool © 2021
License: MIT 
Version: 1.0
Status: Operational
Description: The source code performs a filter and conversion of data ready for analysis.
"""

import sys, csv, pytz
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import time
import numpy as np
import pyproj

import fileinput

root = tk.Tk()
root.withdraw()
v = tk.StringVar(root)

class data():
    
    def filter():

        file_path = filedialog.askopenfilename()

        v.set(file_path)

        rows = []
        with open(file_path, 'r') as f:
            for row in csv.reader(f):
            # Check each row then strip whitespaces and blanks
                row = [col.strip() for col in row]
                rows.append(row) 
           
        df = pd.DataFrame(rows)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.drop(df.columns[[10, 13, 14, 15]], axis = 1, inplace=False)
        df = df.drop_duplicates(keep=False)
        df = df.set_index('time', inplace=False)
        df.to_csv('test01.csv')
        
        df = pd.read_csv('test01.csv')
        df = df[df['onground'] == False]
        df = df[df['alert'] == False]
        df = df[df['baroaltitude'] >= 2590]
        #df['time'] = pd.to_datetime(df['time'],unit='s').dt.time
        df['hour'] = pd.to_datetime(df['hour'],unit='s')
        df = df.set_index('time', inplace=False)
        df.to_csv('test01.csv')
        
        filter_msg = print("\n Noise Data is removed successfully")
        
        return filter_msg
        
    def convert():
        
        # Load the data and convert lat/lon to Eastings/Northings (UK zone 30)
        df = pd.read_csv('test01.csv')
        p = pyproj.Proj(proj='utm', zone=30, ellps='WGS84', preserve_units=False)
        x,y = p(df["lon"].values, df["lat"].values)
        
        # Create columns for x and y and store the generated data
        df = df.assign(eastings = x, northings = y)
        
        # Convert velocity from [m/s] to [knots], vertical speed to [FT/s] and altitude from [m] to [FT]
        df['velocity'] = round(df['velocity']*1.943844)
        df['vertrate'] = round(df['vertrate']/0.3048)
        df['baroaltitude'] = round(df['baroaltitude']*3.28084)
        
        
        df['heading'] = round(df['heading']) # get constant values for direction
        df['icao24'] = df['icao24'].str.upper()
        
        # Classifying in their Airspace classes
        conditions = [
                (18050 <= df['baroaltitude']) & (df['baroaltitude'] <= 60000), # Class A 
                (8550 <= df['baroaltitude']) & (df['baroaltitude'] <= 18000), # Class C
                (8500 <= df['baroaltitude']) & (df['baroaltitude'] <= 12500), # Class E
                ]
        
        classes = ['Class A', 'Class C', 'Class E']
        
        df['airspace'] = np.select(conditions, classes)
        
        df = df.set_index('time', inplace=False)
        df = df.sort_index()
        df.to_csv('test01.csv') # save the file
        
        # Load data to save flights as their callsign in seperate csv. files
        df = pd.read_csv('test01.csv')
        incl = df['callsign']

        for callsign, g in df[df['callsign'].isin(incl)].groupby('callsign'):
            g = g.set_index('callsign', inplace=False)
            g = g.sort_index()
            g.to_csv(f'/Users/harrishollevas/Desktop/YEAR3/FYP/main/flight_data/{callsign}.csv')
        
        convert_msg = print("\n Data Conversion complete \n")
        
        return convert_msg
    
    
    
# data.filter()
# data.convert()