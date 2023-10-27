import ast
from typing import List

def count_loops_in_comprehensions(ast_node: ast.AST) -> int:
    """Count the number of loops in list/set/dict comprehensions."""
    return sum(1 for node in ast.walk(ast_node) 
               if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)))

def count_conditions_in_comprehensions(ast_node: ast.AST) -> int:
    """Count the number of conditions in list/set/dict comprehensions."""
    return sum(len(generator.ifs) for node in ast.walk(ast_node) 
               if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)) 
               for generator in node.generators)

def count_loops_and_conditions_in_comprehensions(ast_node: ast.AST) -> List[int]:
    """Count the total number of loops and conditions in comprehensions."""
    return [count_loops_in_comprehensions(node) + 
            count_conditions_in_comprehensions(node) 
            for node in ast.walk(ast_node) 
            if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp))]

def extract_comprehension_code(code: str, node: ast.AST) -> List[str]:
    """Extract the source code corresponding to a list comprehension."""
    start, end = node.lineno, node.end_lineno
    start_col, end_col = node.col_offset, node.end_col_offset
    code_lines = code.splitlines()[start - 1:end]
    code_lines[0] = code_lines[0][start_col:]
    code_lines[-1] = code_lines[-1][:end_col]
    return code_lines
    
def calculate_comprehension_length(code: str, ast_node: ast.AST) -> List[int]:
    """Calculate the length in characters of each list comprehension."""
    lengths = []
    for node in ast.walk(ast_node):
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            comp_code = extract_comprehension_code(code, node)
            lengths.append(sum(len(line) for line in comp_code))
    return lengths

def count_conditions_per_comprehension(ast_node: ast.AST) -> List[int]:
    """Counts the number of 'if' conditions for each list/set/dict comprehension."""
    counts = []
    for node in ast.walk(ast_node):
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            count = sum(len(generator.ifs) for generator in node.generators)
            counts.append(count)
    return counts

def count_loops_per_comprehension(ast_node: ast.AST) -> List[int]:
    """Compte le nombre de boucles pour chaque compréhension de liste/set/dict."""
    counts = []
    for node in ast.walk(ast_node):
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            count = len(node.generators)
            counts.append(count)
    return counts
