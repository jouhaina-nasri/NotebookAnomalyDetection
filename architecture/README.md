## Architecture of the Tool

Our tool follows a sequential process to analyze and detect 'semlls' from a provided `.ipynb` file. Below is a breakdown of the entire workflow:

### 1. User Interface (UI)
- **Input**: Users upload or introduce their source code through a `.ipynb` file.
- **Action**: The file is then passed on to the AST Analyser.

### 2. AST Analyser
- **Input**: Receives the `.ipynb` source code.
- **Functionality**: 
  - Parses the code into its Abstract Syntax Tree (AST).
  - Traverses the AST to understand the code's structure and flow.
- **Output**: Extracted metrics from the AST, which are then sent to the Semll Detector.

### 3. Semll Detector
- **Input**: Metrics collected from the AST.
- **Functionality**:
  - Uses predefined rules that are based on the collected metrics.
  - Checks these rules to detect any 'semlls' in the code.
- **Output**: If any 'semlls' are found, they are compiled into a report.

### 4. Semll Report
- **Input**: Detected 'semlls' from the Semll Detector.
- **Functionality**: The tool compiles a detailed report of all detected 'semlls'.
- **Output**: Users receive the 'semll' report in the form of a `.csv` file which can be downloaded or viewed directly through the User Interface.

---

With this architecture, our tool provides an efficient and streamlined process to analyze and highlight potential 'semlls' in the provided code. Users can quickly understand issues in their code and take corrective measures. 
