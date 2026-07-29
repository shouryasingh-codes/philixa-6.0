import os
import re

def replace_db_calls(content):
    # We want to replace db.execute, db.scalars, db.scalar, db.refresh, db.commit, db.get
    # For simple ones:
    content = content.replace("db.commit()", "await db.commit()")
    
    # For methods taking arguments, we find the method name, then find the matching closing parenthesis.
    methods_to_await = ["db.execute", "db.scalars", "db.scalar", "db.refresh", "db.get"]
    
    for method in methods_to_await:
        start_idx = 0
        while True:
            idx = content.find(method + "(", start_idx)
            if idx == -1:
                break
            
            # Find matching parenthesis
            paren_count = 0
            end_idx = -1
            for i in range(idx + len(method), len(content)):
                if content[i] == '(':
                    paren_count += 1
                elif content[i] == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        end_idx = i
                        break
            
            if end_idx != -1:
                original_call = content[idx:end_idx+1]
                
                # Check if it already has await
                prefix = content[max(0, idx-6):idx]
                if "await " not in prefix:
                    if method == "db.scalars":
                        # We need to wrap it in parens and add await if we intend to call .all() immediately.
                        # Actually wait, `db.scalars(stmt).all()` vs `(await db.scalars(stmt)).all()`
                        # If the next characters are `.all()`, we need `(await db.scalars(...)).all()`
                        # Let's check what comes after.
                        if content[end_idx+1:end_idx+7] == ".all()":
                            replacement = f"(await {original_call})"
                        else:
                            replacement = f"await {original_call}"
                    else:
                        replacement = f"await {original_call}"
                    
                    content = content[:idx] + replacement + content[end_idx+1:]
                    start_idx = idx + len(replacement)
                else:
                    start_idx = end_idx + 1
            else:
                start_idx = idx + len(method)
                
    return content

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    content = content.replace("from sqlalchemy.orm import Session", "from sqlalchemy.ext.asyncio import AsyncSession")
    if "from sqlalchemy.ext.asyncio import AsyncSession" not in content and "Session" in original:
        content = "from sqlalchemy.ext.asyncio import AsyncSession\n" + content
    
    content = re.sub(r"from sqlalchemy.orm import \n", "", content)
    content = content.replace("db: Session", "db: AsyncSession")
    content = content.replace("def list_clients(db: AsyncSession = Depends(get_db))", "async def list_clients(db: AsyncSession = Depends(get_db))")
    
    content = replace_db_calls(content)

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.lstrip().startswith('def ') and ('db: AsyncSession' in line or (i+1 < len(lines) and 'db: AsyncSession' in lines[i+1])):
            lines[i] = line.replace('def ', 'async def ', 1)
        if line.lstrip().startswith('def _') and ('db: AsyncSession' in line or (i+1 < len(lines) and 'db: AsyncSession' in lines[i+1])):
            lines[i] = line.replace('def ', 'async def ', 1)

    content = '\n'.join(lines)
    
    content = re.sub(r'(?<!await )_get_owned_client\(', r'await _get_owned_client(', content)
    content = re.sub(r'(?<!await )MemoryService\(\)\.get_client_memory\(', r'await MemoryService().get_client_memory(', content)
    content = re.sub(r'(?<!await )AskClientService\(\)\.ask\(', r'await AskClientService().ask(', content)
    content = re.sub(r'(?<!await )meeting_to_dict\(', r'await meeting_to_dict(', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

for root, dirs, files in os.walk(r"c:\Users\admin\Documents\philixa 6.0 2\app"):
    for file in files:
        if file.endswith('.py') and 'alembic' not in root:
            process_file(os.path.join(root, file))
