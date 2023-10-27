import ast

def count_if_statements(root_ast_node: ast.AST) -> int:
    """Count the number of 'if' statements in the given AST node."""
    if not isinstance(root_ast_node, ast.AST):
        raise ValueError("Expected an AST node.")

    total_if_statements = 0
    for node in ast.walk(root_ast_node):
        if isinstance(node, ast.If):
            total_if_statements += 1

    return total_if_statements

def find_max_if_depths(root_ast_node: ast.AST, initial_depth: int = 0) -> list:
    """Find the maximum nested 'if' depths in the given AST node."""
    max_depths_per_branch = []

    if isinstance(root_ast_node, ast.If):
        new_depth = initial_depth + 1
        max_depths_in_then_branch = find_max_if_depths(root_ast_node.body, new_depth)
        max_depths_in_else_branch = find_max_if_depths(root_ast_node.orelse, new_depth)

        # Max depth for this specific 'if' block
        max_depth_for_this_if = max([new_depth] + max_depths_in_then_branch + max_depths_in_else_branch)
        max_depths_per_branch.append(max_depth_for_this_if)

    elif isinstance(root_ast_node, list):
        for child_node in root_ast_node:
            max_depths_per_branch += find_max_if_depths(child_node, initial_depth)

    else:
        for child_node in ast.iter_child_nodes(root_ast_node):
            max_depths_per_branch += find_max_if_depths(child_node, initial_depth)

    return max_depths_per_branch
