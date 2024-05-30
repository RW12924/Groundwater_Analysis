import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

pages = [
    {'name': 'Home', 'url': '/'},  # Working
    {'name': 'Combined Data Dictionaries', 'url': '/Combined_Data_Dictionaries'},  # Working
    {'name': 'missing_values', 'url': '/missing_values'},  # CHECK DATA!!!
    {'name': 'Well Use Graphs', 'url': '/well_use_graphs'},  # Working
    {'name': 'GWE Chart Histogram', 'url': '/GWE_Chart_Histogram'},  # Working     
    {'name': 'Dynamic Scatterplot', 'url': '/dynamic_scatter_plot'},  # Not working
    {'name': 'CDW Dashboard', 'url': '/CDW_Dashboard'}  # Working
]


db_path = os.path.join('../Resources', 'Groundwater.db')
#db_path = os.path.join('../Resources', 'Groundwater.db')

def get_db_tables():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    return [table['name'] for table in tables]

# Retrieve data from Groundwater.db
def get_well_use_counts():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT well_use, COUNT(DISTINCT site_code) as count
        FROM Stations
        WHERE well_use != 'Unknown'
        GROUP BY well_use
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

# Retrieve distinct years from Groundwater.db
def get_years():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT year
        FROM tbl_groundwater
        ORDER BY year
    ''')
    years = [row[0] for row in cursor.fetchall()]
    conn.close()
    return years

# Retrieve data for the second chart from Groundwater.db
def get_second_chart_data(year1, year2):
    conn = sqlite3.connect(db_path)  # Ensure the correct path
    query = '''
        SELECT 
            well_use, 
            CASE WHEN year= ? THEN well_use_avg_gwe_per_year END as avg_gwe_year1,
            CASE WHEN year = ? THEN well_use_avg_gwe_per_year END as avg_gwe_year2
        FROM 
            well_use_avg_gwe_per_year
        WHERE 
            well_use != 'Unknown'
    '''
    df = pd.read_sql_query(query, conn, params=(year1, year2))
    conn.close()
    return df

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

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html', pages=pages)

@app.route('/GWE_Chart_Histogram')
def GWE_Chart_Histogram():
    return render_template('GWE_Chart_Histogram.html', pages=pages)

@app.route('/CDW_Dashboard')
def CDW_Dashboard():
    return render_template('CDW_Dashboard.html', pages=pages)

@app.route('/Combined_Data_Dictionaries')
def combined_data_dictionaries():
    data_dictionary_info = data_dictionaries()
    return render_template('Combined_Data_Dictionaries.html', data_dictionary_info=data_dictionary_info, pages=pages)

@app.route('/missing_values', methods=['GET', 'POST'])
def missing_values():
    missing_percent_change_gwe = get_missing_percent_change_gwe()
    missing_Percent_well_use = get_missing_Percent_well_use()
    return render_template('missing_values.html', 
                           pages=pages,
                           missing_percent_change_gwe=str(int(missing_percent_change_gwe)) + '%', 
                           missing_Percent_well_use=str(int(missing_Percent_well_use)) + '%')

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

@app.route('/dynamic_scatter_plot', methods=['GET'])
def dynamic_scatter_plot():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    tables = [table['name'] for table in tables]
    return render_template('dynamic_scatter_plot.html', tables=tables, pages=pages)

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
    
    return jsonify({'plot_url': f'data:image/png;base64,{plot_url}'})

@app.route('/data')
def data():
    well_use_counts = get_well_use_counts()
    data = {'labels': [], 'counts': []}
    for row in well_use_counts:
        data['labels'].append(row[0])
        data['counts'].append(row[1])
    return jsonify(data)

@app.route('/second_chart_data')
def second_chart_data():
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    if not year1 or not year2:
        return jsonify({'error': 'Both year1 and year2 are required'}), 400
    df = get_second_chart_data(year1, year2)
    grouped_df = df.groupby('well_use').agg({
        'avg_gwe_year1': 'first',
        'avg_gwe_year2': 'first'
    }).reset_index()
    data = {
        'labels': grouped_df['well_use'].tolist(),
        'avg_gwe_year1': grouped_df['avg_gwe_year1'].fillna(0).tolist(),
        'avg_gwe_year2': grouped_df['avg_gwe_year2'].fillna(0).tolist()
    }
    return jsonify(data)

@app.route('/well_use_graphs')
def well_use_graphs():
    years = get_years()
    return render_template('well_use_graphs.html', pages=pages, years=years)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', pages=pages), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
