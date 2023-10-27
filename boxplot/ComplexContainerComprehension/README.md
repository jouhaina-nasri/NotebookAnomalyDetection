# Code Smell Analysis

This repository contains analysis notebooks for identifying the code smell `Complex Container Comprehension`.

## Files Overview

1. **LOC.ipynb**: This notebook focuses on the metric related to the `Length of Container Comprehension`. We've used boxplots to analyze and visualize the distribution of this metric across different datasets.

2. **NOL+NOCC.ipynb**: This notebook explores the combined metrics of `Number of Loops` and `Number of Control Conditions` in container comprehensions. As with the first notebook, we employ boxplots to vividly present the distribution.

## Visualization

For both metrics, we've leveraged boxplots because they are particularly useful in depicting the distribution of the data, showing the median, quartiles, and potential outliers. This makes it easier to pinpoint unusual patterns or values that deviate from the norm, which is essential in our quest to identify and rectify the `Complex Container Comprehension` code smell.

## Data Source

The datasets used in these analyses are sourced from CSV files. Ensure the appropriate file paths are set if replicating or running the notebooks:

- For **LOC.ipynb**: `metrics/comprehension_length_flattened.csv`
- For **NOL+NOCC.ipynb**: `metrics/loop_and_condition_flattened.csv`

---
