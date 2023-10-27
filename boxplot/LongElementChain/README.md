# Long Element Chain Analysis

This repository contains analysis notebooks that aim to investigate the code smell named `Long Element Chain`.

## Files Overview

### DNA.ipynb 
**Code Smell**: Long Element Chain

This notebook is focused on the metric `Depth of Nested Array (DNA)` to determine the Long Element Chain code smell.

**Key Steps**:
1. **Importing Libraries**: Essential Python libraries such as `numpy`, `pandas`, and `matplotlib` are incorporated for data analysis and visualization.
2. **Data Loading**: The dataset from `metrics/nested_array_depth_flattened.csv` is loaded into a pandas DataFrame.
3. **Boxplot Creation**: A boxplot is crafted to visually represent the distribution of DNA values.

### LOEC.ipynb
**Code Smell**: Long Element Chain

This notebook is focused on the metric `Length of Element Chain (LOEC)`.

**Key Steps**:
1. **Importing Libraries**: Fundamental libraries like `numpy`, `pandas`, and `matplotlib` are imported for efficient data manipulation and visualization.
2. **Data Loading**: The dataset from `metrics/element_chain_length_flattened.csv` is loaded into a pandas DataFrame.
3. **Boxplot Creation**: Boxplots are designed to visualize the distribution of LOEC values across different notebook cells.

## Visualization

The notebooks mainly employ boxplots for visual representation. This choice is due to the efficiency of boxplots in showcasing data distribution, highlighting the median, quartiles, potential outliers, and other pivotal statistical measures. Such visualizations are instrumental in identifying trends and irregularities associated with the `Long Element Chain` code smell.
