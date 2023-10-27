# Code Smell Detection Project

This repository encompasses various scripts and tools designed for the evaluation and detection of "code smells" within software projects.

## Files and Their Descriptions

```plaintext
1. __main__.py
   - Purpose: Executes the Python parser.
   - Demonstration Video: main.mkv

2. app.py
   - Purpose: Backend component written in Flask.

3. interface
   - Purpose: Frontend component developed in React.

4. ComprehensionMetricCalculator.py
   - Purpose: Extracts metrics for the CCC (complex container comprehension) code smell.
   - Demonstration Video: comprehension.mkv

5. ConditionMetricCalculator.py
   - Purpose: Extracts metrics for the CIC (complex if condition) code smell.
   - Demonstration Video: condition.mkv

6. CyclomaticComplexityCalculator.py
   - Purpose: Extracts metrics for the LC (long cell) code smell.
   - Demonstration Video: cyclomaticcomplexity.mkv

7. detector.py
   - Purpose: Used to detect code smells (technique 1).
   - Demonstration Video: detector.mkv

8. ElementChainMetricCalculator.py
   - Purpose: Extracts metrics for the LEC (long element chain) code smell.
   - Demonstration Video: elementchain.mkv

9. ExpressionMetricCalculator.py
   - Purpose: Extracts metrics for the LE (long expression) code smell.
   - Demonstration Video: expression.mkv

10. FunctionnalComplexityCalculator.py
   - Purpose: Extracts metrics for the LC (long cell) code smell.
   - Demonstration Video: functionnalcomplexity.mkv

11. HalsteadMetricCalculator.py
   - Purpose: Extracts metrics for the LC (long cell) code smell.
   - Demonstration Video: halstead.mkv

12. OperandsMetricCalculator.py
   - Purpose: Extracts operand metrics.

13. OperatorsMetricCalculator.py
   - Purpose: Extracts operator metrics, which are used in HalsteadMetricCalculator.py.

14. python_parser.py
   - Purpose: The code source of python parser.
   - Demonstration Video: functionnalcomplexity.mkv

15. thresholds.json
   - Contains thresholds used for code smell detection.
