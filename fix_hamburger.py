with open('app/web/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '''      <div class="brand-block">
        <div class="brand-mark" id="logoToggleBtn" style="cursor:pointer;">P6</div>
        <div>
          <h1>PHILIXA 6.0</h1>
          <p>Commitment and Memory</p>
        </div>
      </div>'''

replace = '''      <div class="brand-block" style="display: flex; align-items: center; justify-content: space-between; white-space: nowrap; overflow: hidden; padding-right: 12px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div class="brand-mark" style="flex-shrink: 0; cursor: pointer;" id="logoToggleBtn">P6</div>
          <div class="brand-text">
            <h1>PHILIXA 6.0</h1>
            <p>Commitment and Memory</p>
          </div>
        </div>
        <button id="sidebarToggleBtn" class="hamburger-btn" title="Toggle Sidebar" type="button" style="flex-shrink: 0; background: transparent; color: var(--muted); border: none; cursor: pointer;">
          <svg focusable="false" aria-hidden="true" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
            <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"></path>
          </svg>
        </button>
      </div>'''

html = html.replace(target, replace)

bottom_btn = '''      <!-- Hamburger for collapsing -->
      <button id="sidebarToggleBtn" class="hamburger-btn" title="Toggle Sidebar" type="button" style="position: absolute; bottom: 20px; left: 20px; background: transparent; color: var(--muted); border: none; cursor: pointer;">
        <svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
          <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"></path>
        </svg>
      </button>'''

html = html.replace(bottom_btn, '')

with open('app/web/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
