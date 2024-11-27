from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit  # Fix for text wrapping
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Database connection
def connect_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="123.Dola",
        database="project_srs"  
    )
    return conn

# Function to fetch all data from MySQL
def fetch_all_projects():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM projects")  # Replace 'projects' with your table name
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

# Function to create PDF from database data
def create_pdf_from_data(data, pdf_filepath):
    try:
        os.makedirs(os.path.dirname(pdf_filepath), exist_ok=True)  # Ensure directory exists
        c = canvas.Canvas(pdf_filepath, pagesize=letter)
        width, height = letter
        margin = 50
        y = height - margin  # Start drawing from the top of the page
        line_height = 20
        max_width = width - (2 * margin)  # Account for margins

        c.setFont("Helvetica", 12)

        for item in data:
            for key, value in item.items():
                # Format the text to wrap within the page width
                text = f"{key}: {value}"
                lines = simpleSplit(text, "Helvetica", 12, max_width)
                for line in lines:
                    c.drawString(margin, y, line)
                    y -= line_height
                    if y < margin:  # Add a new page if content overflows
                        c.showPage()
                        c.setFont("Helvetica", 12)
                        y = height - margin
                y -= 10  # Add extra space between key-value pairs
            y -= 20  # Add extra space between records

            if y < margin:  # Add a new page if content overflows
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - margin

        c.save()
        print(f"PDF successfully created at {pdf_filepath}")
    except Exception as e:
        print(f"Error creating PDF: {e}")

if __name__ == '__main__':
    try:
        # Fetch data from the database
        data = fetch_all_projects()

        if data:
            # Create the PDF file
            pdf_filepath = os.path.join('output', 'projects_data.pdf')
            create_pdf_from_data(data, pdf_filepath)
        else:
            print("No data found in the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
