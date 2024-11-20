# Project SRS Generator
This project is a Software Requirements Specification (SRS) Generator that allows users to submit project details through a web form, stores them in a MySQL database, generates an SRS document using AI, and provides a downloadable PDF.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Routes](#routes)
- [Contributing](#contributing)
- [License](#license)

## Features
- **AI Integration**: Automatically generates detailed SRS documents based on user inputs.
- **Data Storage**: Saves project details in a MySQL database for easy retrieval and management.
- **PDF Generation**: Converts AI-generated SRS content into a formatted PDF file for download.
- **Flask Web Framework**: Provides an interactive web form for user input and data submission.

## Requirements
- **Python 3.7+**
- **MySQL Server**

### Python Packages:
- `Flask`
- `mysql-connector-python`
- `transformers`
- `reportlab`

## Setup and Installation

### Clone the Repository
```bash
git clone https://github.com/your-username/srs-generator.git
cd srs-generator/app
```
### Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Database Setup
- Ensure MySQL server is running.
- Create a database named project_srs and a table projects with the required columns.
- Update the connect_db function in app.py with your MySQL credentials.

### AI Model Directory
- Place the AI model files (config.json, pytorch_model.bin, etc.) in the model folder under the app directory.

###Run the Application

```bash
python app.py
```

###Access the Web Interface

####Open a browser and navigate to:

```bash
http://127.0.0.1:5000/
```

## Usage
- Navigate to `/form`: Start entering project details using the web form.
- Submit Data: Upon submission, project data will be saved to the database and an SRS document will be generated.
- View Generated PDF: The generated SRS document is available for download on the output page.

## Routes

| Route    | Method     | Description                                       |
|----------|------------|---------------------------------------------------|
| `/`      | GET        | Start page of the application                     |
| `/form`  | GET/POST   | Form page for entering project details            |
| `/output`| GET        | Displays project information and link to download the PDF |

### Contributing
Contributions are welcome! To make a contribution:

1. Fork the project.
2. Create a new branch.
3. Commit your changes.
4. Submit a pull request.

## License
This project is licensed under the MIT License.
