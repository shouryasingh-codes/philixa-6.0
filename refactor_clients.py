import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content

    # Replace imports
    content = content.replace("from sqlalchemy.orm import Session", "from sqlalchemy.ext.asyncio import AsyncSession")
    if "from sqlalchemy.ext.asyncio import AsyncSession" not in content and "Session" in original:
        content = "from sqlalchemy.ext.asyncio import AsyncSession\n" + content
    
    # Clean up empty Session imports if it got split
    content = re.sub(r"from sqlalchemy.orm import \n", "", content)

    # Dependency Injection
    content = content.replace("db: Session =", "db: AsyncSession =")

    # DB Operations
    content = re.sub(r"db\.scalars\((.*?)\)", r"(await db.scalars(\1))", content)
    content = re.sub(r"db\.scalar\((.*?)\)", r"await db.scalar(\1)", content)
    content = re.sub(r"db\.execute\((.*?)\)", r"await db.execute(\1)", content)
    content = re.sub(r"db\.commit\(\)", r"await db.commit()", content)
    content = re.sub(r"db\.refresh\((.*?)\)", r"await db.refresh(\1)", content)
    content = re.sub(r"db\.get\((.*?)\)", r"await db.get(\1)", content)

    # Function def -> async def (if db: AsyncSession is an arg)
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('def ') and ('db: AsyncSession' in line or (i+1 < len(lines) and 'db: AsyncSession' in lines[i+1])):
            lines[i] = line.replace('def ', 'async def ', 1)
        # Also for internal helpers like _get_owned_client
        if line.startswith('def _') and ('db: AsyncSession' in line or (i+1 < len(lines) and 'db: AsyncSession' in lines[i+1])):
            lines[i] = line.replace('def ', 'async def ', 1)

    content = '\n'.join(lines)

    # Await custom helpers
    # Look for calls to these helpers. Simple approach:
    content = re.sub(r'(?<!await )_get_owned_client\(', r'await _get_owned_client(', content)
    
    # Replace Service calls with await
    content = re.sub(r'(?<!await )MemoryService\(\)\.get_client_memory\(', r'await MemoryService().get_client_memory(', content)
    content = re.sub(r'(?<!await )AskClientService\(\)\.ask\(', r'await AskClientService().ask(', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

process_file(r"c:\Users\admin\Documents\philixa 6.0 2\app\api\v1\routes_clients.py")
