import ast
import operator

_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    raise ValueError("Unsupported expression")

def calculator_tool(query: str) -> str:
    import re
    match = re.search(r"\d+(\.\d+)?\s*[\+\-\*/]\s*\d+(\.\d+)?", query)

    if not match:
        return "Could not find a calculable expression."

    extracted = match.group().strip()
    print(f"DEBUG: extracted expression = '{extracted}'")  # temporary debug line

    try:
        tree = ast.parse(extracted, mode="eval")
        result = _eval_node(tree.body)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"