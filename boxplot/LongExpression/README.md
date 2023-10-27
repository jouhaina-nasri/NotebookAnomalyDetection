# Long Expression Analysis

This repository contains analysis notebooks dedicated to investigating the code smell named `Long Expression`.

## File Overview

### NOC.ipynb
**Code Smell**: Long Expression

This notebook emphasizes the metric **Number of Characters in One Expression (NOCE)** to identify the Long Expression code smell.

**Key Steps**:
1. **Importing Libraries**: Essential Python libraries for data manipulation and visualization, such as `numpy`, `pandas`, and `matplotlib`, are imported.

2. **Load Data into DataFrame**: Data is sourced from the CSV file at `/metrics/expression_length_flattened.csv` and then loaded into a pandas DataFrame for processing. The dataset is further filtered to separate data corresponding to `Cell 0` and other cells.

3. **Creating Boxplot for Metric Number of Characters in One Expression**: 
    - **Boxplot for Cell 0 values**: A boxplot is generated to showcase the data distribution of values related to `Cell 0`.
    - **Boxplot for Other Cells (Median)**: A separate boxplot is used to display the median values of data from cells other than `Cell 0`, providing insights into the overall distribution of the metric across various cells.

## Visualization

Boxplots are heavily utilized in the notebook as they proficiently display data distributions. These visualizations highlight the median, quartiles, potential outliers, and other essential statistical parameters. Using these visualizations, patterns and irregularities linked with the `Long Expression` code smell can be identified.

---
