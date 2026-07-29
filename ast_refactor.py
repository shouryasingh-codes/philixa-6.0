import ast
import os

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    if "db" not in source and "Session" not in source:
        return

    tree = ast.parse(source)

    # We need to collect:
    # 1. Functions to make async
    # 2. DB calls to wrap in await
    # 3. Service calls to wrap in await
    
    functions_to_async = []
    db_calls_to_await = []
    
    class Visitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            # Check if args has db: Session
            has_db = False
            for arg in node.args.args:
                if arg.arg == 'db' or (arg.annotation and getattr(arg.annotation, 'id', '') in ('Session', 'AsyncSession')):
                    has_db = True
            
            # Check if it uses db inside
            uses_db = False
            for child in ast.walk(node):
                if isinstance(child, ast.Name) and child.id == 'db':
                    uses_db = True
                    
            if has_db or uses_db:
                functions_to_async.append(node)
                
            self.generic_visit(node)
            
        def visit_Call(self, node):
            # Check for db.scalars, db.scalar, db.execute, db.commit, db.refresh, db.get
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                if node.func.value.id == 'db' and node.func.attr in ('scalars', 'scalar', 'execute', 'commit', 'refresh', 'get', 'delete'):
                    db_calls_to_await.append(node)
            
            self.generic_visit(node)

    Visitor().visit(tree)
    
    # We will do text replacement from bottom to top to avoid line/col offsets changing!
    # Wait, ast gives lineno and col_offset.
    # Actually, replacing text based on AST line/col is tricky because of multi-line expressions.
    # But we can just use the line numbers to guide regexes!
