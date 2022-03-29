#!/usr/bin/env python

"""
Name: Intent Prediction for Airspace Infringement Detection
Author: Harris Hollevas
Copyright: University of Liverpool © 2021
License: MIT 
Version: 1.0
Status: Development
Description: The source code predicts and estimate velocities of airborne aircraft and their distance covered. 
             It also trains the data to predict future outcomes for condition 01 and 02
"""


import itertools
import datetime
import pandas as pd
import numpy as np
import geopandas as gpd

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from shapely.geometry import Point
from math import sqrt
# from time import time


class prediction:
    
    def time_series():

        # Load data for processing
        df = pd.read_csv("/Users/harrishollevas/Desktop/YEAR3/FYP/main/test01.csv", index_col=None)


        df = df.sort_values(by=['callsign', 'time'])

        df['intial_easting'] = (df.groupby(df['callsign'].fillna(0))['eastings'].transform(lambda x: x.iat[0]))
        df['intial_northing'] = (df.groupby(df['callsign'].fillna(0))['northings'].transform(lambda x: x.iat[0]))
        df['dtime'] = (df.groupby(df['callsign'].fillna(0))['time'].transform(lambda x: x.iat[0]))


        def UTM_Distance(east1,north1,east2,north2):
            
            Dist=sqrt((east1 - east2)**2 + (north1 - north2)**2) # [m]
            
            return Dist

        def velocity(distance, time_start, time_end):
            """Return 0 if time_start == time_end, avoid dividing by 0; V = [m/s] """
            
            veloc = distance / (time_end - time_start)if time_end > time_start else 0
            
            return veloc



        df['distance'] = df.apply(
            lambda row: UTM_Distance(
                east1=row['eastings'],
                north1=row['northings'],
                east2=row['initial_easting'],
                north2=row['initial_northing']
            ),
            axis=1
        )

        df['estimated_velocity'] = df.apply(
            lambda row: velocity(
                distance=row['distance'],
                time_start=row['dtime'],
                time_end=row['time']
            ),
            axis=1
        )

        # Change Estimated velocity [m/s] to [knots]
        df['estimated_velocity'] = round(df['estimated_velocity']*1.943844)

        
        
        

        df.to_csv("test01.csv")
    
        
    def machine_learning():
        
        # Load data for processing
        df = pd.read_csv("/Users/harrishollevas/Desktop/YEAR3/FYP/main/test01.csv", index_col=None)
        
        # Extract the features and target
        features = df.iloc[:, 16:19]
        print(features)
        target = df.iloc[:, -1]
        print(target)
        
        # Create model with no calibration
        algorithm = GaussianNB()
        
        # Make a train/test split using 30% test size
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size = 0.3)
        y_pred = algorithm.fit(X_train, y_train).predict(X_test)
        
        print(f'The predictions are: {y_pred} \n')
        
        print(f'The length of tested data: {len(y_pred)} \n')
        
        score = algorithm.score(X_test, y_test)
        
        print('The Gaussian Model Has Achieved %.1f%% Accuracy \n'%(score*100))
        
        # Validation of data to correct the overfitting (K-fold Validation)
        kfold = model_selection.KFold(n_splits=10)
        
        results_kfold = model_selection.cross_val_score(algorithm, features, target, cv=kfold)
        
        print("Model Accuracy after Validation: %.2f%% \n" % (results_kfold.mean()*100.0)) 
        
        
        
        # Predict on new data
        # y_new = algorithm.predict(Xnew)
     
    def test():
        
        # New instances where the answers are not provided
          
        
        
        return prediction



prediction.machine_learning()






    