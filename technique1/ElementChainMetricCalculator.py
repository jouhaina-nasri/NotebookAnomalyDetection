import ast
from typing import List

def calculate_nesting_value(node: ast.AST) -> int:
    """Calculate Data Nesting Complexity (DNC) for a given AST node."""
    if isinstance(node, (ast.List, ast.Set)):
        return 1 + max((calculate_nesting_value(elt) for elt in node.elts), default=0)
    elif isinstance(node, ast.Dict):
        return 1 + max((max(calculate_nesting_value(key), calculate_nesting_value(value)) for key, value in zip(node.keys, node.values)), default=0)
    else:
        return 0  # For non-container types

def extract_nesting_value(code: str) -> List[int]:
    """List DNCs for all nodes in the code."""
    tree = ast.parse(code)
    values = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.List, ast.Dict, ast.Set)):
            nested_value = calculate_nesting_value(node)
            if nested_value > 0:  # Consider all nested structures
                values.append(nested_value - 1)  # Subtract 1 to account for the container itself

    return sorted(set(values))

def calculate_element_count(node: ast.AST) -> int:
    """Calculate the number of elements for a container AST node."""
    if isinstance(node, (ast.List)):
        return len(node.elts)
    elif isinstance(node, ast.Set):
        return len(node.elts)
    elif isinstance(node, ast.Dict):
        return len([k for k in node.keys if k is not None])  # Filter out None keys
    return None

def extract_element_counts(code: str) -> List[int]:
    """Extract all element counts from a code string."""
    tree = ast.parse(code)
    all_counts = []

    for node in ast.walk(tree):
        count = calculate_element_count(node)
        if count is not None:
            all_counts.append(count)

    return sorted(set(all_counts))

