# Code Smell Classification and Analysis

This repository focuses on the classification and analysis of code smells using various machine learning models and techniques.

## 📓 Notebooks:

### 1. classification.ipynb
- **Description**: This notebook performs code smell classification using three machine learning models: Random Forest, XGB, and Decision Tree.
- **Key Findings**: Among the three models, Random Forest achieved the best classification results.

### 2. Cross-Validation.ipynb
- **Description**: Conducts cross-validation for five different code smells.
- **Metrics**: Precision, Recall, F1-Score, and Accuracy.

### 3. Evolution of correlation.ipynb
- **Description**: Analyzes the adjustment of rules for the first technique.

### 4. Global-Matrix-Confusion.ipynb
- **Description**: Visualizes the global confusion matrix comparing the results between the detection tool (technique 1) and manual labeling by a developer.

### 5. Matrix-Confusion.ipynb
- **Description**: Displays individual confusion matrices for each code smell.

### 6. ROC-Curve.ipynb
- **Description**: Plots the ROC curve for each code smell.

## 📁 Datasets:

- **manual_labeling.csv**: Contains code smell labels manually assigned by a developer.
- **metrics.csv**: Features metrics such as SLOC, CC, FC, etc., which are utilized in detecting code smells.
- **result_tool.csv**: Holds the detection results from the tool.
