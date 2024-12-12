# Subscription Calculator

## Overview  
The Subscription Calculator is a simple web app built using Flask. It helps you keep track of your subscriptions and their costs. You can enter details like the name of the subscription, how much it costs, how often you pay (weekly, monthly, yearly), and an optional description. The app shows your total spending per week, month, and year, making it easier to manage your budget.  

---  

## Features  

### **1. Add Subscriptions**  
You can add a subscription by filling out a form with these details:  
- **Name**: The name of the subscription.  
- **Price**: How much it costs.  
- **Frequency**: How often you pay (weekly, monthly, or yearly).  
- **Description**: Extra details (optional).  

### **2. View and Manage Subscriptions**  
- See all your subscriptions in a table.  
- Use the edit button to change subscription details or the delete button to remove a subscription.  

### **3. Calculate Total Costs**  
The app calculates your total spending:  
- **Weekly costs**  
- **Monthly costs** (including weekly/yearly subscriptions converted to monthly).  
- **Yearly costs** (including weekly/monthly subscriptions converted to yearly).  

### **4. Edit and Delete Options**  
- **Edit**: Change the details of a subscription.  
- **Delete**: Remove a subscription.  

---  

## How It Works  

### **1. App Structure**  
- **Backend**: Built with Flask (Python) for handling data and routes.  
- **Frontend**: HTML templates (Jinja) to show data.  
- **Database**: SQLite to store subscription details.  

### **2. Key Functions**  

#### **Database Setup**  
The `init_db()` function creates a database (`subscriptions.db`) with a table for subscription information:  
```sql  
CREATE TABLE IF NOT EXISTS subscriptions (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,  
    name TEXT NOT NULL,  
    price TEXT NOT NULL,  
    frequency TEXT NOT NULL,  
    description TEXT  
);  
```  

#### **Add Subscriptions**  
When you fill out the form, the app saves your subscription to the database:  
```python  
c.execute('''  
    INSERT INTO subscriptions (name, price, frequency, description)  
    VALUES (?, ?, ?, ?)  
''', (name, price, frequency, description))  
```  

#### **View Subscriptions**  
The app shows all subscriptions in a table using a Jinja template:  
```python  
@app.route('/')  
def index():  
    c.execute('SELECT * FROM subscriptions')  
    subscriptions = c.fetchall()  
    return render_template('index.html', subscriptions=subscriptions)  
```  

#### **Calculate Costs**  
The `calculate_total_costs()` function adds up costs based on how often you pay:  
```python  
if frequency == 'weekly':  
    total_monthly += price * 4.33  # Converts weekly to monthly  
    total_yearly += price * 52  # Converts weekly to yearly  
elif frequency == 'monthly':  
    total_weekly += price / 4.33  
    total_yearly += price * 12  
elif frequency == 'yearly':  
    total_weekly += price / 52  
    total_monthly += price / 12  
```  

#### **Edit Subscriptions**  
The `edit()` function lets you change a subscription:  
```python  
@app.route('/edit/<int:id>', methods=['GET', 'POST'])  
def edit(id):  
    c.execute('SELECT * FROM subscriptions WHERE id = ?', (id,))  
    subscription = c.fetchone()  
    c.execute('''  
        UPDATE subscriptions  
        SET name = ?, price = ?, frequency = ?, description = ?  
        WHERE id = ?  
    ''', (name, price, frequency, description, id))  
```  

#### **Delete Subscriptions**  
The `delete()` function removes a subscription:  
```python  
@app.route('/delete/<int:id>', methods=['POST'])  
def delete(id):  
    c.execute('DELETE FROM subscriptions WHERE id = ?', (id,))  
```  

---  

## What You Need  
- Python 3.x  
- Flask (install with `pip install flask`)  
- SQLite  

---  

## How to Install  

1. Download the project:  
   ```bash  
   git clone https://github.com/HenrikHaalandDev/Subscription-Tracker.git
   cd subscription-calculator  
   ```  

2. Install the necessary libraries:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Set up the database:  
   ```bash  
   python app.py  
   ```  
   This creates the `subscriptions.db` file.  

4. Run the app:  
   ```bash  
   flask run  
   ```  

5. Open your browser and go to: `http://127.0.0.1:5000`  

---  

## How to Use  
1. Start the app and open it in your browser.  
2. Add your subscriptions using the form.  
3. View, edit, or delete your subscriptions in the table.  
4. Check your weekly, monthly, and yearly spending on the "Total Subscription Costs" page.  
