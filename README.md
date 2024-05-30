<h1>California Department of Water Resources Ground Water Elevation (GWE)</h1>
<p>This data comes from the California Department of Water Resources: see <a href="https://water.ca.gov/">https://water.ca.gov/</a></p>
<p>Ground Water Elevation (GWE) refers to the height of the water surface in a well, measured from a specific reference point, usually from the ground surface or a predetermined datum.</p>

<h1>Overview of the Project and Its Purpose</h1>
<p>The purpose of this project is to analyze groundwater levels across California, observe variations over the years, and check the number and types of wells and distribution of their usage.</p>

<h1>The Analysis Involves:</h1>
<p>Data collection: gathering data on stations, measurements, and well perforations from the dataset provided by the California Natural Resources Agency, ensuring comprehensive coverage of wells across California;</p>
<p>Data Processing: cleaning and preprocessing the data to ensure accuracy and consistency, and handling missing values and outliers appropriately;</p>
<p>Creating a comprehensive map of groundwater elevations using data sourced from the California Natural Resources Agency's dataset on periodic groundwater level measurements;</p>
<p>Developing an interactive dashboard to explore the groundwater level measurements from various stations (sites) across California, offering valuable insights into the state's groundwater resources;</p>

<h1>Bar Charts for Visualization Purposes</h1>
<p>Creating bar charts to visually represent groundwater level data, trends, and comparisons between different regions and time periods.</p>

<h1>Instructions on How to Use and Interact with the Project</h1>
<p>Details on how users can interact with the project will be provided here.</p>

<h1>Efforts for Ethical Considerations Made in the Project</h1>
<p>In conducting the Groundwater Level Analysis across California, significant efforts were made to ensure ethical considerations were rigorously upheld throughout the research and analysis processes. Firstly, data integrity and accuracy were prioritized by using verified and reliable data from the California Natural Resources Agency. Secondly, the project adhered to principles of transparency and accountability, with methodologies and findings made accessible to the public to foster trust and facilitate independent verification.</p>

<h1>References for the Data Source(s)</h1>
<p>The data for this project is obtained from the California Natural Resources Agency's Periodic Groundwater Level Measurements dataset.</p>


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
