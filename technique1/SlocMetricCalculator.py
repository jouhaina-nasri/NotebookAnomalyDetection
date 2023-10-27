from radon.raw import analyze

def count_source_lines_of_code(code_str: str) -> int:
    """
    Count the number of source lines of code (SLOC) in a given code string. 
    Excludes comments and empty lines.

    Args:
        code_str (str): The code string to count lines in.

    Returns:
        int: The number of lines of actual code in the string, 
             excluding comments and empty lines.

    Raises:
        ValueError: If the code string is not valid Python code.
    """
    try:
        analysis_result = analyze(code_str)
        return analysis_result.sloc
    except Exception as e:
        raise ValueError(f"An error occurred while analyzing the code: {e}")
    