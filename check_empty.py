import ast

with open('c:/Users/admin/Documents/app_dump.txt', 'r', encoding='utf-16') as f:
    content = f.read()

files = content.split('\n=== ')
for file_block in files:
    if not file_block.strip():
        continue
    lines = file_block.split('\n')
    filepath = lines[0].strip(' =')
    code = '\n'.join(lines[1:])
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                body = node.body
                if len(body) == 1 and isinstance(body[0], ast.Pass):
                    print(f"Empty Function: {node.name} in {filepath}")
                elif len(body) == 1 and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                    print(f"Empty Function (only docstring): {node.name} in {filepath}")
                elif any(isinstance(b, ast.Raise) and (isinstance(b.exc, ast.Name) and b.exc.id == 'NotImplementedError' or (isinstance(b.exc, ast.Call) and isinstance(b.exc.func, ast.Name) and b.exc.func.id == 'NotImplementedError')) for b in body):
                    print(f"NotImplemented: {node.name} in {filepath}")
    except Exception as e:
        pass
