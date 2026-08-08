import re
with open('app/web/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove DOM queries
text = re.sub(r'\s*refreshAll: document\.querySelector\("#refreshAll"\),', '', text)
text = re.sub(r'\s*refreshClients: document\.querySelector\("#refreshClients"\),', '', text)
text = re.sub(r'\s*refreshPriorities: document\.querySelector\("#refreshPriorities"\),', '', text)

# Remove event listeners
text = re.sub(r'\s*els\.refreshAll\.addEventListener.*?catch.*?\);', '', text, flags=re.DOTALL)
text = re.sub(r'\s*els\.refreshClients\.addEventListener.*?catch.*?\);', '', text, flags=re.DOTALL)
text = re.sub(r'\s*els\.refreshPriorities\.addEventListener.*?catch.*?\);', '', text, flags=re.DOTALL)

with open('app/web/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
