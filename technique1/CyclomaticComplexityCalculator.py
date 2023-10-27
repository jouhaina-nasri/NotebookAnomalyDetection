import ast
from radon.complexity import cc_visit

def calculate_cyclomatic_complexity(source_code):
    """
    Calculate the cyclomatic complexity of the given source code.
    
    Parameters:
        source_code (str): The Python source code as a string.
    
    Returns:
        int: The cyclomatic complexity of the source code.
        
    Raises:
        RuntimeError: If the cyclomatic complexity calculation fails.
        
    Note:
        Cyclomatic Complexity = Edges - Nodes + 2 * Connected Components
    """
    
    try:
        # Calculate cyclomatic complexity using Radon's cc_visit method
        calculated_complexity = sum(cc.complexity for cc in cc_visit(source_code))
        
        return calculated_complexity
        
    except Exception as error:
        raise RuntimeError(f"Failed to calculate cyclomatic complexity: {str(error)}")
