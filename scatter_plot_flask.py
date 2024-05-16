##############################MUST RUN FIRST!!!!#################################
#set PYTHONPATH=C:\Users\jerry\Programming\Graphs-Charts\Library;%PYTHONPATH%
########################################################

#################Import Dependencies#########################
from flask import Flask, render_template, request
from scatter_plot_module import scatter_plot
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import sys
import os
from scatter_plot_module import scatter_plot

#################App#########################
app = Flask(__name__)

#################Site Urls########################
pages = [
    {'name': 'Home', 'url': '/'},
    {'name': 'scatter_plot', 'url': '/scatter_plot'}
]

####################Routes########################

#index
@app.route('/')
def index():
    return render_template('index.html', pages=pages)  

#404 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', pages=pages), 404


####################scatter_plot########################
@app.route('/scatter_plot', methods=['GET', 'POST'])
def scatter_plot_page():
    if request.method == 'POST':
        x_column_name = request.form.get('x_column')  # Get input from form
        y_column_name = request.form.get('y_column')  # Get input from form
        
        if not x_column_name or not y_column_name:
            # If form fields are empty, return an error message
            return "Error: Both columns must be specified.", 400
        
        db_path = os.path.join('Resources', 'Groundwater.db')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = "SELECT * FROM vw_groundwater"
        plot_data = pd.read_sql_query(query, connection)
        connection.close()
        
        I need help between here and the return command

        Use plot_data as the data to plot
        Use only x_column and y_column columns
        plot x_column and y_column in a scatter plot, show in the return command below

        return render_template('scatter_plot.html', plot=plot_data, x_column=x_column_name, y_column=y_column_name)

    # In case of GET request or initial page load
    return render_template('scatter_plot.html', plot=None)
    
####################Name App########################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Enable debug mode directly in app.run()