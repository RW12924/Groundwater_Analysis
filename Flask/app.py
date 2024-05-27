import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os
from flask import Flask, render_template, request

app = Flask(__name__)

pages = [
    {'name': 'Home', 'url': '/'},
    {'name': 'scatter_plot_avg_percent', 'url': '/Scatter_Plot_Average_Percent'},
    {'name': 'Scatter Plot Query Groundwater View', 'url': '/Scatter_Plot_Groundwater_View_page'},
    {'name': 'Data_Overview', 'url': '/Data_Overview'},
    {'name': 'missing_values', 'url': '/missing_values'},
    {'name': 'Dynamic Scatterplot', 'url': '/generate_scatterplot'},
    {'name': 'Groundwater Maps', 'url': '/JavaScript'},
    {'name': 'Combined_Data_Dictionaries', 'url': '/Combined_Data_Dictionaries'}
]

db_path = os.path.join('Resources', 'Groundwater.db')
#db_path = os.path.join('../Resources', 'Groundwater.db')

def get_measurements_gwe_avg_percent_change_table():
    query = "SELECT * FROM measurements_gwe_avg_percent_change_table"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_missing_Percent_well_use():
    query_well_use = "SELECT well_use, COUNT(*) FROM measurements_gwe_avg_percent_change_table GROUP BY well_use"
    table_total = "SELECT COUNT (*) FROM measurements_gwe_avg_percent_change_table"
 
    conn = sqlite3.connect(db_path)
    query_well_use = pd.read_sql_query(query_well_use, conn)

    table_total = pd.read_sql_query(table_total, conn)
    table_total = int(table_total.iloc[0, 0])
    unknown_well_use = query_well_use[query_well_use['well_use'] == 'Unknown']
    unknown_well_use = int(unknown_well_use.iloc[0, 1])
    unknown_well_use_percent = round(unknown_well_use/table_total, 2)*100
    conn.close()
    return unknown_well_use_percent

def get_missing_percent_change_gwe():
    query_missing = "SELECT COUNT(*) FROM measurements_gwe_avg_percent_change_table WHERE percent_change_gwe IS NULL OR percent_change_gwe = 'NaN';"
    query_total = "SELECT COUNT (*) FROM measurements_gwe_avg_percent_change_table"   
    conn = sqlite3.connect(db_path)
    percent_change_gwe_missing = pd.read_sql_query(query_missing, conn)
    table_total = pd.read_sql_query(query_total, conn)
    percent_change_gwe_missing = int(percent_change_gwe_missing.iloc[0, 0])
    table_total = int(table_total.iloc[0, 0])
    percent_change_gwe_percent_missing = round((percent_change_gwe_missing/table_total)*100, 2)
    percent_change_gwe_percent_missing
    conn.close()
   
    return percent_change_gwe_percent_missing

def query_vw_groundwater():
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM vw_groundwater"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_tbl_groundwater():
    conn = sqlite3.connect('../Resources/Groundwater_Maps.db')
    query = "SELECT * FROM tbl_groundwater WHERE year > 2013"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def data_dictionaries():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Combined_Data_Dictionaries ORDER BY tables;")
    data_dictionary_info = cursor.fetchall()
    # Convert the result into a list of dictionaries
    data_dictionary_info = [dict(zip([column[0] for column in cursor.description], row)) for row in data_dictionary_info]
    cursor.close()
    conn.close()
    return data_dictionary_info

@app.route('/')
def index():
    return render_template('index.html', pages=pages)

@app.route('/JavaScript')
def JavaScript():
    # Query the data from the database instead of reading from CSV
    #df = query_vw_groundwater()
    df = query_tbl_groundwater()
    # Extract the year for each object from the DataFrame
    years = df['year']
    # Return the HTML template with the years parameter
    return render_template('JavaScript.html', years=years)

@app.route('/data')
def data():
    try:
        # Query the data from the database
        df = query_vw_groundwater()
        # Convert the DataFrame to a CSV string
        csv_data = df.to_csv(index=False)
        # Return the CSV data as a response
        return csv_data, 200, {'Content-Type': 'text/csv'}
    except Exception as e:
        app.logger.error(f"Error fetching data: {e}")
        return "Error fetching data", 500

@app.route('/Data_Overview')
def Data_Overview():
    return render_template('Data_Overview.html', pages=pages)

@app.route('/Combined_Data_Dictionaries')
def combined_data_dictionaries():
    data_dictionary_info = data_dictionaries()  # Assuming you have a function to fetch data
    if isinstance(data_dictionary_info, tuple):
        # Assuming the first item of the tuple is the actual data you want
        data_dictionary_info = data_dictionary_info[0]
    return render_template('Combined_Data_Dictionaries.html', data_dictionary_info=data_dictionary_info, pages=pages)

@app.route('/Scatter_Plot_Average_Percent', methods=['GET', 'POST'])
def scatter_plot_page():
    plot_url = None
    x_column_name = None
    y_column_name = None
    if request.method == 'POST':
        x_column_name = request.form.get('x_column')
        y_column_name = request.form.get('y_column')
        
        if not x_column_name or not y_column_name:
            return "Error: Both columns must be specified.", 400
        
        plot_data = get_measurements_gwe_avg_percent_change_table()
        
        if x_column_name not in plot_data.columns or y_column_name not in plot_data.columns:
            return "Error: Specified columns not found in the data.", 400

        x_data = plot_data[x_column_name]
        y_data = plot_data[y_column_name]

        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data)
        plt.xlabel(x_column_name)
        plt.ylabel(y_column_name)
        plt.title(f'Scatter Plot of {x_column_name} vs {y_column_name}')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()

    return render_template('Scatter_Plot_Average_Percent.html', plot=plot_url, x_column=x_column_name, y_column=y_column_name, pages=pages)

@app.route('/Scatter_Plot_Groundwater_View_page', methods=['GET', 'POST'])
def Scatter_Plot_Groundwater_View_page():
    plot_url = None
    x_column_name = None
    y_column_name = None
    if request.method == 'POST':
        x_column_name = request.form.get('x_column')
        y_column_name = request.form.get('y_column')
        
        if not x_column_name or not y_column_name:
            return "Error: Both columns must be specified.", 400
        
        plot_data = query_vw_groundwater()
        
        if x_column_name not in plot_data.columns or y_column_name not in plot_data.columns:
            return "Error: Specified columns not found in the data.", 400

        x_data = plot_data[x_column_name]
        y_data = plot_data[y_column_name]

        plt.figure(figsize=(10, 6))
        plt.scatter(x_data, y_data)
        plt.xlabel(x_column_name)
        plt.ylabel(y_column_name)
        plt.title(f'Scatter Plot of {x_column_name} vs {y_column_name}')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()

    return render_template('Scatter_Plot_Groundwater_View.html', plot=plot_url, x_column=x_column_name, y_column=y_column_name, pages=pages)


@app.route('/missing_values', methods=['GET', 'POST'])
def missing_values():
    # Assuming these functions return the values you want to pass to the template
    missing_percent_change_gwe = get_missing_percent_change_gwe()
    missing_Percent_well_use = get_missing_Percent_well_use()
    
    # Pass the values to the template
    return render_template('missing_values.html', 
                           missing_percent_change_gwe=str(int(missing_percent_change_gwe)) + '%', 
                           missing_Percent_well_use = str(int(missing_Percent_well_use)) + '%')


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/groundwater_scatter_plot')
def groundwater_scatter_plot():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    tables = [table['name'] for table in tables]
    return render_template('scatter_plot.html', tables=tables)

@app.route('/get_columns', methods=['POST'])
def get_columns():
    table = request.form['table']
    conn = get_db_connection()
    columns = conn.execute(f"PRAGMA table_info({table});").fetchall()
    conn.close()
    columns = [column['name'] for column in columns]
    return jsonify(columns)

@app.route('/generate_scatterplot', methods=['POST'])
def generate_scatterplot():
    table = request.form['table']
    column1 = request.form['column1']
    column2 = request.form['column2']
    
    conn = get_db_connection()
    data = conn.execute(f"SELECT {column1}, {column2} FROM {table}").fetchall()
    conn.close()
    
    x = [row[column1] for row in data]
    y = [row[column2] for row in data]
    
    plt.figure()
    plt.scatter(x, y)
    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.title(f'Scatter Plot of {column1} vs {column2}')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return render_template('scatter_plot.html', plot_url=plot_url, tables=get_db_tables())

def get_db_tables():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    return [table['name'] for table in tables]


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', pages=pages), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)