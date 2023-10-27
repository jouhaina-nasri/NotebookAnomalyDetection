import ast

def calculate_complexity(source_code):
    """
    Calculate the complexity of the given source code based on various AST nodes.

    Parameters:
        source_code (str): The source code to analyze.

    Returns:
        int: The calculated complexity.
    """

    # Initialize counters for different types of AST nodes
    metrics = {
        'functions': 0,
        'parameters': 0,
        'function_calls': 0,
        'imports': 0,
        'operations': 0
    }

    # Walk through each node in the AST
    for node in ast.walk(source_code):
        if isinstance(node, ast.FunctionDef):
            metrics['functions'] += 1
            metrics['parameters'] += len(node.args.args)
        elif isinstance(node, ast.Call):
            metrics['function_calls'] += 1
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            metrics['imports'] += 1
        elif isinstance(node, ast.BinOp) or isinstance(node, ast.UnaryOp):
            metrics['operations'] += 1

    # Calculate total complexity as the sum of individual metrics
    total_complexity = sum(metrics.values())

    return total_complexity
