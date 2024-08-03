# Data Science and Logistic Regression: Harry Potter and the Data Scientist

## Overview
This repository comprises mandatory projects for the Logistic Regression module in the Data Science curriculum at Ecole 42. It encompasses data analysis and logistic regression implementation.


Harry Potter and the Data Scientist: Write a Classifier and Save Hogwarts!
In this project, you will implement a linear classification model, specifically logistic regression, as an extension of the linear regression topic. 
Additionally, you are encouraged to develop a machine learning toolkit throughout the process.

### Key Tasks:

Data Preparation
1.Read Datasets: Learn to load and understand various data formats.
2.Data Visualization: Visualize data in multiple formats to gain insights.
3.Data Cleaning: Perform essential data cleaning by identifying and removing irrelevant or incorrect information to ensure the dataset is accurate and ready for analysis.

### Model Training: 
- Apply logistic regression to address classification problems. This involves training the model to make predictions based on the cleaned and prepared data.

- Toolkit Development: Build a machine learning toolkit to streamline your workflow and enhance your efficiency in future projects.

- By following these steps, you will gain hands-on experience in data preprocessing, visualization, and classification, ultimately contributing to saving Hogwarts!

## Prerequisites
Ensure you have the following libraries installed:
- NumPy
- Pandas
- Matplotlib

You can install them using pip:
```
pip install numpy pandas matplotlib
```

## Data Analysis
Explore the data using the provided scripts:
- Navigate to each folder (`describe`, `Histogram`, `Scatter plot`, `Pair plot`)
- Run `python3 [describe.py] dataset_train.csv` to visualize the dataset.

## Collaborators
- `balbecke` - Collaborator from Ecole 42

------------------------------------------------------------------------------------------

## Introduction
In the realm of data science, understanding and analyzing data are paramount. Professor McGonagall tasks you with creating a program called `describe.[extension]` to explore numerical features in a dataset. Additionally, delve into data visualization techniques and implement logistic regression for multi-classification.

## Part I: Data Analysis
Before any analysis, familiarize yourself with the data. The `describe.[extension]` program provides insights into various features, such as count, mean, standard deviation, and quartiles. Understanding raw data is key to effective analysis.

## Part II: Data Visualization
Visualization plays a vital role, enabling insights and pattern detection. Create scripts to visualize data:
- **Histogram:** Identify courses with a homogeneous score distribution across Hogwarts houses.
- **Scatter Plot:** Determine similar features.
- **Pair Plot:** Explore feature relationships for logistic regression feature selection.

## Part III: Logistic Regression
Implement logistic regression for multi-class classification. Train models using gradient descent to minimize error:
- **logreg_train.[extension]:** Train models and generate weight files.
- **logreg_predict.[extension]:** Use trained weights to predict Hogwarts houses for test data and output predictions to `houses.csv`.

## Bonus Part
For an extra challenge, implement additional features or optimization algorithms. Bonuses are assessed after completing all mandatory requirements.
