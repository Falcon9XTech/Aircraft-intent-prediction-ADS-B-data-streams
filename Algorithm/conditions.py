#!/usr/bin/env python

"""
Name: Conditons for Airspace Infringement Detection
Author: Harris Hollevas
Copyright: University of Liverpool © 2021
License: MIT 
Version: 1.0
Status: Development
Description: The source code performs checks on data to classify it for any breach in Air Law (Rules of Air Annex 02).
"""


import math
from time import time
import numpy as np
import pandas as pd
import geopandas as gpd
import shapely as sp
from shapely.ops import transform
import shapely.ops as so
from shapely.geometry import Point, LineString
from  pyproj import Proj
import glob
from conversion import *



class airspace_infringement():
    
    def __init__(self, icao24, callsign, aircraft, location, breach):
        
        self.icao24 = icao24
        self.callsign = callsign
        self.aircraft = aircraft
        self.location = location
        self.breach = breach
        
    def airspace_bound(self, lat1, lon1, lat2, lon2, lat3, lon3, lat4, lon4):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.lat3 = lat3
        self.lon3 = lon3
        self.lat4 = lat4
        self.lon4 = lon4
    
    # Condition 01 
    def restricted_zones(): 
        
        
        # Create an enclosed boundary to represent area of focus - LHR Airspace
        outer_boundary = [[x1[0], x1[1]], [x2[0], x2[1]], [y1[0], y1[1]], [y2[0], y2[1]]]
        
        #inner_boundaries as classified in London Terminal Manurvoe Airspace (LTMA) or Controlled zones (CTR) - (Polygon or/and Circle shaped)
        
        ltma_D104 = ltma_bound
                        # and so on ...
        
        ltma2 = [[a1[0], a1[1]], [a2[0], a2[1]], [b1[0], b1[1]], [b2[0], b2[1]], [c1[0], c1[1]], [c2[0], c2[1]]]
                                                                                                                # and so on ...
        
        
        # Put coordinates in array
        airspace_bound = np.array(outer_boundary)
        
        ltma_D132 = np.array(ltma2)
        
        
        
        # Load data for processing
        df = pd.read_csv("/Users/harrishollevas/Desktop/YEAR3/FYP/main/test01.csv")

            
        grouped_data = df.groupby("callsign")
        
        # Identify aircraft flying over London Heathrow airspace
        identify = grouped_data.apply(list)
        print('\n Airborne Aircraft: ' , identify.count())
        print("\n")
        
        
        # Pull values from data
        eastings = df['eastings'].values
        northings = df['northings'].values
        
        
        ### Condition 01 - Find aircraft flying within restricted areas [EDIT] ####
        
         # Load into dataframe
        rect_bound = pd.DataFrame({'id':range(len(airspace_bound)),
                          'eastings':airspace_bound[ : , 0],
                          'northings':airspace_bound[ : , 1]})
        
        poly_bound = pd.DataFrame({'id':range(len(ltma_D132)),
                          'eastings':ltma_D132[ : , 0],
                          'northings':ltma_D132[ : , 1]})
        
       
       # points from data loaded
        df_points = pd.DataFrame({'id':range(len(df)),
                          'eastings':eastings,
                          'northings':northings})
        
        
                # Creating a GeoDataFrame for the points to be queried
        gdf_points = gpd.GeoDataFrame(df_points, 
                              crs='epsg:2395',
                              geometry=gpd.points_from_xy(df_points['eastings'], df_points['northings']))
            

                # Creating a GeoDataFrame for the points on the rect and polygon to use as a reference
        gdf_rect = gpd.GeoDataFrame(rect_bound, 
                              crs='epsg:2395',
                              geometry=gpd.points_from_xy(rect_bound['eastings'], rect_bound['northings']))
        
        gdf_poly = gpd.GeoDataFrame(poly_bound, 
                              crs='epsg:2395',
                              geometry=gpd.points_from_xy(poly_bound['eastings'], poly_bound['northings']))
        
        
        # Generating a shapely geometry from the sequence of Polygon and Rectangle Points
        rect_shape = sp.geometry.Polygon(gdf_rect['geometry'])
        
        poly_shape = sp.geometry.Polygon(gdf_poly['geometry'])
        
        # new_shape= so.unary_union([rect_shape, poly_shape])
        # gpd.GeoSeries(new_shape).plot()
        # plt.show()
        
        # Querying which points are actually within the Circle and Rectangle geometry
        gdf_points['Airspace bound'] = gdf_points.intersects(rect_shape)
        gdf_points['LTMA 4A'] = gdf_points.intersects(poly_shape)
        gdf_points['LTMA 11A'] = gdf_points.within(ltma_D104)
        
        
        # circ_points = print(gdf_points['LTMA 11A'])
        # points = print(gdf_points['Airspace bound'])
        # poly_points = print(gdf_points['LTMA 4A'])
        
        # df = pd.DataFrame(df)
        df = df.assign(airspace_bound = gdf_points['Airspace bound'], LTMA_4_A = gdf_points['LTMA 4A'], LTMA_11_A = gdf_points['LTMA 11A'])
        
        
        # Conditions for breach in Air Law
        
        violation01 = (df['airspace_bound'] == True) & (df['LTMA_4_A'] == True) & (df['LTMA_11_A'] == False) & (df['baroaltitude'] < 2500)
        violation02 = (df['airspace_bound'] == True) & (df['LTMA_4_A'] == False) & (df['LTMA_11_A'] == True) & (df['baroaltitude'] < 2400)
        
        warning01 = (df['airspace_bound'] == True) & (df['LTMA_4_A'] == True) & (df['LTMA_11_A'] == False)
        warning02 = (df['airspace_bound'] == True) & (df['LTMA_4_A'] == False) & (df['LTMA_11_A'] == True)
        
        safe = (df['airspace_bound'] == True) & (df['LTMA_4_A'] == False) & (df['LTMA_11_A'] == False)
        
        out = (df['airspace_bound'] == False) & (df['LTMA_4_A'] == False) & (df['LTMA_11_A'] == False)
        UFo = (df['airspace_bound'] == True) & (df['LTMA_4_A'] == True) & (df['LTMA_11_A'] == True) 
        
        
        
        df.loc[violation01, 'C1_outcome'] = 'Aircraft flying under a restricted area (D132/2.5) - In breach of ICAO Rules of Air Annex 02 (section 3.1.10)'
        df.loc[violation02, 'C1_outcome'] = 'Aircraft flying under a restricted area (R104/2.4) - In breach of ICAO Rules of Air Annex 02 (section 3.1.10)'
        
        df.loc[warning01, 'C1_outcome'] = 'Warning Alert - Aircraft flying above a restricted area - D132/2.5'
        df.loc[warning02, 'C1_outcome'] = 'Warning Alert - Aircraft flying above a restricted area - D104/2.4'
        df.loc[safe, 'C1_outcome'] = 'Clear'
        
        df.loc[out, 'C1_outcome'] = 'Not within the London Airspace'
        df.loc[UFo, 'C1_outcome'] = 'This is an Unidentified Flying Object (UFO)'

        df = df.sort_values(by=['callsign', 'time'])
      
        df.to_csv('test01.csv', index=False)
        
        
        return df
    
    
    # Condition 02
    def airspace_class():
        
        # Controlled Airspace classes A, C, E (in FT)
        # class_A = between(18050, 60000)
        # class_C = between(0, 18000) #radius from airport
        # class_E = between(8500, 12500) #radius from airport
        
        
        # Load data for processing
        df = pd.read_csv("/Users/harrishollevas/Desktop/YEAR3/FYP/main/test01.csv")
        
        airspace = df.groupby("callsign")["airspace"]
        vertrate = df.groupby("callsign")["vertrate"]
    
        
        #df = pd.DataFrame(data)
        classes = frozenset({"Class A", "Class C", "Class E"})
        
        level = range(-2, 2)
        
        for airspaceClass in airspace:
            for Class in classes:
                if (airspace.str.contains(classes)) & (vertrate == level):
                    df.loc['C2_outcome'] = 'Not flying within their Airspace class'
                    
                    
                    
                
                
            
        
        # x = df["icao24"]
        # y = grouped_data["icao24"].apply(list)
        
        # Condition 02 - Find aircraft flying outside their airspace
        # for aircraft in df["baroaltitude"]:
            
            #a = grouped_data["baroaltitude"] in class_A
            #b = grouped_data["vertrate"] == 0
         
         
         
         
         
            
        # airspace_classes = []
        # for i in grouped_data['baroaltitude']:
        #     if 18050 <= i <= 60000:
        #         airspace_classes.append('Class A')
        #     elif 8550 <= i <= 18000:
        #         airspace_classes.append('Class C')
        #     elif 8500 <= i <= 12500:
        #         airspace_classes.append('Class E')
        #     else:
        #         airspace_classes.append('Not within controlled airspace') 
                
                
        #print(airspace_classes)
        # d = pd.DataFrame(airspace_classes)
        # d.to_csv("test02.csv")
            
        
         
        
        
    # return airspace_infringement
    

# airspace_infringement.restricted_zones()

# airspace_infringement.airspace_class()