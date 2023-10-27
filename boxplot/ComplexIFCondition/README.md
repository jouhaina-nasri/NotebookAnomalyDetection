# Complex IF Condition Analysis

This repository contains analysis notebooks that aim to investigate the code smell named `Complex IF Condition`.

## Files Overview

### DNIC.ipynb 
**Code Smell**: Complex IF Condition

This notebook is concentrated on the metric related to the nested depth of `if` conditional statements.

**Key Steps**:
1. **Importing Libraries**: Essential Python libraries such as `numpy`, `pandas`, and `matplotlib` are imported for data manipulation and visualization.
2. **Data Loading**: The data is read from `metrics/nested_array_depth_flattened.csv` into a DataFrame for further processing.
3. **Boxplot Creation**:
   - A boxplot is generated to visualize the distribution of the nested depth values specifically for `Cell 0`.
   - Another boxplot showcases the median values of the other cells, providing insights into the general distribution of the metric across cells.

### NOIC.ipynb
**Code Smell**: Complex Ternary Conditional

This notebook focuses on the metric related to the number of `if` conditional statements.

**Key Steps**:
1. **Importing Libraries**: As in the previous notebook, core libraries like `numpy`, `pandas`, and `matplotlib` are imported.
2. **Data Loading**: The dataset is sourced from `/home/jouhaina/Documents/PFE/detector/metrics/num_conditions.csv` and loaded into a DataFrame.
3. **Boxplot Creation**:
   - A boxplot is designed to depict the distribution of the number of `if` conditionals specifically for `Cell 0`.
   - Another boxplot showcases the median values of the other cells, providing insights into the general distribution of the metric across cells.

## Visualization

Boxplots are used prominently in both notebooks as they effectively depict data distribution, displaying the median, quartiles, potential outliers, and other statistical measures. This visualization technique aids in identifying patterns and anomalies associated with the `ComplexIFCondition` code smell.

## Data Source

Datasets utilized in the analyses are sourced from CSV files. If you're replicating or running the notebooks, ensure to have the appropriate file paths set:

- For **DNIC.ipynb**: `metrics/nested_array_depth_flattened.csv`
- For **NOIC.ipynb**: `metrics/num_conditions.csv`

---
