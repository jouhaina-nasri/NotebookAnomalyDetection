## Overview

This directory contains three files related to managing and processing git repositories and `.ipynb` files:

1. `clone_project.py`: A Python script to clone git repositories.
2. `move_ipynb_files.py`: A Python script to move `.ipynb` files.
3. `nbcontents.csv`: A CSV file detailing various notebooks.

## Files

### 1. `clone_project.py`

This script provides a utility for cloning multiple git repositories from a list of repository URLs. The user can specify the output directory and the maximum number of repositories to clone.

**Key functionalities**:
- Clone repositories from a list of URLs to a designated output directory.
- Load repository URLs from the `nbcontents.csv` file.
- Extract unique repository URLs.
- Handle git errors during the cloning process.

### 2. `move_ipynb_files.py`

This script enables users to move all `.ipynb` notebook files from a specified source directory (and its sub-directories) to a destination directory.

**Key functionalities**:
- Transfer all `.ipynb` files from the source to the target directory.
- Address file-related errors such as "File Not Found" or "Permission Denied".

### 3. `nbcontents.csv`

This CSV file contains various columns describing individual notebooks. 
