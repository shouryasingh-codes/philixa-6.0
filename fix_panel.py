with open('app/web/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = '''/* --- Highlighted Primary Panel --- */
.primary-panel {
    border: 2px solid var(--accent) !important;
    box-shadow: 0 16px 40px -12px rgba(20, 184, 166, 0.3), 0 4px 6px -1px rgba(0, 0, 0, 0.05);'''

replace = '''/* --- Highlighted Primary Panel --- */
.primary-panel {
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.08), 0 10px 15px -3px rgba(0, 0, 0, 0.03) !important;'''

if target in css:
    css = css.replace(target, replace)
    print("Replaced successfully")
else:
    print("Target NOT found")

with open('app/web/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
