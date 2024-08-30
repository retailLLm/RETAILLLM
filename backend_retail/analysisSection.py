import pandas as pd
from flask import Flask, send_file, jsonify
import os
import matplotlib.pyplot as plt
import seaborn as sns
from flask_cors import CORS
from statsmodels.tsa.seasonal import seasonal_decompose

app = Flask(_name_)
CORS(app)
# Define paths to CSV files
TRAIN_CSV_PATH = 'C:\Users\tejas\OneDrive\Desktop\flask\flask-server\train.csv'
STORE_CSV_PATH = 'C:\Users\tejas\OneDrive\Desktop\flask\flask-server\store.csv'

# Load data
training_data = pd.read_csv(TRAIN_CSV_PATH)
store_data = pd.read_csv(STORE_CSV_PATH)
training_data["Date"] = pd.to_datetime(training_data["Date"])


# Define a function to save plots
def save_plot(fig, filename):
    path = os.path.join('static', filename)
    fig.savefig(path)
    plt.close(fig)
    return path

@app.route('/sales', methods=['GET'])
def get_sales():
    # Logic to fetch and return sales data
    total_sales = training_data['Sales'].sum()
    return jsonify({"total_sales": total_sales})

@app.route('/sales_distribution', methods=['GET'])
def get_sales_distribution():
    plt.figure(figsize=(10, 6))
    sns.histplot(training_data['Sales'], bins=50, kde=True)
    plt.title('Sales Distribution')
    path = save_plot(plt.gcf(), 'sales_distribution.png')
    return send_file(path, mimetype='image/png')

@app.route('/sales_over_time', methods=['GET'])
def get_sales_over_time():
    plt.figure(figsize=(14, 7))
    plt.plot(training_data['Date'], training_data['Sales'])
    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    path = save_plot(plt.gcf(), 'sales_over_time.png')
    return send_file(path, mimetype='image/png')

@app.route('/seasonal_trends', methods=['GET'])
def get_seasonal_trends():
    decomposition = seasonal_decompose(training_data.set_index('Date')['Sales'], model='additive', period=365)
    fig = decomposition.plot()
    fig.set_size_inches(14, 7)
    path = save_plot(fig, 'seasonal_trends.png')
    return send_file(path, mimetype='image/png')

@app.route('/christmas_sales', methods=['GET'])
def get_christmas_sales():
    before_holiday, during_holiday, after_holiday = Christmas_Season_Sales("2014", "2015")
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=before_holiday.index, y=before_holiday["Sales"], label="Before", color="blue")
    sns.lineplot(x=during_holiday.index, y=during_holiday["Sales"], label="During", color="red")
    sns.lineplot(x=after_holiday.index, y=after_holiday["Sales"], label="After", color="green")
    plt.title("Christmas Season Sales")
    path = save_plot(plt.gcf(), 'christmas_sales.png')
    return send_file(path, mimetype='image/png')
app.run(port=5000)