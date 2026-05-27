# PLACEMUX ANALYTICS DASHBOARD GUIDE

## Overview

This project is an interactive analytics dashboard developed using Streamlit and Python.

The dashboard focuses on analyzing student learning behavior, placement performance, skill difficulty trends, and college-level comparisons.

The goal of the project is to identify actionable insights that can help improve learning outcomes and placement success.

---

# Features

## 1. Executive Overview

Displays important KPIs including:

* Total students
* Placement rate
* Average skill score
* Average interview score
* Weekly learning hours

---

## 2. Student Journey Funnel

Tracks the progression of students through different stages:

* Signup
* Level 50 completion
* Interview eligibility
* Placement

This section helps identify major drop-off points in the learning journey.

---

## 3. Skill Difficulty Analysis

Analyzes:

* Average skill performance
* Pass rates
* Hardest skills
* Common low-performing areas

This helps identify which skills require additional learning support.

---

## 4. College Performance Comparison

Compares colleges based on:

* Average skill score
* Interview performance
* Placement conversion
* Student engagement

---

## 5. Trend Analysis

Visualizes:

* Student growth trends
* Weekly learning activity
* Interview score progression

---

## 6. Anomaly Detection

Automatically highlights:

* Students with very low scores
* Low engagement patterns
* Unusual performance drops

---

# Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* Scikit-learn

---

# Project Structure

PLACEMUX_DASHBOARD/
│
├── dashboard.py
├── requirements.txt
├── DASHBOARD_GUIDE.md
├── data/
│   ├── students.csv
│   ├── colleges.csv
│   ├── skills.csv

---

# How to Run the Project

## Step 1

Install required libraries:

pip install -r requirements.txt

## Step 2

Run the Streamlit dashboard:

streamlit run dashboard.py

---

# Key Insights Generated

* Students with higher weekly practice hours generally perform better in interviews.
* Python and Statistics are comparatively difficult skills with lower pass rates.
* Some colleges show high engagement but lower placement conversion.
* Students completing Level 50 have significantly better placement outcomes.

---

# Future Improvements

Possible future enhancements:

* Machine learning placement prediction
* Real-time database integration
* User authentication
* Exportable PDF reports
* Advanced anomaly detection

---

# Conclusion

This dashboard was designed to provide a clear and interactive view of student learning and placement performance.

The project focuses not only on visualization but also on generating useful insights that can support better academic and placement decisions.
