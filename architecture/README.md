## Architecture of the Tool

Our tool follows a sequential process to analyze and detect 'smells' from a provided `.ipynb` file. Below is a breakdown of the entire workflow:

### 1. User Interface (UI)
- **Input**: Users upload or introduce their source code through a `.ipynb` file.
- **Action**: The file is then passed on to the AST Analyser.

### 2. AST Analyser
- **Input**: Receives the `.ipynb` source code.
- **Functionality**: 
  - Parses the code into its Abstract Syntax Tree (AST).
  - Traverses the AST to understand the code's structure and flow.
- **Output**: Extracted metrics from the AST, which are then sent to the Smell Detector.

### 3. Smell Detector
- **Input**: Metrics collected from the AST.
- **Functionality**:
  - Uses predefined rules that are based on the collected metrics.
  - Checks these rules to detect any 'smells' in the code.
- **Output**: If any 'smells' are found, they are compiled into a report.

### 4. Smell Report
- **Input**: Detected 'smells' from the Smell Detector.
- **Functionality**: The tool compiles a detailed report of all detected 'smells'.
- **Output**: Users receive the 'smell' report in the form of a `.csv` file which can be downloaded or viewed directly through the User Interface.

---

With this architecture, our tool provides an efficient and streamlined process to analyze and highlight potential 'smells' in the provided code. Users can quickly understand issues in their code and take corrective measures. 
