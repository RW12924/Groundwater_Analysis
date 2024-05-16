# Folder Structure
### Root
##### Groundwater_ETL.ipynb - ETL script that takes in groundwater data and sends to the SQLite database
##### scatter_plot_flask.py - example flask web server using python script.
##### text.py - example flask web server using python script.
##### testdata.csv - test data on longitute and lattitude.
### Exploratory Analysis and Graphs
###### Groundwater Statistics and Graphs.ipynb.ipynb - contains graphs and summary statistics on the groundwarter data
### Metadata
##### DataDictionary_measurements.csv - data dictionary on groundwater measurements.
##### DataDictionary_perforations.csv - data dictionary on groundwater perforations.
##### DataDictionary_stations.csv - data dictionary on groundwater stations.
##### Metadata.ipynb - currently has the metadata from all three Data Dictionaries noted above.
##### Groundwater Metadata.drawio - contains documentation on the ERD, ETL, 
##### High-Level Groundwater Metadata.txt
##### QuickDBD-export.sql - SQL of QuickDBD ERD.
##### QuickDBD-export.svg - image of QuickDBD ERD.
### Resources
##### Groudwater.db - SQLLite database containing Groundwater tables and views
##### measurements - csv file with measurment Data
##### perforations - csv file with preforations Data
##### stations - csv file with station data
##### groundwater_data.csv - contains data for all three mreged tables (measurements, stations and perforations).
### Templates
##### 404.html - contains the 404 page if the use enters a web page that does not exit
##### index.html - the homepage
#### scatter_plot.html - contains a scatter plot that takes in two columns and produces a graph