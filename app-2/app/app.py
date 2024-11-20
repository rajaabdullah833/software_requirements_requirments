from flask import Flask, render_template, request, redirect, url_for, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import mysql.connector
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flashing messages

# MySQL Database connection
def connect_db():
    conn = mysql.connector.connect(
        host=os.getenv("host"),
        user=os.getenv("user"),
        password=os.getenv("password"),
        database=os.getenv("database")
    )
    return conn

# Function to insert project data into MySQL
def insert_project(data):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """
        INSERT INTO projects 
        (project_name, project_description, stakeholders, stakeholder_responsibilities, target_audience, 
        project_objectives, estimated_budget, project_timeline, data_management, rbac, rbac_details, analytics, 
        analytics_details, user_stories, use_cases, performance_requirements, usability_requirements, 
        reliability_requirements, support_maintain)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_management_json = json.dumps(data['data_management'])  # Convert to JSON string
        cursor.execute(query, (
            data['project_name'], data['project_description'], data['stakeholders'],
            data['stakeholder_responsibilities'], data['target_audience'],
            data['project_objectives'], data['estimated_budget'], data['project_timeline'],
            data_management_json, data['rbac'], data['rbac_details'], data['analytics'],
            data['analytics_details'], data['user_stories'], data['use_cases'],
            data['performance_requirements'], data['usability_requirements'],
            data['reliability_requirements'], data['support_maintain']
        ))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        flash("Database Insertion Error.")
    finally:
        cursor.close()
        conn.close()

# Fetch Wikipedia Summary
def fetch_wikipedia_summary(query):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=&explaintext=&titles={query}"
        response = requests.get(url)
        data = response.json()
        
        if 'query' not in data:
            return "No summary available."

        page = next(iter(data['query'].get('pages', {}).values()), {})
        return page.get('extract', 'No summary available.')
    except Exception as e:
        print(f"Error fetching Wikipedia summary: {e}")
        return "Wikipedia summary not available."

# Create PDF function
def create_pdf(data, pdf_filepath):
    try:
        # Ensure the 'static' folder exists
        os.makedirs(os.path.dirname(pdf_filepath), exist_ok=True)
        c = canvas.Canvas(pdf_filepath, pagesize=letter)
        width, height = letter

        y = height - 50
        for key, value in data.items():
            c.drawString(100, y, f"{key.replace('_', ' ').title()}: {value}")
            y -= 20

        wiki_summary = fetch_wikipedia_summary(data['project_name'])
        c.drawString(100, y, f"\nWikipedia Summary:\n{wiki_summary}")
        c.save()
    except Exception as e:
        print(f"Error creating PDF: {e}")
        flash("Error generating PDF file.")

# Routes
@app.route('/')
def start_page():
    return render_template('start.html')

@app.route('/form', methods=['GET', 'POST'])
def form_page():
    if request.method == 'POST':
        try:
            data = {
                'project_name': request.form['project_name'],
                'project_description': request.form['project_description'],
                'stakeholders': request.form['stakeholders'],
                'stakeholder_responsibilities': request.form['stakeholder_responsibilities'],
                'target_audience': request.form['target_audience'],
                'project_objectives': request.form['project_objectives'],
                'estimated_budget': request.form['estimated_budget'],
                'project_timeline': request.form['project_timeline'],
                'data_management': request.form.getlist('dataManagement'),
                'rbac': request.form['rbac'],
                'rbac_details': request.form['rbac_details'],
                'analytics': request.form['analytics'],
                'analytics_details': request.form['analytics_details'],
                'user_stories': request.form['Userstories'],
                'use_cases': request.form['Use_Cases'],
                'performance_requirements': request.form['performance_requirements'],
                'usability_requirements': request.form['usability_requirements'],
                'reliability_requirements': request.form['reliability_requirements'],
                'support_maintain': request.form['support_maintain'],
            }

            # Insert data into MySQL
            insert_project(data)

            # Create PDF file
            pdf_filename = f"{data['project_name']}_SRS.pdf"
            pdf_filepath = os.path.join('static', pdf_filename)
            create_pdf(data, pdf_filepath)

            return redirect(url_for('output_page', project_name=data['project_name'], pdf_filename=pdf_filename))
        except Exception as e:
            print(f"Error processing form: {e}")
            flash("An error occurred while processing the form.")
    return render_template('page1.html')

@app.route('/output')
def output_page():
    project_name = request.args.get('project_name')
    pdf_filename = request.args.get('pdf_filename')
    return render_template('output.html', project_name=project_name, pdf_filename=pdf_filename)

if __name__ == '__main__':
    app.run(debug=True)
