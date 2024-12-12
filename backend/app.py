from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os



app = Flask(__name__, static_folder='../static', template_folder='../templates')


print(app.static_folder)

def init_db():
    if not os.path.exists('subscriptions.db'):
        conn = sqlite3.connect('subscriptions.db')
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                frequency TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized and table created.")
    else:
        print("Database already exists.")

def calculate_total_costs():
    """Calculate the total costs of all subscriptions."""
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()

    # Get all subscriptions
    c.execute('SELECT price, frequency FROM subscriptions')
    subscriptions = c.fetchall()
    conn.close()

    total_weekly = 0
    total_monthly = 0
    total_yearly = 0

    # Calculate total cost for each timeframe
    for price, frequency in subscriptions:
        try:
            price = float(price)
            if frequency == 'weekly':
                total_weekly += price
                total_monthly += price * 4.348  # 4.348 weeks in a month
                total_yearly += price * 52.18  # 52.18 weeks in a year
            elif frequency == 'monthly':
                total_weekly += price / 4.348  # Convert monthly to weekly
                total_monthly += price
                total_yearly += price * 12  # 12 months in a year
            elif frequency == 'yearly':
                total_weekly += price / 52.18  # Convert yearly to weekly
                total_monthly += price / 12  # Convert yearly to monthly
                total_yearly += price
        except ValueError:
            pass  # If price is invalid, skip it

    return round(total_weekly, 2), round(total_monthly, 2), round(total_yearly, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        frequency = request.form['frequency']
        description = request.form.get('description', '')

        conn = sqlite3.connect('subscriptions.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO subscriptions (name, price, frequency, description)
            VALUES (?, ?, ?, ?)
        ''', (name, price, frequency, description))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    # Shows all subscriptions added
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()
    c.execute('SELECT * FROM subscriptions')
    subscriptions = c.fetchall()
    conn.close()

    return render_template('index.html', subscriptions=subscriptions)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()

    c.execute('SELECT * FROM subscriptions WHERE id = ?', (id,))
    subscription = c.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        frequency = request.form['frequency']
        description = request.form.get('description', '')

        # Update the subscription data
        c.execute('''
            UPDATE subscriptions
            SET name = ?, price = ?, frequency = ?, description = ?
            WHERE id = ?
        ''', (name, price, frequency, description, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('edit.html', subscription=subscription)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = sqlite3.connect('subscriptions.db')
    c = conn.cursor()

    # Delete the subscription
    c.execute('DELETE FROM subscriptions WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/calculate', methods=['GET'])
def calculate():
    total_weekly, total_monthly, total_yearly = calculate_total_costs()

    return render_template('calculate.html', total_weekly=total_weekly, total_monthly=total_monthly, total_yearly=total_yearly)

if __name__ == '__main__':
    init_db()  
    app.run(debug=True, host="0.0.0.0")
