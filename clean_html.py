import re

with open('app/web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Topbar actions: remove refreshAll and Swagger
topbar_target = r'''<div class="topbar-actions">
          <button id="settingsBtn" type="button" class="icon-btn" title="Notification Settings"
            style="font-size: 1.2rem; background: transparent; border: none; cursor: pointer; color: var\(--muted\); margin-right: 10px;">⚙️</button>
          <button id="refreshAll" type="button">Refresh</button>
          <a class="docs-link" href="/docs" target="_blank" rel="noreferrer">Swagger</a>
        </div>'''
topbar_replace = '''<div class="topbar-actions">
          <button id="settingsBtn" type="button" class="icon-btn" title="Notification Settings"
            style="font-size: 1.2rem; background: transparent; border: none; cursor: pointer; color: var(--muted); margin-right: 10px;">⚙️</button>
        </div>'''
html = re.sub(topbar_target, topbar_replace, html)

# 2. Day 4 tag and refresh button
html = re.sub(r'\s*<!-- Day 4: Follow-up and Risk Engine -->', '', html)
html = re.sub(r'\s*<p class="eyebrow">Day 4 .*?</p>', '', html)
html = re.sub(r'\s*<button id="refreshPriorities" type="button">Reload</button>', '', html)

# 3. Memory Index refresh button
html = re.sub(r'\s*<button id="refreshClients" type="button">Reload</button>', '', html)

# 4. Hero feature and Supporting view
html = re.sub(r'\s*<p class="eyebrow">Hero feature</p>', '', html)
html = re.sub(r'\s*<p class="eyebrow">Supporting view</p>', '', html)

with open('app/web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
