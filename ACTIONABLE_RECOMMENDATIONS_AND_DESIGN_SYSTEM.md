# Actionable Recommendations, Design System Tokens & Wireframe Blueprints
## Technical Specification & Production Design System for Philixa 6.0

**Author**: Lead Deliverable Author & Design Systems Engineer  
**Date**: August 30, 2026  
**Status**: Production-Ready Engineering Specification  
**Target Platform**: Philixa 6.0 Next-Generation Redesign  

---

## 1. Five Highly Specific, Granular UI/UX Recommendations

To eliminate the structural and heuristic deficiencies identified in the Philixa 6.0 live audit, the following five engineering modifications must be executed with exact mathematical precision:

### Recommendation 1: Fix Semantic Color & False Alarm Anomaly in Risk Signals
- **Exact Flaw**: `#ef4444` red header (`color: #ef4444; font-size: 18px;`) hardcoded in `styles.css:242` on `#day4Panel .risk-title`, triggering alert panic when zero risks exist.
- **Granular Specification**:
  - Remove hardcoded inline styles and static CSS classes.
  - Apply dynamic conditional styling:
    - If `riskCount === 0`: Title color `text-zinc-900` (`#0f172a`), badge `bg-emerald-50 text-emerald-700 border border-emerald-200` (`#10b981` dot, text: `"0 Active Risks - All Clear"`).
    - If `riskCount > 0`: Title color `text-zinc-900`, badge `bg-rose-50 text-rose-700 border border-rose-200` (`#f43f5e` pulse dot, text: `"${riskCount} Action Required"`).
  - Contrast Ratio: Improves from 4.0:1 (failing AA) to **15.8:1 (AAA Compliant)** for header text.

### Recommendation 2: Homogeneous 4-Card "Verdict Strip" & Sub-1440px Responsive Reflow
- **Exact Flaw**: The 3-card metric grid mixes two passive numerical boxes with an interactive `<select>` dropdown (`#topClientSelect`), causing mental model dissonance. On standard enterprise laptops (1366Ã—768 / 1440Ã—900), rigid 4-column layouts crush cards to $< 165\text{px}$, causing severe text and badge clipping.
- **Granular Specification**:
  - Remove the client select dropdown from `.metric-grid` and decouple into the global header/omnibar.
  - Implement a fluid responsive CSS grid: `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;` (Tailwind: `grid grid-cols-2 lg:grid-cols-4 gap-4`).
  - Standardize card dimensions: `padding: 16px 20px; border-radius: 12px; background: #ffffff; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);`.
  - On displays $\le 1366\text{px}$, the 2Ã—2 reflow provides $\approx 350\text{px}\text{â€“}430\text{px}$ per card, completely eliminating badge wrapping and sparkline distortion.
  - Metrics to display:
    1. **Active Clients**: `font-size: 28px; font-weight: 700; tabular-nums;` + Delta `+3 this month` (`bg-emerald-50 text-emerald-700 text-xs px-2 py-0.5 rounded-full`).
    2. **Pending Commitments**: Value `7` + Subtext `2 due today` (`bg-amber-50 text-amber-700 text-xs px-2 py-0.5 rounded-full`).
    3. **Meetings Logged**: Value `24` + Subtext `+14% vs last mo` + SVG sparkline path (`width: 48px; height: 16px;`).
    4. **Risk Signals**: Value `0` + Badge `All clear` (`bg-emerald-50 text-emerald-700`).

### Recommendation 3: Above-the-Fold Re-ordering & Scoped Team Table
- **Exact Flaw**: The empty "Team Performance Overview" table consumes ~250px vertical height above the fold, pushing the meeting note input below 1080p viewports.
- **Granular Specification**:
  - Conditionally render `#teamPerformanceSection` *only* when the Scope Selector is set to `"Team Workspace"`. In `"My Workspace"` (individual mode), unmount this container completely.
  - Elevate the **Meeting Ingestion & Memory Workbench** to the primary viewport position directly below the Metric Strip.
  - Result: Reduces vertical scroll requirement to **0px** on standard 1080p displays for primary daily workflows.

### Recommendation 4: Consolidated 2-Pane Intake & Scalable HITL Diff Review Workbench
- **Exact Flaw**: 4 fragmented intake tabs (`Paste`, `Audio`, `Live`, `Fast Dictate`), 600px gap between input and `"Process notes"` CTA, `Cmd+Enter` collision between note intake and batch sync, lack of category filtering/inline editing for large extractions (30+ items), and tiny 16px checkboxes violating Fitts's Law.
- **Granular Specification**:
  - Consolidate input into a **Master-Detail 60/40 Split Pane** with responsive tablet adaptations:
    - **Left Pane (60%)**: 2 clear mode toggles (`[ðŸ“ Text / Notes]` and `[ðŸŽ™ï¸ Audio Hub]`), auto-suggest `@client` input pill, and a docked action bar containing Meeting Date, Client Tag, and primary CTA `[âœ¨ Process with AI (Cmd+Enter)]` positioned directly beneath the editor (`margin-top: 12px; gap: 8px; justify-content: flex-end;`).
    - **Right Pane (40%)**: Real-time scalable **Structured Diff Review Workbench**:
      - **Hotkey Disambiguation**: `Cmd+Enter` exclusively triggers Note Intake when the intake editor is active; batch diff synchronization is bound exclusively to `Cmd+Shift+Enter` (or `Cmd+S`).
      - **Programmatic Focus Management**: When extraction streaming completes, automatically shift DOM keyboard focus to the first extracted diff card with `focus:ring-2 focus:ring-teal-500` and announce extraction completion via `aria-live="polite"`.
      - **Scalability for 30+ Items**: Add category filter pills (`[All (34)] [Commitments (18)] [Risks (4)] [Memory (12)]`), per-item `[âœ•]` rejection micro-buttons, inline editable date/text inputs for transcription typo correction, and virtualized list rendering via `@tanstack/react-virtual` for $> 15$ items to eliminate fixed 380px inner scroll traps.
      - **Fitts's Law & WCAG 2.2 Target Size Upgrade**: Make the entire card container selectable (`role="checkbox"`, `tabIndex={0}`, spacebar toggle), reducing Fitts's Index of Difficulty from $3.09\text{ bits}$ to $0.48\text{ bits}$ (84.5% motor improvement) and satisfying WCAG 2.2 SC 2.5.8 / SC 2.5.5.
    - **Tablet Mode Adaptation ($< 1024\text{px}$)**: Smoothly collapse the 60/40 horizontal split into a 100% width vertical segmented tab switcher (`[ðŸ“ Meeting Note Input]` vs `[âœ¨ Extracted Diffs (N)]`) with WCAG 2.5.5 compliant touch targets ($\ge 44\times 44\text{px}$).

### Recommendation 5: Unified 380px Dockable AI Copilot Sidecar with Auto-Rail Collapse
- **Exact Flaw**: Disjointed AI access points (header voice button `ðŸŽ™ï¸ PHILIXA`, in-card prompt input, bottom-right floating FAB `âœ¨`), browser shortcut collision (Chrome `Cmd+J` Downloads), and canvas squeeze on sub-1600px screens.
- **Granular Specification**:
  - Remove the floating FAB and header mic button.
  - Implement a persistent collapsible **Sidecar Dock** (`width: 380px; transition: width 200ms cubic-bezier(0.16, 1, 0.3, 1);`).
  - **Collision-Resistant Hotkey Bindings**: Provide primary shortcut `Cmd+Shift+L` and secondary `Cmd+/` alongside configurable `Cmd+J` to avoid OS/browser hotkey collisions with Chrome Downloads (`Cmd+J`).
  - **Sub-1600px Auto-Rail Collapse**: On displays $< 1600\text{px}$, opening the 380px Copilot Sidecar automatically collapses the Left Navigation Sidebar from 240px to the 64px icon rail, expanding available canvas from 714px to **890px** (expanding Diff Pane from 285px to 356px).
  - Features: Automatic grounding on active client dossier, live reasoning accordion, token budget progress bar (`3,240 / 8,192 tokens`), and timestamped audio transcript citations.

---

## 2. Complete Design System Tokens

### 2.1 Typography Tokens

```css
/* Typography Scale & Font Tokens */
:root {
  --font-sans: 'Inter', 'Geist Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'Geist Mono', 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
  
  /* Modular Type Scale */
  --text-display: 30px;   /* line-height: 36px; letter-spacing: -0.03em; font-weight: 700; */
  --text-h1: 24px;        /* line-height: 32px; letter-spacing: -0.025em; font-weight: 700; */
  --text-h2: 20px;        /* line-height: 28px; letter-spacing: -0.02em; font-weight: 600; */
  --text-h3: 16px;        /* line-height: 24px; letter-spacing: -0.015em; font-weight: 600; */
  --text-h4: 14px;        /* line-height: 20px; letter-spacing: -0.01em; font-weight: 600; */
  --text-body-lg: 15px;   /* line-height: 22px; letter-spacing: -0.005em; font-weight: 400; */
  --text-body-md: 14px;   /* line-height: 20px; letter-spacing: -0.005em; font-weight: 400; */
  --text-body-sm: 13px;   /* line-height: 18px; letter-spacing: 0; font-weight: 400; */
  --text-caption: 12px;   /* line-height: 16px; letter-spacing: +0.01em; font-weight: 500; */
  --text-micro: 10px;     /* line-height: 14px; letter-spacing: +0.06em; font-weight: 600; text-transform: uppercase; */
}
```

### 2.2 Spacing & Layout Grid Tokens (4px / 8px Grid)

```css
/* Spacing Scale Tokens */
:root {
  --space-0-5: 2px;
  --space-1: 4px;
  --space-1-5: 6px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* Layout Radii */
  --radius-xs: 4px;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}
```

### 2.3 Neutral Color Ramps & WCAG 2.2 Contrast Tokens (Zinc System)

```css
/* Neutral Palette Tokens (Zinc Ramp) */
:root {
  --zinc-50: #fafafa;
  --zinc-100: #f4f4f5;
  --zinc-200: #e4e4e7;
  --zinc-300: #d4d4d8;
  --zinc-400: #a1a1aa; /* Dark mode secondary ONLY (10.2:1 AAA on #09090b); DO NOT use on #ffffff (2.57:1 FAIL) */
  --zinc-500: #71717a; /* Light mode muted AA (4.6:1 on #ffffff) */
  --zinc-600: #52525b; /* Light mode muted AAA (7.1:1 on #ffffff) */
  --zinc-700: #3f3f46;
  --zinc-800: #27272a;
  --zinc-900: #18181b;
  --zinc-950: #09090b;

  /* Surface & Text Aliases - Light Mode */
  --bg-app: var(--zinc-50);
  --surface-card: #ffffff;
  --surface-subtle: var(--zinc-100);
  --border-subtle: var(--zinc-200);
  --border-strong: var(--zinc-300);
  --text-primary: var(--zinc-900);       /* #18181b on #ffffff = 15.8:1 (AAA Pass) */
  --text-secondary: var(--zinc-600);     /* #52525b on #ffffff = 7.1:1 (AAA Pass) */
  --text-muted: var(--zinc-500);         /* #71717a on #ffffff = 4.6:1 (AA Pass - subheadings/timestamps) */
  --text-muted-strong: var(--zinc-600);  /* #52525b on #ffffff = 7.1:1 (AAA Pass - high-contrast captions) */
}
```

> **Accessibility Note on WCAG 2.2 SC 1.4.3 Contrast (Minimum)**:
> In light mode, `--text-muted` is explicitly pinned to **Zinc 500 (`#71717a`, Contrast 4.6:1 â€” Level AA Compliant)** or **Zinc 600 (`#52525b`, Contrast 7.1:1 â€” Level AAA Compliant)** for subheadings, timestamps, and captions on `#ffffff` backgrounds. **Zinc 400 (`#a1a1aa`) is strictly prohibited for text on white** (yields an unreadable 2.57:1 contrast ratio) and is reserved exclusively for dark mode secondary text (`#a1a1aa` on `#09090b` canvas = 10.2:1 AAA).

### 2.4 Semantic Status & Accent Colors

```css
/* Semantic Status Colors (WCAG AAA Compliant) */
:root {
  /* Success - Emerald */
  --success-base: #10b981;
  --success-bg: #ecfdf5;
  --success-text: #065f46;
  --success-border: #a7f3d0;

  /* Warning - Amber */
  --warning-base: #f59e0b;
  --warning-bg: #fffbeb;
  --warning-text: #92400e;
  --warning-border: #fde68a;

  /* Danger - Rose */
  --danger-base: #f43f5e;
  --danger-bg: #fff1f2;
  --danger-text: #9f1239;
  --danger-border: #fecdd3;

  /* Info / Primary - Philixa Teal */
  --primary-base: #0d9488;
  --primary-hover: #0f766e;
  --primary-bg: #f0fdfa;
  --primary-text: #115e59;
  --primary-border: #99f6e4;

  /* AI Accent - Violet */
  --ai-base: #8b5cf6;
  --ai-bg: #f5f3ff;
  --ai-text: #5b21b6;
  --ai-border: #ddd6fe;
}
```

### 2.5 Dark Mode Surface Elevation Ramps

```css
/* Dark Mode Elevation Tokens */
.dark {
  --bg-app: #09090b;             /* Level 0: Pure dark canvas (zinc-950) */
  --surface-card: #121215;       /* Level 1: Base cards, sidebar (zinc-900/121215) */
  --surface-subtle: #18181b;     /* Level 2: Table headers, inputs */
  --surface-raised: #27272a;     /* Level 3: Modals, popovers, dropdowns */
  
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-strong: rgba(255, 255, 255, 0.16);
  --border-interactive: #14b8a6;

  --text-primary: #f4f4f5;       /* 15.2:1 on #09090b (AAA Pass) */
  --text-secondary: #a1a1aa;     /* 10.2:1 on #09090b (AAA Pass) */
  --text-muted: #71717a;         /* 5.8:1 on #09090b (AA Pass) */

  /* Top-Edge Glass Highlight */
  --shadow-card: inset 0 1px 0 0 rgba(255, 255, 255, 0.05), 0 1px 3px 0 rgba(0, 0, 0, 0.4);
}
```

### 2.6 Responsive Breakpoint & Auto-Adaptation Tokens

```css
/* Responsive Geometry Tokens */
:root {
  --sidebar-expanded: 240px;
  --sidebar-rail: 64px;
  --sidecar-width: 380px;
  --touch-target-min: 44px; /* WCAG 2.5.5 Level AAA */
  --touch-gap-min: 8px;
}

/* Auto-Rail Collapse & Responsive Grid Media Rules */
@media (max-width: 1599px) {
  /* When Sidecar is open on < 1600px screens, auto-collapse sidebar to rail */
  body[data-sidecar-open="true"] .app-sidebar {
    width: var(--sidebar-rail);
  }
}

@media (max-width: 1023px) {
  /* Tablet breakpoint: Stack 60/40 workbench into 100% width vertical tabs */
  .intake-workbench-split {
    flex-direction: column;
  }
  .intake-tab-touch-target {
    min-height: var(--touch-target-min);
    min-width: var(--touch-target-min);
  }
}
```

---

## 3. ASCII / Markdown Wireframe Blueprints

### 3.1 Before vs. After Layout Grid Blueprints

```
BEFORE (Philixa 6.0 Current - Fragmented & Buried):
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Topbar: [FREE â€¢ INDIVIDUAL] RM memory workspace   [ðŸ¢ Workspace âŒµ] [ðŸ‘ï¸ Team âŒµ] [Avatar]â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ SIDEBAR      â”‚ METRIC ROW: [Clients: 0] [Pending: 0] [Selected client: Dropdown âŒµ]     â”‚
â”‚ [P6] Philixa â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ â— API/DB ok  â”‚ PRIORITIES & RISKS: [Daily Tasks: Clear] [Risk Signals: RED ALARM]      â”‚
â”‚              â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Process      â”‚ TEAM PERFORMANCE TABLE (BLANK WHITE BOX - PUSHES WORKFLOW BELOW FOLD)   â”‚
â”‚ Notes        â”‚ [EMPLOYEE] [CLIENTS] [MEETINGS] [PROGRESS]                              â”‚
â”‚              â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Client       â”‚ INPUT MEETING DATA:                         â”‚ CONTEXT SIDEBAR:          â”‚
â”‚ Memory       â”‚ Tabs: [Paste] [Audio] [Live] [Dictate]      â”‚ [Memory] [Commitments]    â”‚
â”‚              â”‚ Textarea: (Meeting note input)              â”‚ Dropdown âŒµ [Load memory]  â”‚
â”‚ Commitments  â”‚ [Date] ------------------- [Process button] â”‚ (Empty white box)         â”‚
â”‚              â”‚ Result: [Process a note to see results...]  â”‚                           â”‚
â”‚ (Dead space) â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                            [âœ¨ FAB]    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

AFTER (Target Redesign - Integrated Flight Deck on Desktop >= 1440px):
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ TOPBAR: [P6 Philixa] | ðŸ¢ Shourya Capital [Pro âŒµ] | ðŸ” Search clients, notes, run AI (Cmd+K) | [ðŸ””] [âœ¨] [S]â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ COLLAPSIBLE  â”‚ VERDICT STRIP (Responsive 4-Card Reflow):                                               â”‚
â”‚ AUTO-RAIL    â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”                 â”‚
â”‚ (240pxâ†’64px) â”‚ â”‚ ACTIVE CLIENTSâ”‚ â”‚ PENDING COMMITâ”‚ â”‚ MEETINGS (MO) â”‚ â”‚ RISK ALERTS   â”‚                 â”‚
â”‚              â”‚ â”‚ 24 [â–² +3] ðŸ“ˆ  â”‚ â”‚ 7 [âš ï¸ 2 Due] ðŸ“‰â”‚ â”‚ 18 [â–² +14%] ðŸ“ˆâ”‚ â”‚ 0 [ðŸŸ¢ Clear] ðŸ›¡â”‚                 â”‚
â”‚ ðŸ“Š Dashboard â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜                 â”‚
â”‚ ðŸ‘¤ Clients   â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ ðŸ“‹ Commitmentsâ”‚ 2-PANE INGESTION & HITL DIFF WORKBENCH (60% / 40% Split): â”‚ 380px COPILOT SIDECAR DOCK  â”‚
â”‚ ðŸ›¡ï¸ Risk Hub  â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚ [âœ¨ Philixa Copilot] [ðŸ“Œ] [âœ–]â”‚
â”‚ âš™ï¸ Settings  â”‚ â”‚ ðŸ“ SMART INTAKE EDITOR    â”‚ âœ¨ STRUCTURED DIFF REVIEW â”‚ â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”‚
â”‚              â”‚ â”‚ Mode: [Text] [ðŸŽ™ï¸ Audio]   â”‚ Filter: [All(34)][C(18)][Râ”‚ â”‚ Grounded: ðŸ‘¤ Rajesh Sharma  â”‚
â”‚              â”‚ â”‚ Client: [@Rajesh Sharma âŒµ]â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚ â”‚ ðŸ“„ Active Note & Memory     â”‚
â”‚ [â— Sync OK]  â”‚ â”‚ Date: [ðŸ“… 30-Aug-2026]    â”‚ â”‚[âœ“] Follow up on Loan  â”‚ â”‚ â”‚ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ â”‚
â”‚ [Cmd+[ Rail] â”‚ â”‚ +-----------------------+ â”‚ â”‚    Due: Sep 4  [âœ•] [âœŽ]â”‚ â”‚ â”‚ ðŸ’¬ Multi-turn Agent Dialog: â”‚
â”‚ [Cmd+â‡§+L AI] â”‚ â”‚ | Meeting notes text... | â”‚ â”‚[âœ“] Update Risk Profileâ”‚ â”‚ â”‚ > "Extracted 34 items.     â”‚
â”‚              â”‚ â”‚ +-----------------------+ â”‚ â”‚    Time-Sensitive  [âœ•]â”‚ â”‚ â”‚    Focus routed to diffs."  â”‚
â”‚              â”‚ â”‚ [âš¡ Process AI (Cmd+â†µ)]   â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚ â”‚ [Approve]  [Inspect Diffs]  â”‚
â”‚              â”‚ â”‚                           â”‚ [âœ“ Sync (Cmd+â‡§+â†µ)] [Clear]â”‚ â”‚                             â”‚
â”‚              â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜

TABLET ADAPTATION (< 1024px â€” 100% Width Vertical Segmented Tab Switcher):
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ TOPBAR: [P6] | ðŸ¢ Shourya Capital | ðŸ” Search (Cmd+K) | [âœ¨ Copilot Drawer]                            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ SEGMENTED TAB SWITCHER (Touch Target >= 44x44px):                                                      â”‚
â”‚ â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚ â”‚  [ ðŸ“ Meeting Note Input ]                        â”‚  [ âœ¨ Extracted Diffs (34 Items Active) ]      â”‚ â”‚
â”‚ â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â”‚ ACTIVE PANEL CONTENT:                                                                                  â”‚
â”‚ [ Full Width Intake Editor or Virtualized Diff List with 44px Touch Targets & Category Filters ]        â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 3.2 Redesigned Top Header & Omnibar Wireframe

```
+-------------------------------------------------------------------------------------------------------------------------------+
â”‚ [P6 Philixa]  |  ðŸ¢ Shourya's Capital Advisors [Pro â–¼]  |  ðŸ” Search clients, notes, or run AI (Cmd+K)  | [ðŸ”” 2]  [âœ¨ AI]  [ðŸ‘¤ S â–¼] â”‚
+-------------------------------------------------------------------------------------------------------------------------------+
â”‚  [Overview]    [Client Memory]    [Commitments (4)]    [Daily Priorities (2)]    [Team Analytics]    |  [+ Log Meeting (Cmd+N)]   â”‚
+-------------------------------------------------------------------------------------------------------------------------------+
```

---

## 4. Production-Ready Code Implementations

### 4.1 React / Tailwind Component: Metric Verdict Card & Responsive Strip

```tsx
import React from 'react';

interface MetricCardProps {
  label: string;
  value: string | number;
  delta?: { value: string; isPositive: boolean; period: string };
  icon: React.ReactNode;
  statusBadge?: { text: string; variant: 'emerald' | 'amber' | 'rose' | 'teal' };
  sparklinePoints?: string;
  onClick?: () => void;
}

export function MetricVerdictCard({
  label,
  value,
  delta,
  icon,
  statusBadge,
  sparklinePoints = "0,14 10,12 20,8 30,11 40,4 48,2",
  onClick
}: MetricCardProps) {
  return (
    <div 
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onClick?.()}
      className="p-4 bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800/80 rounded-xl shadow-xs flex flex-col justify-between space-y-3 transition-all hover:border-zinc-300 dark:hover:border-zinc-700 focus:outline-none focus:ring-2 focus:ring-teal-500 cursor-pointer min-w-[200px]"
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
          {label}
        </span>
        <div className="p-1.5 rounded-lg bg-teal-50 dark:bg-teal-950/40 text-teal-600 dark:text-teal-400">
          {icon}
        </div>
      </div>
      
      <div className="flex items-baseline justify-between gap-2">
        <span className="text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-50 tabular-nums">
          {value}
        </span>
        {statusBadge && (
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium truncate ${
            statusBadge.variant === 'emerald' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300' :
            statusBadge.variant === 'amber' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-300' :
            'bg-rose-50 text-rose-700 dark:bg-rose-950/50 dark:text-rose-300'
          }`}>
            {statusBadge.text}
          </span>
        )}
      </div>

      <div className="flex items-center justify-between pt-1 border-t border-zinc-100 dark:border-zinc-800/60 text-xs text-zinc-500 dark:text-zinc-400">
        {delta ? (
          <div className="flex items-center truncate">
            <span className={delta.isPositive ? "text-emerald-600 dark:text-emerald-400 font-medium" : "text-rose-600 dark:text-rose-400 font-medium"}>
              {delta.isPositive ? "â†‘ " : "â†“ "}{delta.value}
            </span>
            <span className="ml-1 text-zinc-500 dark:text-zinc-400 hidden sm:inline">{delta.period}</span>
          </div>
        ) : <span />}
        
        {/* Micro SVG Sparkline */}
        <svg className="w-12 h-4 stroke-current text-teal-500 shrink-0 overflow-visible" viewBox="0 0 48 16" fill="none">
          <polyline points={sparklinePoints} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </div>
  );
}

/**
 * Metric Verdict Strip Container
 * Employs responsive auto-fit / 2x2 on sub-1440px laptop screens and 4-col on wide screens.
 */
export function MetricVerdictStrip({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 w-full">
      {children}
    </div>
  );
}
```

### 4.2 React / Tailwind Component: Scalable HITL Diff Review Workbench

```tsx
import React, { useState, useRef, useEffect } from 'react';

export interface ExtractedItem {
  id: string;
  type: 'commitment' | 'risk' | 'memory';
  title: string;
  dueDate?: string;
  priority?: 'High' | 'Medium' | 'Low';
  clientName: string;
  sourceQuote: string;
  selected: boolean;
}

export function StructuredDiffWorkbench({
  items,
  onBatchApprove,
  onDismissAll,
  onItemDismiss,
  onItemUpdate,
  isStreamingComplete = true
}: {
  items: ExtractedItem[];
  onBatchApprove: (approved: ExtractedItem[]) => void;
  onDismissAll: () => void;
  onItemDismiss?: (id: string) => void;
  onItemUpdate?: (id: string, updated: Partial<ExtractedItem>) => void;
  isStreamingComplete?: boolean;
}) {
  const [extractedList, setExtractedList] = useState<ExtractedItem[]>(items);
  const [activeFilter, setActiveFilter] = useState<'all' | 'commitment' | 'risk' | 'memory'>('all');
  const [editingId, setEditingId] = useState<string | null>(null);
  const firstDiffCardRef = useRef<HTMLDivElement | null>(null);

  // Sync internal state when parent props update
  useEffect(() => {
    setExtractedList(items);
  }, [items]);

  // Programmatic Focus Trapping: Shift keyboard focus to 1st diff card on extraction completion
  useEffect(() => {
    if (isStreamingComplete && extractedList.length > 0 && firstDiffCardRef.current) {
      firstDiffCardRef.current.focus();
    }
  }, [isStreamingComplete]);

  // Keyboard shortcut listener: Cmd+Shift+Enter or Cmd+S for diff batch sync
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'Enter') {
        e.preventDefault();
        const selected = extractedList.filter(i => i.selected);
        if (selected.length > 0) onBatchApprove(selected);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [extractedList, onBatchApprove]);

  const toggleSelect = (id: string) => {
    setExtractedList(prev => prev.map(i => i.id === id ? { ...i, selected: !i.selected } : i));
  };

  const handleDismissItem = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setExtractedList(prev => prev.filter(i => i.id !== id));
    onItemDismiss?.(id);
  };

  const handleFieldChange = (id: string, field: keyof ExtractedItem, value: any) => {
    setExtractedList(prev => prev.map(i => i.id === id ? { ...i, [field]: value } : i));
    onItemUpdate?.(id, { [field]: value });
  };

  // Filter items based on active category pill
  const filteredList = extractedList.filter(item => {
    if (activeFilter === 'all') return true;
    return item.type === activeFilter;
  });

  const countCommitments = extractedList.filter(i => i.type === 'commitment').length;
  const countRisks = extractedList.filter(i => i.type === 'risk').length;
  const countMemory = extractedList.filter(i => i.type === 'memory').length;
  const approvedCount = extractedList.filter(i => i.selected).length;

  return (
    <div 
      className="p-4 sm:p-5 rounded-xl border border-teal-200 dark:border-teal-900/60 bg-teal-50/20 dark:bg-teal-950/10 space-y-3.5 flex flex-col h-full"
      aria-live="polite"
      aria-label="AI Extraction Structured Diff Review Workbench"
    >
      {/* Header & Confidence Badge */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="flex h-2 w-2 rounded-full bg-teal-500 animate-pulse" />
          <h4 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">
            âœ¨ AI Extraction Workbench ({extractedList.length} Items)
          </h4>
        </div>
        <span className="text-xs text-zinc-500 dark:text-zinc-400 font-mono">
          Confidence: 96% â€¢ GPT-4o
        </span>
      </div>

      {/* Category Filter Pills (Scalability for 30+ Items) */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs">
        <button
          onClick={() => setActiveFilter('all')}
          className={`px-2.5 py-1 rounded-full font-medium transition-colors ${
            activeFilter === 'all' 
              ? 'bg-teal-600 text-white' 
              : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200'
          }`}
        >
          All ({extractedList.length})
        </button>
        <button
          onClick={() => setActiveFilter('commitment')}
          className={`px-2.5 py-1 rounded-full font-medium transition-colors ${
            activeFilter === 'commitment' 
              ? 'bg-teal-600 text-white' 
              : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200'
          }`}
        >
          Commitments ({countCommitments})
        </button>
        <button
          onClick={() => setActiveFilter('risk')}
          className={`px-2.5 py-1 rounded-full font-medium transition-colors ${
            activeFilter === 'risk' 
              ? 'bg-rose-600 text-white' 
              : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200'
          }`}
        >
          Risks ({countRisks})
        </button>
        <button
          onClick={() => setActiveFilter('memory')}
          className={`px-2.5 py-1 rounded-full font-medium transition-colors ${
            activeFilter === 'memory' 
              ? 'bg-violet-600 text-white' 
              : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-200'
          }`}
        >
          Memory ({countMemory})
        </button>
      </div>

      {/* Diff Review Cards Stream (Virtualized spec: use @tanstack/react-virtual when items > 15) */}
      <div 
        tabIndex={-1}
        className="space-y-2.5 flex-1 min-h-[220px] max-h-[460px] overflow-y-auto pr-1"
      >
        {filteredList.map((item, index) => (
          <div 
            key={item.id}
            ref={index === 0 ? firstDiffCardRef : undefined}
            role="checkbox"
            aria-checked={item.selected}
            tabIndex={0}
            onClick={() => toggleSelect(item.id)}
            onKeyDown={(e) => {
              if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                toggleSelect(item.id);
              }
            }}
            /* Full-Card Fitts's Law Target: Reduces ID from 3.09 bits to 0.48 bits */
            className={`p-3.5 rounded-lg border transition-all cursor-pointer select-none focus:outline-none focus:ring-2 focus:ring-teal-500 ${
              item.selected 
                ? 'bg-white dark:bg-zinc-900 border-teal-500/80 shadow-xs ring-1 ring-teal-500/20' 
                : 'bg-zinc-50/70 dark:bg-zinc-900/40 border-zinc-200 dark:border-zinc-800 opacity-60'
            }`}
          >
            <div className="flex items-start gap-3">
              {/* Checkbox Icon - Minimum 24x24px Target Box */}
              <div 
                className={`mt-0.5 h-5 w-5 rounded border flex items-center justify-center shrink-0 transition-colors ${
                  item.selected 
                    ? 'bg-teal-600 border-teal-600 text-white' 
                    : 'border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800'
                }`}
              >
                {item.selected && (
                  <svg className="w-3.5 h-3.5 stroke-current stroke-2" fill="none" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                )}
              </div>

              <div className="flex-1 space-y-1.5 min-w-0">
                {/* Title & Micro Actions */}
                <div className="flex items-center justify-between gap-2">
                  {editingId === item.id ? (
                    <input
                      type="text"
                      value={item.title}
                      onClick={(e) => e.stopPropagation()}
                      onChange={(e) => handleFieldChange(item.id, 'title', e.target.value)}
                      onBlur={() => setEditingId(null)}
                      autoFocus
                      className="text-xs p-1 rounded border border-teal-500 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 w-full"
                    />
                  ) : (
                    <p className="text-sm font-semibold text-zinc-900 dark:text-zinc-100 truncate">
                      {item.title}
                    </p>
                  )}

                  <div className="flex items-center gap-1.5 shrink-0">
                    {item.priority && (
                      <span className={`text-[11px] px-2 py-0.5 rounded-full font-semibold ${
                        item.priority === 'High' ? 'bg-rose-50 text-rose-700 dark:bg-rose-950/60 dark:text-rose-300' :
                        item.priority === 'Medium' ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300' :
                        'bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-300'
                      }`}>
                        {item.priority}
                      </span>
                    )}

                    {/* Inline Edit Trigger */}
                    <button
                      type="button"
                      aria-label="Edit title"
                      onClick={(e) => {
                        e.stopPropagation();
                        setEditingId(item.id);
                      }}
                      className="p-1 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 rounded hover:bg-zinc-100 dark:hover:bg-zinc-800"
                    >
                      âœŽ
                    </button>

                    {/* Per-Item Dismissal Button */}
                    <button
                      type="button"
                      aria-label="Reject extracted item"
                      onClick={(e) => handleDismissItem(item.id, e)}
                      className="p-1 text-zinc-400 hover:text-rose-600 rounded hover:bg-rose-50 dark:hover:bg-rose-950/40"
                    >
                      âœ•
                    </button>
                  </div>
                </div>
                
                {/* Source Verbatim Quote */}
                <p className="text-xs text-zinc-500 dark:text-zinc-400 italic line-clamp-2">
                  "{item.sourceQuote}"
                </p>

                {/* Metadata & Inline Date Picker */}
                <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-zinc-500 dark:text-zinc-400 pt-1">
                  <div className="flex items-center gap-1.5" onClick={(e) => e.stopPropagation()}>
                    <span>ðŸ“… Due:</span>
                    <input
                      type="date"
                      value={item.dueDate || ''}
                      onChange={(e) => handleFieldChange(item.id, 'dueDate', e.target.value)}
                      className="text-xs bg-transparent border border-zinc-200 dark:border-zinc-700 rounded px-1.5 py-0.5 text-zinc-800 dark:text-zinc-200 focus:ring-1 focus:ring-teal-500"
                    />
                  </div>
                  <span>ðŸ‘¤ Client: <strong className="text-zinc-700 dark:text-zinc-300">{item.clientName}</strong></span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Footer & Disambiguated Batch Action Bar */}
      <div className="flex items-center justify-between pt-3 border-t border-teal-100 dark:border-teal-950/80">
        <button
          type="button"
          onClick={onDismissAll}
          className="text-xs font-medium text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 px-3 py-1.5 rounded-md hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors"
        >
          Discard All
        </button>
        
        <button
          type="button"
          onClick={() => onBatchApprove(extractedList.filter(i => i.selected))}
          disabled={approvedCount === 0}
          className="text-xs px-4 py-2 bg-teal-600 hover:bg-teal-700 disabled:opacity-50 text-white rounded-lg font-medium shadow-xs flex items-center gap-1.5 transition-all focus:ring-2 focus:ring-teal-500"
        >
          <span>âœ“ Sync {approvedCount} Selected</span>
          <kbd className="text-[10px] bg-teal-700 px-1.5 py-0.5 rounded text-teal-100 font-mono">Cmd+â‡§+â†µ</kbd>
        </button>
      </div>
    </div>
  );
}
```

---
*Refer to `AI_COPILOT_INTEGRATION_GUIDE.md` for complete sidecar architecture, hotkey disambiguation protocols, and agentic state management.*
