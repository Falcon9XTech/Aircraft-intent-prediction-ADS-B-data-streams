![alt text](https://aspenavionics.com/images/uploads/products/asdb_icon_homepage_03.png)
# Aircraft intent prediction using ADS-B data streams
The code developed is to identify way points of an aircraft with its position, velocity, identity and other associated information to predict an aircraft's intent that infringes airspace rules with dataset analysed from OpenSky Network (open source)

The aim is to analyse and predict unauthorised flight patterns of airborne aircraft within a controlled airspace (e.g., London Heathrow Airport) using ADS-B data that is broadcasted from the aircraft. The developed system is named as Airspace Infringement Detection (AID) System

To run the program, it is recommended to download Python3.6 or above and have its dependencies listed in the requirements.txt file installed. It is also recommended to run the program on a macOS platform since the code base is developed under it.

Requirements:

- pandas
- geopandas
- numpy
- sklearn
- math
- shapely
- pyproj
- many more (check its file)


PROCEDURES OF THE PROGRAM

-	Fetch dataset from OpenSkyNet via SSH portal to access Hadoop shell
- Filter and convert the fetched data ready for analysis
-	Feed data to set of conditions to identify aircraft flying within or out of their Airspace and flying over or under prohibited areas within London Terminal Manoeuvring Airspace (LTMA) or Controlled zones (CTA) ¬¨- raise an alert when a breach of Air Law.
-	Further prediction using mathematical models: Bayesian Naive Network for future datasets analysed.
- Create log files for security purposes such as timestamps, program use, extracted information from data etc.


AID System flowchart
![image](https://github.com/Falcon9XTech/Aircraft-intent-prediction-ADS-B-data-streams/blob/main/Misc/AID_Flowchart.png) {width=800 height=800}

