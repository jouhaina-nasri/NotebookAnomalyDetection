# Project Documentation

This project consists of several directories, each serving a specific purpose. Below is a description of each directory:

## [architecture](./architecture)
This directory contains the architecture of technique 1.

## [boxplot](./boxplot)
Contains the distribution of metrics visualized as boxplots.

## [collect_data](./collect_data)
Houses the scripts used for collecting Jupyter Notebook files.

## [data](./data)
This is the directory where the physical Jupyter Notebook files are stored, which will be used for code smell detection.

## [extract_notebook](./extract_notebook)
Contains scripts used to read the content of a cell in a Jupyter Notebook file, which will then be used for manual labeling.

## [manual_labeling](./manual_labeling)
This directory contains the manual labeling as well as the script used to randomly collect cells.

## [metrics](./metrics)
Houses CSV files used to create boxplots.

## [precision_recall](./precision_recall)
This directory contains scripts used to evaluate the tool in relation to manual labeling.

## [technique1](./technique1)
Contains the Python parser used to extract metrics from scripts and the tool that detects code smells : Manual approach.

## [technique2](./technique2)
Contains the Python parser used to extract metrics from scripts and the model that detects code smells : Automatic approach.

## [validate](./validate)
Contains `.ipynb` files for evaluating the results.

