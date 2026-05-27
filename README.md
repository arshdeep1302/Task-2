# Placement Analytics Dashboard

A simple data analytics dashboard built using Streamlit, Pandas, and Plotly for analyzing student placement performance.

## Features

* Student performance analysis
* Placement rate tracking
* College-wise performance
* Skill analysis
* Activity trends visualization
* Risk detection using Isolation Forest
* Interactive charts and filters

## Technologies Used

* Python
* Streamlit
* Pandas
* Plotly
* Scikit-learn

## Project Structure

```bash
Placement-Dashboard/
│
├── Data/
│   ├── Student.csv
│   ├── Skills.csv
│   ├── College.csv
│   ├── Activity.csv
│   └── Placement.csv
│
├── app.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/placement-dashboard.git
```

Go to the project folder:

```bash
cd placement-dashboard
```

Install required libraries:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
streamlit run app.py
```

## Dashboard Modules

### Overview

Shows:

* Total students
* Average score
* Average level
* Placement percentage

### Activity Analysis

* Daily active students
* Weekly activity analysis

### Placement Funnel

Visualizes:

* Students
* Interviewed students
* Placed students

### Skill Analysis

* Average score by skill
* Skill pass rates

### College Performance

Compares placement rates across colleges.

### Risk Analysis

Detects unusual student records using machine learning.

## Screenshots

Add screenshots of your dashboard here.

## Future Improvements

* Login system
* Better UI design
* More ML models
* Real-time analytics
* Export reports

## Author

Developed by [Your Name]

## License

This project is for educational purposes.
