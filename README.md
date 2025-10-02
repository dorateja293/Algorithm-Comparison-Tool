# Combinatorial Optimization Tool

This project is a web application built with Flask to compare various combinatorial optimization algorithms on standard problems such as 0/1 Knapsack and Traveling Salesman Problem (TSP).

## Features

- Implements multiple algorithms: Greedy, Dynamic Programming, Backtracking, Branch & Bound, Divide & Conquer.
- Allows users to upload custom datasets for Knapsack and TSP.
- Dynamic input of parameters such as knapsack capacity.
- Visualizes results with tables and charts.
- Professional and responsive UI using Bootstrap and custom styling.

## Project Structure

- `app.py`: Main Flask application with routes and logic.
- `problems/`: Problem definitions and data structures.
- `solvers/`: Algorithm implementations.
- `templates/`: HTML templates for UI.
- `static/css/`: Custom CSS styles.
- `utils/`: Utility modules for timing, logging, etc.

## Setup and Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the Flask app:
   ```
   python app.py
   ```

3. Open your browser at `http://127.0.0.1:5000` to access the tool.

4. Upload datasets, select algorithms, set parameters, and run comparisons.

## Notes

- Unnecessary folders such as `datasets/`, `results/`, and unused static JS files have been removed to keep the project clean.
- Ensure your datasets follow the expected CSV format for knapsack and TSP.

## License

MIT License
