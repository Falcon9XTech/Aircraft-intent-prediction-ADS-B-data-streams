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
   and many more (check its file)


PROCEDURES OF THE PROGRAM

-	Fetch dataset from OpenSkyNet via SSH portal to access Hadoop shell
- Filter and convert the fetched data ready for analysis
-	Feed data to set of conditions to identify aircraft flying within or out of their Airspace and flying over or under prohibited areas within London Terminal Manoeuvring Area (LTMA) or Controlled areas (CTA) -- raise an alert when a breach of Air Law occurs.
-	Further prediction using mathematical models: Bayesian Naive Network for future datasets analysed.
- Create log files for security purposes such as timestamps, program use, extracted information from data etc.


# AID Process Chart
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/AID_ProcessChart.png#gh-dark-mode-only)

# AID System flowchart
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/AID_Flowchart.png#gh-dark-mode-only)

From the above flowchart, the data is fetched automatically using terminal command lines from the Subprocess to access the terminal and retrive data as requested. This is achieved in the ```Algorithm\fetch_data.py```

The data as state_vector_data4 format is extracted and stored as a csv file.

Then, data is filtered and converted using pandas and pyproj library as shown in ```Algorithm\filter.py```.

# Visualisation of Flight routes over London Airspace
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/airways_transparent.png#gh-dark-mode-only)

Above Details: LHR Aiport coordinates 51° 28’ N, 0° 27’ W
Date: 19/03/2021 , Timeframe: 7:00 to 10:00 HRS
Total Airborne Aircraft: 95 

Data is then feed to the program for analysis. We have created two conditions that best suit our system to find and identify aircraft that infringe airspace rules. This is achieved in the ```Algorithm\conditions.py```.

# Condition 01

The aim is to search and output ```callsign```, ```icao24 address```, ```time``` and ```location``` of the aircraft that is in breach of Rules of Air Annex 02 - section 3.1.10 within the LTMA restricted areas (D132/2.5 and D104/2.4) -- this is to illustrate the search of two areas only, but would be necessary to include other restricted areas.

Below is the chart of the London Airspace and the two restricted areas as mentioned earlier.
![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/Southern-England_standard_Airspace.png#gh-dark-mode-only)

Then, data of aircraft location (Eastings, Northings) is queried to intersect the two areas (```LTMA 11A``` and ```LTMA 4A```) that are exclusively within the ``airspace_bound`` boundary and raise alerts as shown in ```Algorithm\conditions.py```.

# Time Series Prediction

Data is first sorted out in ```time``` and grouped in their ```callsign```, then the initial time and location are referenced to calculate the distance covered [m] and estimate velocity [knots] of the aircraft. This is achieved in ```Algorithm\intent_prediction.py```.

# Machine Learning using Gaussian Naive Bayes

To make prediction more accurately, it is important to implement a machine learning algorithm to be able to predict values or future outcomes. The observations are taken from columns ```airspace_bound```, ```LTMA_11_A```,```LTMA_4_A``` as features and ```C1_outcome``` as the target.

A portion of the data is set for training (70%) and the remaining (30%) is set for testing. The results are shown below; But this raises the question of overfitting when the accuracy is above (90%) that the data has been trained without considering errors.

![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/C1_Outcome.png#gh-dark-mode-only)

The classification report of the Trained Data is shown below.

![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/classification_report.png#gh-dark-mode-only)

This has to be corrected by use of K-fold cross validation, therefore part of the data is set for vaildation and the data is split into different dataset each used for training and a portion for validation, until the process is complete. The outcome of this has achieved an accuracy of about 99.95%

![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/K-fold_cross_validation.png#gh-dark-mode-only)

The decision boundary helps to classify the data (for this case, we'll show the tested data) as shown below; ```Class 0 = not_within_London_airspace```, ```Class 1 = clear```, ```Class 2 = warning_above_restricted_area```

![alt text](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/decision_boundary.png#gh-dark-mode-only)


# Condition 02

This section is still under development.




