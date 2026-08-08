with open('app/web/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

target_keyframes = '''@keyframes magnetic-float {
  0% { 
    transform: scale(1) translateY(0); 
    box-shadow: 0 0 15px rgba(20, 184, 166, 0.4), inset 0 0 5px rgba(20, 184, 166, 0.2); 
  }
  50% { 
    transform: scale(1.03) translateY(-2px); 
    box-shadow: 0 8px 30px rgba(20, 184, 166, 0.8), inset 0 0 15px rgba(20, 184, 166, 0.4); 
    border-color: #2dd4bf;
  }
  100% { 
    transform: scale(1) translateY(0); 
    box-shadow: 0 0 15px rgba(20, 184, 166, 0.4), inset 0 0 5px rgba(20, 184, 166, 0.2); 
  }
}'''

replace_keyframes = '''@keyframes magnetic-float {
  0% { 
    transform: scale(1) translateY(0); 
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.05); 
  }
  50% { 
    transform: scale(1.02) translateY(-2px); 
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255, 255, 255, 0.1); 
    border-color: rgba(94, 234, 212, 0.6);
  }
  100% { 
    transform: scale(1) translateY(0); 
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.05); 
  }
}'''

target_hover = '''.copilot-box:hover {
  animation: none !important;
  box-shadow: 0 10px 40px rgba(20, 184, 166, 1) !important;
  border-color: #5eead4 !important;
  transform: scale(1.06) translateY(-3px) !important;
  color: #ffffff !important;
}'''

replace_hover = '''.copilot-box:hover {
  animation: none !important;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3) !important;
  border-color: rgba(94, 234, 212, 0.8) !important;
  transform: scale(1.04) translateY(-3px) !important;
  color: #ffffff !important;
}'''

if target_keyframes in css:
    css = css.replace(target_keyframes, replace_keyframes)
    print("Keyframes replaced.")
else:
    print("Keyframes NOT FOUND")

if target_hover in css:
    css = css.replace(target_hover, replace_hover)
    print("Hover replaced.")
else:
    print("Hover NOT FOUND")

with open('app/web/styles.css', 'w', encoding='utf-8') as f:
    f.write(css)
