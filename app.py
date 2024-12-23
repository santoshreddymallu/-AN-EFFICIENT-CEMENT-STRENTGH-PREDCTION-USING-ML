from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flashing messages

# # MySQL connection configuration
# def create_connection():
#     return mysql.connector.connect(
#         host='localhost',    # Replace with your MySQL host
#         user='your_username',  # Replace with your MySQL username
#         password='your_password',  # Replace with your MySQL password
#         database='your_database'   # Replace with your MySQL database name
#     )

# Function to execute and commit SQL queries
# def execute_sql(query, params=None):
#     conn = create_connection()
#     if conn.is_connected():
#         cursor = conn.cursor()
#         cursor.execute(query, params)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return True
#     else:
#         return False

# Route for the registration page
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         # Get form data
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         # Input validation (basic example)
#         if not username or not email or not password or not confirm_password:
#             flash('Please fill out all fields', 'error')
#             return redirect(url_for('register'))

#         if password != confirm_password:
#             flash('Passwords do not match!', 'error')
#             return redirect(url_for('register'))

#         # Check if the user already exists
#         conn = create_connection()
#         if conn.is_connected():
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
#             existing_user = cursor.fetchone()

#             if existing_user:
#                 flash('User with this email already exists!', 'error')
#                 cursor.close()
#                 conn.close()
#                 return redirect(url_for('register'))
#             else:
#                 # Insert data into MySQL using the execute_sql function
#                 if execute_sql("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
#                                (username, email, password)):
#                     flash('Registration successful!', 'success')
#                     return redirect(url_for('login'))  # Redirect to login page after successful registration
#                 else:
#                     flash('Failed to connect to the database.', 'error')
#                 return redirect(url_for('register'))
#         else:
#             flash('Failed to connect to the database.', 'error')
#             return redirect(url_for('register'))

#     return render_template('register.html')



@app.route('/')
def index():
    return render_template('index.html')  


@app.route('/about')
def about():
    return render_template('about.html')  


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        days = int(request.form['days'])
        blaine = float(request.form['blaine'])
        residue90 = float(request.form['residue90'])
        residue45 = float(request.form['residue45'])
        nc = float(request.form['nc'])
        loi = float(request.form['loi'])
        so3 = float(request.form['so3'])
        c3s = float(request.form['c3s'])
        c2s = float(request.form['c2s'])
        c3a = float(request.form['c3a'])
        lsf = float(request.form['lsf'])
        moisture = float(request.form['moisture'])
        clinkerLiter = float(request.form['clinkerLiter'])
        clinkerFeedTemp = float(request.form['clinkerFeedTemp'])
        water = float(request.form['water'])
        gadDosage = float(request.form['gadDosage'])
        cementTemp = float(request.form['cementTemp'])
        

        # Create a list of the input features
        input_features = [days, blaine, residue90, residue45, nc, loi, so3, c3s, c2s, c3a, lsf, moisture, clinkerLiter, clinkerFeedTemp, water, gadDosage, cementTemp]
        print(input_features)

        # Load the model and make the prediction
        import joblib
        model = joblib.load('polymodel.joblib')
        poly = joblib.load('poly.joblib')
        new = poly.transform([input_features])
        prediction = model.predict(new)

        # Render the template with the prediction
        return render_template('prediction.html', prediction=prediction)

    return render_template('prediction.html')

 



@app.route('/model',methods=['GET', 'POST'])
def model():
    if request.method == 'POST':
        model = int(request.form['model'])
        if model == 1:
            result = "Linear Regression: 99%"
        elif model == 2:
            result = "ANN: 98%"
        elif model == 3:
            result = "Gradient Boost Regressor: 99%"
        elif model == 4:
            result = "Decision Tree Regressor: 98%"
        elif model == 5:
            result = "Random Forest Regressor: 99%"
        elif model == 6:
            result = "Extra Tree Regressor: 98%"
        elif model == 7:
            result = "Hist Gradient Boost Regressor: 99%"
        return render_template('model.html', result=result)
    return render_template('model.html')


    
if __name__ == '__main__':
    app.run(debug=True)
