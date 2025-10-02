from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import logging
import os
from werkzeug.utils import secure_filename
from solvers import GreedyKnapsack, GreedyTSP, DPKnapsack, DPTSP, BacktrackingKnapsack, BacktrackingTSP, BBKnapsack, BBTSP, DCKnapsack, DCTSP
from problems.knapsack import Knapsack
from problems.tsp import TSP
from utils.timers import measure_time
from utils.logger import setup_logger

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
logger = setup_logger()

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_knapsack_data_from_file(file_path):
    items = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    try:
                        value = int(row[0])
                        weight = int(row[1])
                        name = row[2]
                        items.append((value, weight, name))
                    except ValueError:
                        logging.warning(f"Invalid data in {file_path}: {row}")
                        continue
    except Exception as e:
        logging.error(f"Error loading {file_path}: {e}")
    return items

def load_tsp_data_from_file(file_path):
    cities = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    try:
                        x = float(row[0])
                        y = float(row[1])
                        cities.append((x, y))
                    except ValueError:
                        logging.warning(f"Invalid data in {file_path}: {row}")
                        continue
    except Exception as e:
        logging.error(f"Error loading {file_path}: {e}")
    return cities


default_knapsack = [
    (60, 10, 'A'),
    (100, 20, 'B'),
    (120, 30, 'C')
]
default_capacity = 50

default_tsp = [(0, 0), (2, 3), (5, 2), (6, 6), (8, 3)]

algorithms = {
    'Greedy': (GreedyKnapsack, GreedyTSP),
    'Dynamic Programming': (DPKnapsack, DPTSP),
    'Backtracking': (BacktrackingKnapsack, BacktrackingTSP),
    'Branch & Bound': (BBKnapsack, BBTSP),
    'Divide & Conquer': (DCKnapsack, DCTSP)
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    # Handle file uploads
    knapsack_file = request.files.get('knapsackFile')
    tsp_file = request.files.get('tspFile')
    capacity = request.form.get('capacity', type=int)
    selected_algorithms = request.form.getlist('algorithms')

    knapsack_items = []
    tsp_cities = []

    if knapsack_file and allowed_file(knapsack_file.filename):
        filename = secure_filename(knapsack_file.filename)
        knapsack_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        knapsack_file.save(knapsack_path)
        knapsack_items = load_knapsack_data_from_file(knapsack_path)
    else:
        knapsack_items = load_knapsack_data_from_file('datasets/knapsack.csv')
        if not knapsack_items:
            knapsack_items = default_knapsack

    if tsp_file and allowed_file(tsp_file.filename):
        filename = secure_filename(tsp_file.filename)
        tsp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        tsp_file.save(tsp_path)
        tsp_cities = load_tsp_data_from_file(tsp_path)
    else:
        tsp_cities = load_tsp_data_from_file('datasets/tsp.csv')
        if not tsp_cities:
            tsp_cities = default_tsp

    if not capacity or capacity <= 0:
        capacity = default_capacity

    results = []

    for name in selected_algorithms:
        knap_class, tsp_class = algorithms.get(name, (None, None))
        if knap_class:
            instance = Knapsack(knapsack_items, capacity)
            solver = knap_class()
            try:
                solution, t = measure_time(solver.solve, instance)
                selected, value = solution
                results.append([name, 'Knapsack', str(selected), f"{t:.6f}", value])
            except Exception as e:
                logger.error(f"Error in {name} Knapsack: {e}")
                results.append([name, 'Knapsack', 'Error', 'N/A', 'N/A'])
        if tsp_class:
            instance = TSP(tsp_cities)
            solver = tsp_class()
            try:
                solution, t = measure_time(solver.solve, instance)
                tour, dist = solution
                results.append([name, 'TSP', str(tour), f"{t:.6f}", dist])
            except Exception as e:
                logger.error(f"Error in {name} TSP: {e}")
                results.append([name, 'TSP', 'Error', 'N/A', 'N/A'])

    # Save results to CSV
    os.makedirs('results', exist_ok=True)
    with open('results/output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Algorithm', 'Problem', 'Solution', 'Time', 'Metric'])
        writer.writerows(results)

    return redirect(url_for('results'))

@app.route('/results')
def results():
    results_data = []
    try:
        with open('results/output.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            results_data = list(reader)
    except FileNotFoundError:
        logging.info("No results file found")
    except Exception as e:
        logging.error(f"Error reading results: {e}")
    return render_template('results.html', results=results_data)

if __name__ == '__main__':
    app.run(debug=True)
