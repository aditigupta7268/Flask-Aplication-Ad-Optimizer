from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import pickle

app = Flask(__name__)

# --- CONFIGURATION ---
# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aditi@123'
app.config['MYSQL_DB'] = 'ad_dashboard'

mysql = MySQL(app)

# --- ML MODEL ---
def load_model():
    """Loads the pickled machine learning model."""
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        print("Warning: model.pkl not found. ML features will be disabled.")
        return None

# --- API ROUTES ---

@app.route('/api/performance_data')
def performance_data():
    """API endpoint to provide campaign data for charts."""
    cur = None  # Initialize cursor to None
    try:
        cur = mysql.connection.cursor()
        # Fetch data needed for the chart (e.g., name, clicks, conversions)
        cur.execute("SELECT name, clicks, conversions FROM campaigns ORDER BY clicks DESC LIMIT 10")
        campaigns = cur.fetchall()
        
        # Format data for Chart.js
        labels = [row[0] for row in campaigns]
        clicks_data = [row[1] for row in campaigns]
        conversions_data = [row[2] for row in campaigns]
        
        chart_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Clicks',
                    'data': clicks_data,
                    'borderColor': 'rgba(79, 70, 229, 1)',
                    'backgroundColor': 'rgba(79, 70, 229, 0.2)',
                    'tension': 0.3,
                    'fill': True,
                },
                {
                    'label': 'Conversions',
                    'data': conversions_data,
                    'borderColor': 'rgba(16, 185, 129, 1)',
                    'backgroundColor': 'rgba(16, 185, 129, 0.2)',
                    'tension': 0.3,
                    'fill': True,
                }
            ]
        }
        return jsonify(chart_data)
    except Exception as e:
        print(f"Database error in /api/performance_data: {e}")
        return jsonify({'error': 'Could not retrieve chart data'}), 500
    finally:
        if cur:
            cur.close()


# --- CORE APPLICATION ROUTES ---

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    """Fetches and displays all campaign data on the dashboard."""
    cur = None # Initialize cursor to None
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM campaigns")
        data = cur.fetchall()
        return render_template('dashboard.html', data=data)
    except Exception as e:
        print(f"Database error in /dashboard: {e}")
        return render_template('dashboard.html', data=[], error="Could not connect to the database.")
    finally:
        if cur:
            cur.close()


@app.route('/ml_insights', methods=['GET', 'POST'])
def ml_insights():
    """Handles ML predictions based on user input."""
    predictions = None
    if request.method == 'POST':
        try:
            # Get form data
            impressions = float(request.form['impressions'])
            clicks = float(request.form['clicks'])
            
            model = load_model()
            if model:
                # Predict using the loaded model
                prediction_result = model.predict([[impressions, clicks]])[0]
                # Format the prediction for display (example format)
                # You might need to adjust this based on your model's output
                predictions = [('PRED-01', f"{prediction_result:.2%}", f"{prediction_result / 10:.0f}")]
            else:
                # Handle case where model is not loaded
                print("ML model could not be loaded for prediction.")

        except (ValueError, KeyError) as e:
            # Gracefully handle invalid form input
            print(f"Error processing ML insights form: {e}")
            pass
            
    return render_template('ml_insights.html', predictions=predictions)


@app.route('/optimization')
def optimization():
    """Renders the budget optimization page."""
    return render_template('optimization.html')

@app.route('/optimize_budget', methods=['POST'])
def optimize_budget():
    """Handles the budget optimization logic."""
    campaign_id = request.form.get('campaign_id')
    current_budget_str = request.form.get('budget', '0')
    recommendation = "Please enter valid campaign data."

    try:
        # A simple recommendation logic: suggest a 20% increase
        current_budget = float(current_budget_str)
        recommended_budget = current_budget * 1.20
        recommendation = (f"For Campaign '{campaign_id}', a budget of "
                          f"₹{recommended_budget:,.2f} is recommended for potentially higher performance.")
    except ValueError:
        recommendation = "Invalid budget amount. Please enter a number."
        
    return render_template('optimization.html', recommendation=recommendation)


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html')


if __name__ == '__main__':
    # Set debug=False for production environments
    app.run(debug=True)

