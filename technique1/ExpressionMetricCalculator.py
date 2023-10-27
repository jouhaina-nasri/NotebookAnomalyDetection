import ast
from typing import List

def extract_assignment_lengths(ast_node: ast.AST) -> List[int]:
    """
    Extracts the lengths of assignment expressions from an AST node, excluding docstrings.

    Args:
        ast_node (ast.AST): The AST node to search.

    Returns:
        List[int]: List of lengths of assignment expressions.
    """
    return [len(ast.unparse(node)) for node in ast.walk(ast_node)
            if isinstance(node, (ast.Assign, ast.Expr)) and not (isinstance(node.value, ast.Str) if hasattr(node, 'value') else False)]

def is_method_or_function_call(node):
    return isinstance(node, ast.Call)

def count_parameters_in_call(node):
    if is_method_or_function_call(node):
        return len(node.args) + len(node.keywords)
    return 0

def identify_args_per_expression(ast_node):
    args_counts = []
    for node in ast.walk(ast_node):
        if isinstance(node, ast.Module):
            for item in node.body:
                if isinstance(item, (ast.Assign,ast.Expr)):
                    total_parameters = sum(count_parameters_in_call(n) for n in ast.walk(item.value) if is_method_or_function_call(n))
                    if total_parameters > 0:
                        args_counts.append(total_parameters)
    return args_counts

def identify_methods_per_expression(ast_node):
    methods_counts = []
    for node in ast.walk(ast_node):
        if isinstance(node, ast.Module):
            for item in node.body:
                if isinstance(item, (ast.Assign,ast.Expr)):
                    total_methods = sum(1 for n in ast.walk(item.value) if is_method_or_function_call(n))
                    if total_methods > 0:
                        methods_counts.append(total_methods)
    return methods_counts

def identify_total_per_expression(ast_node):
    total_counts = []
    for node in ast.walk(ast_node):
        if isinstance(node, ast.Module):
            for item in node.body:
                if isinstance(item, (ast.Assign,ast.Expr)):
                    total_parameters = sum(count_parameters_in_call(n) for n in ast.walk(item.value) if is_method_or_function_call(n))
                    total_methods = sum(1 for n in ast.walk(item.value) if is_method_or_function_call(n))
                    total = total_parameters + total_methods
                    if total > 0:
                        total_counts.append(total)
    return total_counts

