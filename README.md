![alt text](https://aspenavionics.com/images/uploads/products/asdb_icon_homepage_03.png)
# Aircraft intent prediction using ADS-B data streams
The code developed is to identify way points of an aircraft with its position, velocity, identity and other associated information to predict an aircraft's intent that infringes airspace rules with dataset analysed from OpenSky Network (open source)

The aim is to analyse and predict unauthorised flight patterns of airborne aircraft within a controlled airspace (e.g., London Heathrow Airport) using ADS-B data that is broadcasted from the aircraft. The developed system is named as Airspace Infringement Detection (AID) System

To run the program, it is recommended to download Python3.6 or above and have its dependencies listed in the ```requirements.txt``` file installed. It is also recommended to run the program on a macOS platform since the code base is developed under it.

Requirements:

- pandas
- geopandas
- numpy
- sklearn
- math
- shapely
- pyproj
   many more (check its file)


PROCEDURES OF THE PROGRAM

-	Fetch dataset from OpenSkyNet via SSH portal to access Hadoop shell
- Filter and convert the fetched data ready for analysis
-	Feed data to set of conditions to identify aircraft flying within or out of their Airspace and flying over or under prohibited areas within London Terminal Manoeuvring Airspace (LTMA) or Controlled zones (CTA) ¬¨- raise an alert when a breach of Air Law.
-	Further prediction using mathematical models: Bayesian Naive Network for future datasets analysed.
- Create log files for security purposes such as timestamps, program use, extracted information from data etc.


# AID Process Chart
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/AID_ProcessChart.png#gh-dark-mode-only)

# AID System flowchart
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/AID_Flowchart.png#gh-dark-mode-only)

From the above flowchart, the data is fetched automatically using terminal command lines from the Subprocess to access the terminal and retrive data as requested. This is achieved in the ```fetch_data.py```

The data as state_vector_data4 format is extracted and stored as a csv file.

Then, data is filtered and converted using pandas and pyproj library as shown in ```filter.py```

# Visualisation of Flight routes over London Airspace
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/airways_transparent.png#gh-dark-mode-only)


Data is then feed to the program for analysis. We have created two conditions that best suit our system to find and identify aircraft that infringe airspace rules. This is achieved in the ```conditions.py``` file

# Condition 01

The aim is to search and output ```callsign```, ```icao24 address```, ```time``` and ```location``` of the aircraft that is in breach of Rules of Air Annex 02 - section 3.1.10 within the LTMA restricted areas (D132/2.5 and D104/2.4) -- this is to illustrate the search of two areas only, but would be necessary to include other restricted areas.

Below is the chart of the London Airspace and the two restricted areas as mentioned earlier.
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/Southern-England_standard_Airspace.png#gh-dark-mode-only)






