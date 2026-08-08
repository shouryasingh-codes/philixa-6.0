with open('app/web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the flex wrapper entirely
html = html.replace('<div style="display: flex; justify-content: center; width: 100%; margin-bottom: 25px;">\n', '')
html = html.replace('        <div style="display: flex; justify-content: center; width: 100%; margin-bottom: 25px;">\n', '')

# 2. Remove the inline style from the panel section
html = html.replace(
    '<section class="panel primary-panel" id="notePanel" style="width: 100%; max-width: 1100px;">',
    '<section class="panel primary-panel" id="notePanel">'
)

# 3. Remove the closing </div> of the wrapper just before the bottom layout
# Note: we need to match the specific </div> that comes before <section class="grid-layout bottom-layout">
html = html.replace(
    '        </div>\n\n      <section class="grid-layout bottom-layout">',
    '      <section class="grid-layout bottom-layout">'
)

with open('app/web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
