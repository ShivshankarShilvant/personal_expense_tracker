# personal_expense_tracker

A simple Flask web application to track and analyze your expenses using SQLite and matplotlib.

## 🔧 Features

- Add, edit, and delete expense records
- Store data in a local SQLite database
- Visualize spending via:
  - Bar chart (by category)
  - Pie chart (percentage distribution)
- Auto-generated charts on `/analytics` route

## 🖥 Tech Stack

- Python (Flask, SQLite3)
- HTML + Jinja templates
- Matplotlib for data visualization

## 📷 Screenshots

Analytics (Bar + Pie Chart)
![Bar Chart](static/category_bar_chart.png)  
![Pie Chart](static/category_pie_chart.png)


## 🚀 How to Run

```bash
pip install flask matplotlib
python app.py
