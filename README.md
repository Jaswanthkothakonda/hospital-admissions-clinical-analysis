# Hospital Admissions & Clinical Outcomes Analysis

## Project Overview
This project analyzes hospital admission and clinical data to identify
patterns in patient demographics, admission types, medical conditions,
length of stay, clinical measurements, and patient outcomes.
The project follows an end-to-end data analytics workflow using:

**Python → MySQL/SQL → Power BI**

Python was used for data inspection, cleaning, validation, statistical analysis, and visualization. The cleaned dataset was then loaded into MySQL for SQL-based analysis and data-quality validation. Power BI was used to create an interactive multi-page analytical dashboard.

## Objectives
- Inspect and understand hospital admission data
- Clean and prepare the dataset for analysis
- Handle missing and invalid values
- Perform exploratory and statistical analysis
- Load the cleaned dataset into MySQL
- Perform SQL-based analysis and validation
- Analyze patient demographics and admission patterns
- Examine medical condition prevalence
- Analyze hospital length of stay
- Compare outcomes across admission types, gender, and age groups
- Analyze clinical measurements such as glucose and ejection fraction
- Build an interactive Power BI dashboard

## Tools & Technologies
- Python
- Pandas
- Matplotlib
- Jupyter Notebook
- MySQL
- SQL
- Power BI
- DAX
- Git
- GitHub

## Dataset
**Dataset:** Hospital Admissions Data  
**Source:** Kaggle  
**Author:** Ashish Sahani
The dataset contains hospital admission and clinical information covering multiple years.

The project uses a cleaned version of the admission data for analysis.

## Data Preparation
The dataset was inspected and cleaned using Python and Pandas.
Main preprocessing steps included:
- Standardizing column names
- Converting date fields to appropriate datetime types
- Handling missing values
- Handling invalid date values
- Converting clinical measurements to numeric types
- Converting categorical and numerical fields to appropriate data types
- Creating admission year and month fields
- Creating age-group categories
- Calculating length of stay where applicable
- Handling invalid values in selected fields
- Checking for duplicate records
- Performing data-quality validation

The final cleaned admission dataset contains:
**15,757 records and 60 columns**

## SQL / MySQL Analysis
The cleaned hospital admissions dataset was loaded into a MySQL database
named `hospital_analysis`.

The main table is:
hospital_admissions