from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
DATABASE = 'expenses.db'
STATIC_FOLDER = 'static'

# Initialize database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()

# Generate charts for analytics
def generate_charts():
    # Query data from the database
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        data = cursor.fetchall()

    categories = [item[0] for item in data]
    amounts = [item[1] for item in data]

    # Create and save a bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts, color='skyblue')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    bar_chart_path = os.path.join(STATIC_FOLDER, 'category_bar_chart.png')
    plt.savefig(bar_chart_path)
    plt.close()

    # Create and save a pie chart
    plt.figure(figsize=(8, 5))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title('Expense Distribution')
    pie_chart_path = os.path.join(STATIC_FOLDER, 'category_pie_chart.png')
    plt.savefig(pie_chart_path)
    plt.close()

# Routes
@app.route('/')
def index():
    """Home page: Display all expenses."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses')
        expenses = cursor.fetchall()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    """Add new expense."""
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)',
                           (date, category, amount, description))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    """Edit an existing expense."""
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE expenses
                              SET date = ?, category = ?, amount = ?, description = ?
                              WHERE id = ?''', 
                           (date, category, amount, description, expense_id))
            conn.commit()
        return redirect(url_for('index'))

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses WHERE id = ?', (expense_id,))
        expense = cursor.fetchone()

    return render_template('edit_expense.html', expense=expense)

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    """Delete an expense by ID."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/analytics')
def analytics():
    """Analytics page: Generate and display charts."""
    generate_charts()  # Generate the charts each time the analytics page is visited
    return render_template('analytics.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
