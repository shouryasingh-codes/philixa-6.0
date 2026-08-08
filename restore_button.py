with open('app/web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove floating button from bottom
html = html.replace('''    <!-- Philixa Voice Assistant Floating Button -->
    <button id="philixaVoiceBtn" class="fab-voice-btn" title="Talk to Philixa" type="button">
      <div class="fab-icon">🎙️</div>
    </button>\n\n''', '')

# 2. Put it in the panel heading
heading_target = '''          <div class="panel-heading" style="padding-bottom: 0; border-bottom: none; margin-bottom: 25px; display: flex; align-items: center; justify-content: space-between; position: relative;">
            <div style="flex: 1; display: flex; justify-content: flex-start;">
              <h3 style="margin: 0;">Input Meeting Data</h3>
            </div>
            
            <div style="flex: 1; display: flex; justify-content: flex-end;">
              <select id="knownClient" style="width: auto;">
                <option value="">Auto identify client</option>
              </select>
            </div>
          </div>'''

heading_replace = '''          <div class="panel-heading" style="padding-bottom: 0; border-bottom: none; margin-bottom: 25px; display: flex; align-items: center; justify-content: space-between;">
            <div style="flex: 1; display: flex; justify-content: flex-start;">
              <h3 style="margin: 0;">Input Meeting Data</h3>
            </div>
            
            <div style="flex: 0 1 auto; display: flex; justify-content: center;">
              <!-- Philixa Copilot Box -->
              <button id="philixaVoiceBtn" class="copilot-box" title="Talk to Philixa" type="button">
                <span class="copilot-icon">🎙️</span>
                <span class="copilot-text" id="copilotText">PHILIXA</span>
              </button>
            </div>

            <div style="flex: 1; display: flex; justify-content: flex-end;">
              <select id="knownClient" style="width: auto;">
                <option value="">Auto identify client</option>
              </select>
            </div>
          </div>'''

html = html.replace(heading_target, heading_replace)

with open('app/web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
