import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import sys
import os
from flask import Flask, render_template, request

#################App#########################
app = Flask(__name__)

#################Site Urls########################
pages = [
    {'name': 'Home', 'url': '/'},
    {'name': 'scatter_plot', 'url': '/scatter_plot'}
]

####################Routes########################

# Query Data
def query_data():
    db_path = os.path.join('Resources', 'Groundwater.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    query = "SELECT * FROM vw_groundwater"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

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
        
        plot_data = query_data()

        # Extract specified columns for plotting
        x_data = plot_data[x_column_name]
        y_data = plot_data[y_column_name]

        # Create scatter plot
        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data)
        plt.xlabel(x_column_name)
        plt.ylabel(y_column_name)
        plt.title(f'Scatter Plot of {x_column_name} vs {y_column_name}')
        
        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()

        # Pass the image to the template
        return render_template('scatter_plot.html', plot=plot_url, x_column=x_column_name, y_column=y_column_name)

    # In case of GET request or initial page load
    return render_template('scatter_plot.html', plot=None)

####################Name App########################
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Enable debug mode directly in app.run()
