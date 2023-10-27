# Long Cell Visualization for Code Smell Detection

This repository contains analysis notebooks that aim to investigate the code smell named `Long Cell`.

## Files Overview

### SLOC.ipynb 
**Code Smell**: Long Cell

This notebook is focused on the metric `Source Lines of Code (SLOC)` to determine the Long Cell code smell.

**Key Steps**:
1. **Importing Libraries**: Key Python libraries such as `numpy`, `pandas`, and `matplotlib` are utilized for data management and visualization.
2. **Data Loading**: The dataset from `metrics/source_lines_of_code.csv` is loaded into a pandas DataFrame.
3. **Boxplot Creation**: A boxplot is generated to visually represent the distribution of SLOC.

### CC.ipynb
**Code Smell**: Long Cell

This notebook is focused on the metric `Cyclomatic Complexity (CC)`.

**Key Steps**:
1. **Importing Libraries**: Standard libraries like `numpy`, `pandas`, and `matplotlib` are imported.
2. **Data Loading**: Data is imported from the designated path and processed using pandas.
3. **Boxplot Creation**: Boxplots are designed to depict the distribution of CC values.

### FC.ipynb
**Code Smell**: Long Cell

This notebook examines the metric `Functional Complexity (FC)`.

**Key Steps**:
1. **Importing Libraries**: As with other notebooks, main libraries are imported for data analysis and visualization.
2. **Data Loading**: Data related to FC is loaded and processed.
3. **Boxplot Creation**: Boxplots are used to visualize FC values across cells.

### Vol.ipynb
**Code Smell**: Long Cell

This notebook is dedicated to the metric `Volume`.

**Key Steps**:
1. **Importing Libraries**: Core Python libraries are imported.
2. **Data Loading**: Data representing the Volume metric is loaded from the given path.
3. **Boxplot Creation**: Using `matplotlib`, boxplots are generated to provide insights into Volume values.

## Visualization

Both notebooks prominently use boxplots as they effectively depict the data distribution, showcasing the median, quartiles, possible outliers, and other essential statistical figures. This visualization technique is crucial in pinpointing patterns and anomalies linked with the `Long Cell` code smell.

## Data Source

Datasets used in these analyses are extracted from CSV files. If you're attempting to reproduce or execute the notebooks, ensure the correct file paths are set.

---
