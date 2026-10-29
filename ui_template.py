MESA_HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>CS2 // SKIN & INVENTORY LOADER</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

  :root {
    /* ARCEUS MONOCHROME — PURE BLACK & STARK WHITE PRO CHEAT UI */
    --bg-root: #050505;
    --bg-sidebar: #090909;
    --bg-header: #090909;
    --bg-card: #0E0E0E;
    --bg-card-hover: #151515;
    --bg-input: #060606;

    --line: #1B1B1B;
    --line-mid: #2C2C2C;
    --line-hi: #484848;

    --white: #FFFFFF;
    --white-soft: #E5E5E5;
    --white-tint: rgba(255, 255, 255, 0.06);
    --white-tint-hi: rgba(255, 255, 255, 0.11);

    --text-hi: #FFFFFF;
    --text-mid: #8E8E93;
    --text-lo: #4A4A4F;

    --radius: 4px;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    user-select: none;
  }

  html, body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: var(--bg-root);
    color: var(--text-hi);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 12px;
    display: flex;
    -webkit-font-smoothing: antialiased;
    border: 1px solid #27272a;
    box-sizing: border-box;
    user-select: none;
    -webkit-app-region: no-drag !important;
  }

  .app, .sidebar, .main, .content, .catalog-scroll, .content-scroll, .inventory-container,
  .overlay-backdrop, .config-dialog, .sticker-modal-dialog, .skin-card, .lo-card,
  .cfg-body, .cfg-left, .cfg-right, .cfg-stage, .cfg-stickers-box {
    -webkit-app-region: no-drag !important;
  }

  /* MINIMAL MONOCHROME SCROLLBAR */
  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: var(--bg-root); }
  ::-webkit-scrollbar-thumb { background: #262626; border-radius: 2px; }
  ::-webkit-scrollbar-thumb:hover { background: #555555; }

  /* ===================== SIDEBAR (204px, ZERO SCROLL) ===================== */
  .sidebar {
    width: 204px;
    height: 100%;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--line);
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    overflow: hidden;
  }

  .brand {
    height: 48px;
    padding: 0 10px;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, transparent 100%);
    display: flex;
    align-items: center;
    gap: 9px;
    flex-shrink: 0;
    position: relative;
    cursor: pointer;
    -webkit-app-region: drag;
  }

  .brand-emblem {
    width: 32px;
    height: 32px;
    border-radius: 4px;
    background: radial-gradient(circle at 50% 50%, #1c1c1c 0%, #080808 100%);
    border: 1px solid var(--line-mid);
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.09), inset 0 0 6px rgba(255, 255, 255, 0.04);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    position: relative;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .brand-emblem:hover {
    transform: scale(1.06);
    border-color: var(--white);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.35);
  }

  .brand-logo {
    width: 24px;
    height: 24px;
    object-fit: contain;
    display: block;
    filter: brightness(0) invert(1) drop-shadow(0 0 6px rgba(255, 255, 255, 0.4));
    transition: transform 0.2s ease;
  }

  .brand-text-wrap {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 2px;
    min-width: 0;
  }

  .brand-name {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #ffffff;
    line-height: 1;
  }

  .brand-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5px;
    font-weight: 600;
    letter-spacing: 1.2px;
    color: var(--text-mid);
    text-transform: uppercase;
  }

  .nav-section-lbl {
    padding: 10px 14px 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 600;
    letter-spacing: 1.4px;
    color: var(--text-lo);
    text-transform: uppercase;
  }

  .nav-list {
    flex: 1;
    padding: 2px 8px;
    display: flex;
    flex-direction: column;
    gap: 2px;
    overflow: hidden;
  }

  .nav-item {
    height: 32px;
    padding: 0 10px;
    background: transparent;
    border: 1px solid transparent;
    border-radius: var(--radius);
    color: var(--text-mid);
    display: flex;
    align-items: center;
    gap: 9px;
    cursor: pointer;
    position: relative;
    transition: background 0.1s ease, color 0.1s ease, border-color 0.1s ease;
  }

  .nav-item:hover {
    background: #121212;
    color: var(--white);
  }

  .nav-item.active {
    background: var(--white-tint);
    border-color: var(--line-mid);
    color: var(--white);
  }

  .nav-item.active::before {
    content: "";
    position: absolute;
    left: -1px;
    top: 6px;
    bottom: 6px;
    width: 2px;
    background: var(--white);
  }

  .nav-icon {
    width: 23px;
    height: 14px;
    object-fit: contain;
    filter: brightness(0) invert(0.52);
    flex-shrink: 0;
    transition: filter 0.1s ease;
  }

  .nav-item:hover .nav-icon,
  .nav-item.active .nav-icon {
    filter: brightness(0) invert(1);
  }

  .nav-label {
    font-size: 11.5px;
    font-weight: 600;
    flex: 1;
    text-align: left;
  }

  .nav-item.active .nav-label {
    color: var(--white);
    font-weight: 700;
  }

  .nav-cnt {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-lo);
  }

  .nav-item.active .nav-cnt {
    color: var(--white);
  }

  /* SIDEBAR FOOTER — CHEAT TELEMETRY & LOADOUT */
  .sidebar-footer {
    padding: 8px 10px 10px;
    border-top: 1px solid var(--line);
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .arceus-lore-box {
    background: #060606;
    border: 1px solid var(--line);
    border-left: 2px solid var(--white);
    border-radius: var(--radius);
    padding: 5px 8px;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .lore-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
  }

  .lore-k {
    color: var(--text-lo);
    font-weight: 700;
    letter-spacing: 0.8px;
  }

  .lore-v {
    color: var(--text-mid);
    font-weight: 600;
    letter-spacing: 0.5px;
  }

  .telemetry-card {
    background: var(--bg-input);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 6px 8px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .bridge-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--text-mid);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .bridge-pill.connected {
    color: var(--white);
  }

  .bridge-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: var(--text-lo);
    flex-shrink: 0;
  }

  .bridge-pill.connected .bridge-dot {
    background: var(--white);
    box-shadow: 0 0 6px rgba(255, 255, 255, 0.8);
  }

  .step-mini-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 3px;
  }

  .step-chip {
    height: 15px;
    border-radius: 2px;
    background: #0C0C0C;
    border: 1px solid var(--line);
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5px;
    font-weight: 600;
    color: var(--text-lo);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .step-chip.ok {
    background: var(--white);
    border-color: var(--white);
    color: #050505;
    font-weight: 700;
  }

  .loadout-trigger {
    width: 100%;
    height: 32px;
    background: var(--bg-card);
    border: 1px solid var(--line-mid);
    border-radius: var(--radius);
    color: var(--white);
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 10px;
    cursor: pointer;
    transition: all 0.1s ease;
  }

  .loadout-trigger:hover {
    background: var(--bg-card-hover);
    border-color: var(--line-hi);
  }

  .loadout-trigger.active {
    background: var(--white);
    color: #050505;
    border-color: var(--white);
  }

  .loadout-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    padding: 1px 6px;
    background: #1A1A1A;
    color: var(--white);
    border-radius: 2px;
  }

  .loadout-trigger.active .loadout-badge {
    background: #050505;
    color: var(--white);
  }

  /* ===================== MAIN STAGE ===================== */
  .main-stage {
    flex: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--bg-root);
    position: relative;
  }

  /* ARCEUS CELESTIAL WATERMARK */
  .main-stage::before {
    content: "";
    position: absolute;
    inset: 0;
    background: url('/assets/arceus_terminal_pillars_master.jpg') right bottom / cover no-repeat;
    opacity: 0.22;
    pointer-events: none;
    z-index: 0;
    transition: opacity 0.4s ease;
  }

  .stage-header {
    height: 48px;
    padding: 0 12px;
    background: var(--bg-header);
    border-bottom: 1px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    position: relative;
    z-index: 10;
    user-select: none;
    -webkit-app-region: drag;
    flex-wrap: nowrap;
    overflow: hidden;
  }

  .stage-header button, .stage-header input, .stage-header select, .stage-header a {
    -webkit-app-region: no-drag;
  }

  .header-left-zone {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    -webkit-app-region: no-drag;
  }

  .header-center-zone {
    display: flex;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;
    -webkit-app-region: no-drag;
  }

  .header-right-zone {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
    -webkit-app-region: no-drag;
  }

  .win-controls {
    display: flex;
    align-items: center;
    gap: 4px;
    border-left: 1px solid var(--line);
    padding-left: 6px;
    margin-left: 4px;
    -webkit-app-region: no-drag;
  }

  .win-btn {
    width: 24px;
    height: 22px;
    background: #0d0d0f;
    border: 1px solid #27272a;
    border-radius: 2px;
    color: #a1a1aa;
    font-size: 11px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s ease;
    font-family: 'JetBrains Mono', monospace;
  }

  .win-btn:hover {
    background: #ffffff;
    color: #050505;
    border-color: #ffffff;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
  }

  .win-btn.win-close:hover {
    background: #e11d48 !important;
    color: #ffffff !important;
    border-color: #f43f5e !important;
    box-shadow: 0 0 8px rgba(225, 29, 72, 0.6) !important;
  }

  .header-hud-badge {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .hud-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    font-weight: 600;
    color: #888;
    letter-spacing: 0.6px;
    padding: 2px 5px;
    border: 1px solid var(--line);
    border-radius: 2px;
    background: #080808;
    white-space: nowrap;
  }

  .hud-grid-toggle {
    height: 22px;
    padding: 0 5px;
    background: #0a0a0a;
    border: 1px solid var(--line-mid);
    border-radius: 2px;
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.12s ease;
  }

  .hud-grid-toggle:hover {
    border-color: var(--white);
    color: var(--white);
  }

  .hud-grid-toggle.active {
    background: var(--white);
    border-color: var(--white);
    color: #000;
  }

  /* --- MINIMALIST ARCEUS INTRO (PURE B&W // 5.0s) --- */
  .arceus-boot-screen {
    position: fixed;
    inset: 0;
    z-index: 100000;
    background: #030304;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    user-select: none;
    -webkit-app-region: drag;
    transition: opacity 0.5s ease, filter 0.5s ease;
  }

  .arceus-boot-screen.dismissed {
    opacity: 0;
    filter: blur(10px);
    pointer-events: none;
  }

  .boot-center-frame {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 320px;
  }

  .boot-logo-wrap {
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .boot-emblem-img {
    width: 56px;
    height: 56px;
    object-fit: contain;
    filter: brightness(0) invert(1) drop-shadow(0 0 16px rgba(255, 255, 255, 0.5));
    animation: bootLogoPulse 2.4s ease-in-out infinite;
  }

  @keyframes bootLogoPulse {
    0%, 100% { transform: scale(0.97); opacity: 0.9; }
    50% { transform: scale(1.03); opacity: 1; filter: brightness(0) invert(1) drop-shadow(0 0 24px rgba(255, 255, 255, 0.85)); }
  }

  .boot-brand {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 12px;
    color: #ffffff;
    text-indent: 12px;
    text-align: center;
    margin-top: 16px;
  }

  .boot-tagline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 600;
    letter-spacing: 4px;
    color: #52525b;
    margin-top: 6px;
    text-align: center;
    text-indent: 4px;
  }

  .boot-progress-wrap {
    width: 260px;
    margin-top: 36px;
  }

  .boot-progress-bar {
    width: 100%;
    height: 2px;
    background: #141418;
    border-radius: 1px;
    overflow: hidden;
  }

  .boot-progress-fill {
    width: 0%;
    height: 100%;
    background: #ffffff;
    box-shadow: 0 0 8px #ffffff;
    transition: width 0.08s linear;
  }

  .boot-progress-stats {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    color: #52525b;
    margin-top: 8px;
    letter-spacing: 0.8px;
  }

  .boot-pct {
    color: #ffffff;
    font-weight: 700;
  }

  /* SCANLINE / TACTICAL GRID OVERLAY (TOGGLEABLE) */
  .tactical-grid-overlay {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 9999;
    background: linear-gradient(rgba(18, 18, 18, 0) 50%, rgba(0, 0, 0, 0.28) 50%), linear-gradient(90deg, rgba(255, 255, 255, 0.015), rgba(0, 0, 0, 0.02) 100%);
    background-size: 100% 3px, 6px 100%;
    opacity: 0;
    transition: opacity 0.2s ease;
  }
  .tactical-grid-overlay.active {
    opacity: 1;
  }

  @keyframes arceus-flash {
    0% { box-shadow: inset 0 0 0 0 rgba(255, 255, 255, 0.8); }
    50% { box-shadow: inset 0 0 100px 30px rgba(255, 255, 255, 0.2); }
    100% { box-shadow: inset 0 0 0 0 rgba(255, 255, 255, 0); }
  }
  .judgment-pulse {
    animation: arceus-flash 0.6s ease-out;
  }

  .back-btn {
    height: 28px;
    padding: 0 10px;
    background: var(--bg-card);
    border: 1px solid var(--line-mid);
    border-radius: var(--radius);
    color: var(--text-mid);
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    display: none;
    align-items: center;
    gap: 5px;
    transition: all 0.1s ease;
  }

  .back-btn:hover {
    border-color: var(--white);
    color: var(--white);
  }

  .stage-title {
    display: none !important;
  }

  .ctrl-input, .ctrl-select {
    height: 26px;
    background: var(--bg-input);
    border: 1px solid var(--line-mid);
    border-radius: var(--radius);
    color: var(--white);
    padding: 0 8px;
    font-family: 'Inter', sans-serif;
    font-size: 10.5px;
    outline: none;
    transition: border-color 0.1s ease;
  }

  .ctrl-input { width: 125px; }
  .ctrl-input::placeholder { color: var(--text-lo); }
  .ctrl-select { width: 105px; }
  .ctrl-input:focus, .ctrl-select:focus {
    border-color: var(--white);
  }

  /* LOADOUT SUB-TABS */
  .loadout-tabs {
    height: 36px;
    padding: 0 16px;
    background: var(--bg-header);
    border-bottom: 1px solid var(--line);
    display: none;
    align-items: center;
    gap: 6px;
    flex-shrink: 0;
  }

  .lo-tab {
    height: 24px;
    padding: 0 10px;
    background: transparent;
    border: 1px solid transparent;
    border-radius: var(--radius);
    color: var(--text-mid);
    font-family: 'Inter', sans-serif;
    font-size: 10.5px;
    font-weight: 600;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.1s ease;
  }

  .lo-tab:hover {
    color: var(--white);
  }

  .lo-tab.active {
    background: var(--white);
    color: #050505;
    border-color: var(--white);
    font-weight: 700;
  }

  /* VIEW 1: WEAPON MODELS GRID (5x4, ZERO SCROLL IN 900x580) */
  .models-grid {
    flex: 1;
    padding: 12px 16px;
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    grid-auto-rows: 113px;
    gap: 8px;
    align-content: start;
    overflow: hidden;
  }

  .model-card {
    background: var(--bg-card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    cursor: pointer;
    position: relative;
    transition: background 0.12s ease, border-color 0.12s ease, transform 0.12s ease;
  }

  .model-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--white);
    transform: translateY(-1px);
  }

  .model-top-row {
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }

  .model-cnt {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 600;
    color: var(--text-lo);
  }

  .model-card:hover .model-cnt {
    color: var(--white);
  }

  .model-img-wrap {
    height: 56px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .model-img {
    max-width: 86%;
    max-height: 52px;
    object-fit: contain;
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.8));
    transition: transform 0.14s ease;
  }

  .model-card:hover .model-img {
    transform: scale(1.05);
  }

  .model-footer {
    width: 100%;
    border-top: 1px solid var(--line);
    padding-top: 5px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .model-name {
    font-size: 11px;
    font-weight: 600;
    color: var(--white);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* VIEW 2: SKINS GRID (4 COLUMNS, CLEAN MONOCHROME CARDS) */
  .skins-grid {
    flex: 1;
    overflow-y: auto;
    padding: 12px 16px;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    grid-auto-rows: 150px;
    gap: 8px;
    align-content: start;
  }

  .skin-card {
    background: var(--bg-card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 8px 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    cursor: pointer;
    position: relative;
    transition: background 0.12s ease, border-color 0.12s ease, transform 0.12s ease;
  }

  .skin-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--white);
    transform: translateY(-1px);
  }

  .skin-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-lo);
  }

  .rarity-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--rarity-col, #FFFFFF);
    display: inline-block;
  }

  .st-tag {
    padding: 0 4px;
    border: 1px solid var(--line-mid);
    border-radius: 2px;
    color: var(--white-soft);
    font-size: 8px;
    font-weight: 600;
  }

  .skin-img-box {
    height: 78px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .skin-img {
    max-width: 90%;
    max-height: 72px;
    object-fit: contain;
    filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.85));
    transition: transform 0.14s ease;
  }

  .skin-card:hover .skin-img {
    transform: scale(1.05);
  }

  .skin-card-bottom {
    border-top: 1px solid var(--line);
    padding-top: 5px;
  }

  .skin-wep-sub {
    font-size: 9.5px;
    font-weight: 500;
    color: var(--text-mid);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .skin-title {
    font-size: 11.5px;
    font-weight: 700;
    color: var(--white);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-top: 1px;
  }

  /* VIEW 3: LOADOUT GRID */
  .loadout-grid {
    flex: 1;
    overflow-y: auto;
    padding: 12px 16px;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    grid-auto-rows: 94px;
    gap: 8px;
    align-content: start;
  }

  .lo-card {
    background: var(--bg-card);
    border: 1px solid var(--line);
    border-left: 2px solid var(--white);
    border-radius: var(--radius);
    padding: 8px 11px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .lo-card:hover {
    border-color: var(--line-hi);
    border-left-color: var(--white);
  }

  .lo-thumb {
    width: 74px;
    height: 72px;
    background: var(--bg-input);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .lo-thumb img {
    max-width: 88%;
    max-height: 58px;
    object-fit: contain;
  }

  .lo-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .lo-wep {
    font-size: 9.5px;
    font-weight: 600;
    color: var(--text-mid);
    text-transform: uppercase;
  }

  .lo-name {
    font-size: 12px;
    font-weight: 700;
    color: var(--white);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .lo-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-mid);
    display: flex;
    gap: 6px;
  }

  .lo-meta-pill {
    padding: 1px 5px;
    background: var(--bg-input);
    border: 1px solid var(--line);
    border-radius: 2px;
  }

  .lo-stickers {
    display: flex;
    gap: 4px;
    margin-top: 3px;
  }

  .lo-stk {
    width: 22px;
    height: 17px;
    background: var(--bg-input);
    border: 1px solid var(--line);
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .lo-stk.filled { border-color: var(--white); }
  .lo-stk img { max-width: 18px; max-height: 14px; object-fit: contain; }

  .lo-del-btn {
    height: 26px;
    padding: 0 9px;
    background: transparent;
    border: 1px solid var(--line-mid);
    border-radius: var(--radius);
    color: var(--text-mid);
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.1s ease;
  }

  .lo-del-btn:hover {
    background: var(--white);
    border-color: var(--white);
    color: #050505;
  }

  /* ===================== CONFIGURATOR MODAL (MONOCHROME CHEAT) ===================== */
  .overlay-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.82);
    backdrop-filter: blur(6px);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 100;
  }

  .config-dialog {
    width: 650px;
    background: var(--bg-sidebar);
    border: 1px solid var(--line-mid);
    border-top: 2px solid var(--white);
    border-radius: var(--radius);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .cfg-top {
    height: 38px;
    padding: 0 14px;
    border-bottom: 1px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }

  .cfg-top-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    color: var(--text-lo);
    letter-spacing: 0.8px;
    margin-right: auto;
    margin-left: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .cfg-top-pill {
    padding: 1px 5px;
    border-radius: 2px;
    background: #080808;
    border: 1px solid var(--line);
    color: var(--text-mid);
  }

  .cfg-head-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--white);
    text-transform: uppercase;
  }

  .cfg-close {
    height: 22px;
    padding: 0 8px;
    background: var(--bg-card);
    border: 1px solid var(--line-mid);
    border-radius: 2px;
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    cursor: pointer;
  }

  .cfg-close:hover {
    color: #050505;
    background: var(--white);
    border-color: var(--white);
  }

  .cfg-body {
    padding: 14px;
    display: flex;
    gap: 14px;
  }

  .cfg-left {
    width: 275px;
    display: flex;
    flex-direction: column;
    gap: 9px;
    flex-shrink: 0;
  }

  .cfg-stage {
    height: 140px;
    background: radial-gradient(circle 110px at 50% 50%, rgba(255, 255, 255, 0.05), var(--bg-input) 82%);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    position: relative;
    overflow: hidden;
  }

  .name-chip-row {
    display: flex;
    gap: 4px;
    margin-top: 2px;
  }

  .cfg-stage img {
    max-width: 90%;
    max-height: 120px;
    object-fit: contain;
    filter: drop-shadow(0 10px 18px rgba(0, 0, 0, 0.85));
  }

  .cfg-inspect-btn {
    position: absolute;
    bottom: 7px;
    right: 7px;
    height: 21px;
    padding: 0 7px;
    border-radius: 2px;
    background: #111111;
    border: 1px solid var(--line-mid);
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 600;
    cursor: pointer;
  }

  .cfg-inspect-btn:hover {
    border-color: var(--white);
    color: var(--white);
  }

  .cfg-stickers-box {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .cfg-lbl-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10px;
    font-weight: 600;
    color: var(--text-mid);
    text-transform: uppercase;
  }

  .cfg-lbl-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    color: var(--white);
  }

  /* 4 STICKER SLOTS DIRECTLY UNDER SKIN BOX */
  .cfg-stk-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }

  .cfg-stk-slot {
    height: 48px;
    background: #0d0d10;
    border: 1px solid #27272a;
    border-radius: 3px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: relative;
    transition: all 0.12s ease;
  }

  .cfg-stk-slot:hover {
    border-color: #ffffff;
    background: #18181c;
  }

  .cfg-stk-slot.active-slot {
    border-color: #ffffff;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
  }

  .cfg-stk-slot.has-stk {
    border-color: #52525b;
    background: #121215;
  }

  .cfg-stk-slot img { max-width: 32px; max-height: 28px; object-fit: contain; }
  .cfg-stk-slot span {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    color: var(--text-lo);
  }

  .stk-rm-btn {
    position: absolute;
    top: 2px;
    right: 2px;
    width: 13px;
    height: 13px;
    background: var(--bg-sidebar);
    color: var(--text-mid);
    border: 1px solid var(--line-mid);
    border-radius: 2px;
    font-size: 8px;
    cursor: pointer;
  }

  .stk-rm-btn:hover {
    background: var(--white);
    color: #050505;
    border-color: var(--white);
  }

  .stk-transform-panel {
    background: var(--bg-input);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 7px 9px;
    display: none;
    flex-direction: column;
    gap: 5px;
  }

  .stk-tr-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
  }

  .cfg-right {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .cfg-item-header {
    border-bottom: 1px solid var(--line);
    padding-bottom: 7px;
  }

  .cfg-wep-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    color: var(--text-mid);
    text-transform: uppercase;
  }

  .cfg-skin-name {
    font-size: 16px;
    font-weight: 800;
    color: var(--white);
    margin-top: 2px;
  }

  /* MONOCHROME WEAR TRACK & REAL-CS2 PILLS */
  .wear-spectrum-bar {
    height: 4px;
    width: 100%;
    background: linear-gradient(90deg, 
      #FFFFFF 0%, #FFFFFF 7%, 
      #D4D4D8 7%, #D4D4D8 15%, 
      #8E8E93 15%, #8E8E93 38%, 
      #52525B 38%, #52525B 45%, 
      #27272A 45%, #27272A 100%);
    border-radius: 2px;
    margin: 4px 0 6px;
    position: relative;
  }

  .wear-pointer {
    position: absolute;
    top: -4px;
    width: 3px;
    height: 12px;
    background: #FFFFFF;
    box-shadow: 0 0 6px #FFFFFF;
    transform: translateX(-50%);
    left: 0.1%;
    pointer-events: none;
    border-radius: 1px;
  }

  .wear-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px;
    margin-top: 4px;
  }

  .wear-pill {
    height: 26px;
    border-radius: 2px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.12s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    text-transform: uppercase;
  }

  /* WEAR VISUAL DEGRADATION (PURE WHITE -> CHARCOAL ASH) */
  .wear-pill.wear-fn {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.85);
    color: #FFFFFF;
  }
  .wear-pill.wear-mw {
    background: rgba(228, 228, 231, 0.08);
    border: 1px solid rgba(228, 228, 231, 0.5);
    color: #E4E4E7;
  }
  .wear-pill.wear-ft {
    background: rgba(161, 161, 170, 0.06);
    border: 1px solid rgba(161, 161, 170, 0.35);
    color: #A1A1AA;
  }
  .wear-pill.wear-ww {
    background: rgba(113, 113, 122, 0.04);
    border: 1px solid rgba(113, 113, 122, 0.25);
    color: #71717A;
  }
  .wear-pill.wear-bs {
    background: rgba(82, 82, 91, 0.03);
    border: 1px solid rgba(82, 82, 91, 0.18);
    color: #52525B;
  }

  .wear-pill:hover:not(:disabled) {
    border-color: #FFFFFF;
    color: #FFFFFF;
  }

  /* ACTIVE STATE: SOLID PURE WHITE INVERSION */
  .wear-pill.active {
    background: #FFFFFF !important;
    border-color: #FFFFFF !important;
    color: #050505 !important;
    font-weight: 800 !important;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
  }

  /* DISABLED STATE: BLOCKED BECAUSE INEXISTENT IN CS2 FOR THIS SKIN */
  .wear-pill.wear-disabled, .wear-pill:disabled {
    opacity: 0.18 !important;
    cursor: not-allowed !important;
    pointer-events: none !important;
    background: #09090b !important;
    border-color: #27272a !important;
    color: #3f3f46 !important;
    box-shadow: none !important;
  }

  .seed-chip-row {
    display: flex;
    gap: 4px;
  }

  .seed-chip {
    padding: 1px 5px;
    border-radius: 2px;
    background: var(--bg-input);
    border: 1px solid var(--line);
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 600;
    cursor: pointer;
  }

  .seed-chip:hover {
    border-color: var(--white);
    color: var(--white);
  }

  /* MONOCHROME RANGE SLIDER */
  input[type="range"] {
    -webkit-appearance: none;
    appearance: none;
    width: 100%;
    height: 4px;
    background: #1E1E1E;
    border-radius: 2px;
    outline: none;
    cursor: pointer;
    margin: 4px 0;
  }

  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 12px;
    height: 12px;
    border-radius: 2px;
    background: var(--white);
    border: 1px solid #050505;
    cursor: pointer;
  }

  .cfg-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }

  .cfg-input {
    height: 28px;
    width: 100%;
    background: var(--bg-input);
    border: 1px solid var(--line-mid);
    border-radius: var(--radius);
    color: var(--white);
    padding: 0 9px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    outline: none;
  }

  .cfg-input:focus { border-color: var(--white); }

  .btn-add-ingame {
    margin-top: auto;
    height: 36px;
    width: 100%;
    background: var(--white);
    border: 1px solid var(--white);
    border-radius: var(--radius);
    color: #050505;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    cursor: pointer;
    transition: background 0.1s ease;
  }

  .btn-add-ingame:hover {
    background: #DCDCDC;
  }

  /* STICKER PICKER MODAL */
  .sticker-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.86);
    backdrop-filter: blur(6px);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 200;
  }

  .sticker-dialog {
    width: 560px;
    height: 395px;
    background: var(--bg-sidebar);
    border: 1px solid var(--line-mid);
    border-top: 2px solid var(--white);
    border-radius: var(--radius);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .stk-search-wrap {
    padding: 9px 12px;
    background: var(--bg-input);
    border-bottom: 1px solid var(--line);
  }

  .stk-picker-grid {
    flex: 1;
    overflow-y: auto;
    padding: 10px 12px;
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    grid-auto-rows: 96px;
    gap: 7px;
    align-content: start;
  }

  .stk-item {
    background: var(--bg-card);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 6px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    cursor: pointer;
  }

  .stk-item:hover { border-color: var(--white); background: var(--bg-card-hover); }
  .stk-item img { max-width: 54px; max-height: 46px; object-fit: contain; }
  .stk-item-title {
    font-size: 9px;
    color: var(--white);
    width: 100%;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* MONOCHROME TOAST */
  .toast {
    position: fixed;
    bottom: 12px;
    right: 12px;
    background: #0B0B0B;
    border: 1px solid var(--line-mid);
    border-left: 3px solid var(--white);
    border-radius: var(--radius);
    padding: 9px 13px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--white);
    display: none;
    z-index: 300;
  }

  /* --- SIDEBAR MID ACTIONS (INVENTAIRE UNDER ITEMS) --- */
  .sidebar-mid-actions {
    padding: 6px 10px 8px;
    border-top: 1px solid var(--line);
  }

  /* --- SIDEBAR USER PROFILE CARD --- */
  .sidebar-profile-card {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 6px 8px;
    background: #0d0d10;
    border: 1px solid #222226;
    border-radius: var(--radius);
    cursor: pointer;
    transition: all 0.12s ease;
  }
  .sidebar-profile-card:hover {
    background: #15151a;
    border-color: #3f3f46;
  }
  .profile-avatar-wrap {
    position: relative;
    width: 28px;
    height: 28px;
    flex-shrink: 0;
  }
  .profile-avatar-img {
    width: 28px;
    height: 28px;
    border-radius: 4px;
    object-fit: cover;
    background: #18181b;
    border: 1px solid #27272a;
  }
  .profile-status-indicator {
    position: absolute;
    bottom: -1px;
    right: -1px;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #ffffff;
    border: 1.5px solid #0d0d10;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.7);
  }
  .profile-meta {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .profile-name {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: var(--white);
    letter-spacing: 0.3px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .profile-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    color: var(--text-dim);
    letter-spacing: 0.4px;
    text-transform: uppercase;
  }
  .profile-arrow {
    color: var(--text-dim);
    display: flex;
    align-items: center;
    transition: color 0.12s ease, transform 0.12s ease;
  }
  .sidebar-profile-card:hover .profile-arrow {
    color: var(--white);
    transform: translateX(2px);
  }

  /* --- PROFILE DETAIL MODAL --- */
  .profile-dialog {
    width: 480px;
    max-width: 95vw;
    background: #09090b;
    border: 1px solid #27272a;
    border-radius: 6px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.85);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: cfgPop 0.15s ease-out;
  }

  .profile-modal-body {
    padding: 16px 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .profile-header-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 12px 14px;
    background: #111114;
    border: 1px solid #222226;
    border-radius: 4px;
  }

  .profile-hero-avatar-wrap {
    position: relative;
    width: 50px;
    height: 50px;
    flex-shrink: 0;
  }

  .profile-hero-avatar {
    width: 50px;
    height: 50px;
    border-radius: 6px;
    object-fit: cover;
    background: #18181b;
    border: 1px solid #3f3f46;
  }

  .profile-hero-badge {
    position: absolute;
    bottom: -3px;
    right: -3px;
    background: var(--white);
    color: #050505;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    font-weight: 800;
    padding: 1px 4px;
    border-radius: 2px;
    letter-spacing: 0.5px;
  }

  .profile-hero-details {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .profile-hero-name-row {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .profile-hero-name {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    font-weight: 800;
    color: var(--white);
    letter-spacing: 0.4px;
  }

  .profile-hero-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 700;
    background: #27272a;
    color: #a1a1aa;
    padding: 2px 5px;
    border-radius: 2px;
    letter-spacing: 0.5px;
  }

  .profile-hero-steamid {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #71717a;
    letter-spacing: 0.4px;
  }

  .profile-hero-vac {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #ffffff;
    display: flex;
    align-items: center;
    gap: 5px;
    font-weight: 600;
    letter-spacing: 0.3px;
  }

  .profile-stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
  }

  .profile-stat-card {
    background: #0d0d10;
    border: 1px solid #1f1f23;
    border-radius: 4px;
    padding: 8px 6px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  .pstat-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 700;
    color: var(--white);
  }

  .pstat-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 8px;
    font-weight: 600;
    color: #71717a;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    line-height: 1.2;
  }

  .profile-info-section {
    background: #0d0d10;
    border: 1px solid #1f1f23;
    border-radius: 4px;
    padding: 4px 12px;
    display: flex;
    flex-direction: column;
  }

  .pinfo-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 0;
    border-bottom: 1px solid #18181c;
  }
  .pinfo-row:last-child {
    border-bottom: none;
  }

  .pinfo-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    font-weight: 600;
    color: #a1a1aa;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }

  .pinfo-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--white);
    font-weight: 600;
  }

  .pinfo-input {
    background: #141418;
    border: 1px solid #27272a;
    border-radius: 3px;
    color: var(--white);
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 600;
    padding: 2px 6px;
    width: 120px;
    text-align: right;
    outline: none;
    transition: border-color 0.12s ease;
  }
  .pinfo-input:focus {
    border-color: var(--white);
  }

  .profile-actions-row {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
    margin-top: 2px;
  }

  .paction-btn {
    height: 28px;
    padding: 0 10px;
    background: #18181c;
    border: 1px solid #27272a;
    border-radius: 3px;
    color: #e4e4e7;
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: all 0.12s ease;
  }
  .paction-btn:hover {
    background: #222228;
    border-color: #3f3f46;
    color: var(--white);
  }
  .paction-btn-primary {
    background: var(--white);
    color: #050505;
    border-color: var(--white);
  }
  .paction-btn-primary:hover {
    background: #e4e4e7;
    color: #050505;
  }


  .profile-hero-avatar-wrap:hover .profile-hero-avatar {
    border-color: var(--white);
    filter: brightness(1.15);
  }


    /* ==========================================================================
     ARCEUS SEAMLESS TERMINAL & PILLARS LOGIN (ZERO DELIMITATION)
     ========================================================================== */
  .arceus-login-screen {
    position: fixed;
    inset: 0;
    z-index: 99990;
    background: #0a0a0c url('/assets/arceus_terminal_pillars_master.jpg') center center / cover no-repeat;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    user-select: none;
    border: none !important;
    outline: none !important;
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .arceus-login-screen.dismissed {
    opacity: 0;
    transform: scale(1.015);
    pointer-events: none;
  }

  .login-header-bar {
    height: 42px;
    background: transparent;
    border: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 18px;
    cursor: default;
    z-index: 10;
  }

  .login-bar-left {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .login-badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
    animation: vacPulse 2s infinite ease-in-out;
  }

  .login-title-txt {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.45);
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  .login-win-controls {
    display: flex;
    align-items: center;
    gap: 4px;
    -webkit-app-region: no-drag !important;
    pointer-events: auto !important;
    position: relative;
    z-index: 999999 !important;
  }

  .login-win-controls .win-btn {
    -webkit-app-region: no-drag !important;
    pointer-events: auto !important;
    position: relative;
    z-index: 999999 !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: none !important;
    color: rgba(255, 255, 255, 0.65) !important;
    font-size: 13px;
    width: 28px;
    height: 26px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    cursor: pointer !important;
    transition: background 0.15s ease, color 0.15s ease;
  }

  .login-win-controls .win-btn:hover {
    background: rgba(255, 255, 255, 0.08) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: none !important;
  }

  .login-win-controls .win-btn.win-btn-close:hover {
    background: rgba(225, 29, 72, 0.28) !important;
    color: #ff4d6d !important;
    border: none !important;
    box-shadow: none !important;
  }

  .login-inner-stage {
    position: relative;
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 64px 28px;
    z-index: 5;
  }

  /* --- REFINED STEALTH TERMINAL LOGIN CARD (ZERO LOGO, PURE LOGIN) --- */
  .login-terminal-card {
    position: relative;
    z-index: 10;
    width: 300px;
    background: rgba(10, 10, 14, 0.50);
    backdrop-filter: blur(32px);
    -webkit-backdrop-filter: blur(32px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 24px 20px 20px;
    box-shadow: 0 32px 80px rgba(0, 0, 0, 0.85), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    display: flex;
    flex-direction: column;
    animation: cfgPop 0.25s ease-out;
  }

  .login-stealth-form {
    display: flex;
    flex-direction: column;
    gap: 13px;
    width: 100%;
  }

  .login-field-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
    text-align: left;
  }

  .login-label-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .login-field-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 700;
    letter-spacing: 1.2px;
    color: rgba(255, 255, 255, 0.40);
    text-transform: uppercase;
  }

  .login-quick-dev-btn {
    background: none;
    border: none;
    padding: 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    font-weight: 600;
    letter-spacing: 0.8px;
    color: rgba(255, 255, 255, 0.35);
    cursor: pointer;
    transition: color 0.12s ease;
  }

  .login-quick-dev-btn:hover {
    color: #ffffff;
  }

  .login-field-input-wrap {
    position: relative;
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    transition: border-color 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
  }

  .login-field-input-wrap:focus-within {
    border-color: rgba(255, 255, 255, 0.35);
    background: rgba(255, 255, 255, 0.045);
    box-shadow: 0 0 16px rgba(255, 255, 255, 0.05);
  }

  .login-field-input-wrap.has-error {
    border-color: #ff4d6d !important;
    animation: loginShake 0.3s ease;
  }

  .login-prompt-glyph {
    position: absolute;
    left: 11px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.25);
    pointer-events: none;
    transition: color 0.15s ease;
  }

  .login-field-input-wrap:focus-within .login-prompt-glyph {
    color: #ffffff;
  }

  .login-field-input {
    width: 100%;
    height: 36px;
    padding: 0 12px 0 28px;
    background: transparent;
    border: none;
    outline: none;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11.5px;
    color: #ffffff;
    letter-spacing: 0.4px;
  }

  .login-field-input::placeholder {
    color: rgba(255, 255, 255, 0.18);
    font-size: 10.5px;
    letter-spacing: 0.5px;
  }

  .login-error-msg {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    color: #ff4d6d;
    letter-spacing: 0.5px;
    display: none;
    padding: 6px 10px;
    background: rgba(255, 77, 109, 0.08);
    border: 1px solid rgba(255, 77, 109, 0.25);
    border-radius: 6px;
    text-align: center;
    animation: cfgPop 0.15s ease;
  }

  .login-stealth-submit {
    margin-top: 5px;
    width: 100%;
    height: 38px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 6px;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    cursor: pointer;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  }

  .login-stealth-submit:hover {
    background: #ffffff;
    border-color: #ffffff;
    color: #000000;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(255, 255, 255, 0.20);
  }

  .login-stealth-submit:active {
    transform: translateY(0);
  }

  .login-loading-phase {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 10px 16px;
    animation: cfgPop 0.2s ease;
  }

  .login-loading-spinner {
    width: 32px;
    height: 32px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    margin-bottom: 14px;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
  }

  .login-loading-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 1.5px;
    margin-bottom: 4px;
  }

  .login-loading-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    color: rgba(255, 255, 255, 0.4);
    letter-spacing: 0.8px;
    margin-bottom: 16px;
  }

  .login-loading-bar-wrap {
    width: 100%;
    height: 3px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 2px;
    overflow: hidden;
  }

  .login-loading-bar-fill {
    height: 100%;
    width: 0%;
    background: #ffffff;
    border-radius: 2px;
    transition: width 0.12s ease;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
  }

  /* --- RICH CARD STAGGER & HOVER MICRO-ANIMATIONS --- */
  @keyframes cardFadeIn {
    0% {
      opacity: 0;
      transform: translateY(12px) scale(0.97);
    }
    100% {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  .model-card, .skin-card, .lo-card {
    background: rgba(16, 16, 20, 0.6) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 8px !important;
    position: relative;
    overflow: hidden;
    animation: cardFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
    animation-delay: calc(var(--i, 0) * 0.018s);
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.2s ease,
                border-color 0.22s ease,
                box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* Shimmer light reflection sweep on card hover */
  .model-card::after, .skin-card::after, .lo-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: -150%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.07), transparent);
    transform: skewX(-25deg);
    transition: left 0.65s ease;
    pointer-events: none;
  }

  .model-card:hover::after, .skin-card:hover::after, .lo-card:hover::after {
    left: 200%;
  }

  .model-card:hover, .skin-card:hover, .lo-card:hover {
    transform: translateY(-4px) scale(1.015) !important;
    background: rgba(28, 28, 35, 0.82) !important;
    border-color: rgba(255, 255, 255, 0.45) !important;
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 255, 255, 0.08) !important;
  }

  .model-img, .skin-img {
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), filter 0.28s ease;
  }

  .model-card:hover .model-img, .skin-card:hover .skin-img {
    transform: scale(1.08) rotate(-1deg);
    filter: drop-shadow(0 8px 18px rgba(255, 255, 255, 0.16));
  }

  /* Smooth Nav Item Slide & Glow */
  .nav-item {
    transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.15s ease,
                color 0.15s ease,
                border-color 0.15s ease,
                padding-left 0.18s ease;
  }
  .nav-item:hover {
    transform: translateX(4px);
    padding-left: 14px;
    background: rgba(255, 255, 255, 0.06);
    color: #ffffff;
  }
  .nav-item.active {
    background: rgba(255, 255, 255, 0.09) !important;
    border-left: 2px solid #ffffff !important;
    color: #ffffff !important;
    box-shadow: inset 4px 0 14px rgba(255, 255, 255, 0.06);
  }

  /* Tactile Button Press Ripple */
  button:active, .model-card:active, .skin-card:active {
    transform: scale(0.97) !important;
    transition: transform 0.06s ease !important;
  }


  /* --- ARCEUS AUTHENTIC HIGH-DENSITY ASCII ART WALKER --- */
  .arceus-walker-lane {
    position: absolute;
    bottom: 15px;
    left: 0;
    width: 100%;
    height: 255px;
    pointer-events: none;
    z-index: 2; /* Behind .login-terminal-card (which is z-index: 10) */
    overflow: hidden;
  }

  .arceus-walker-entity {
    position: absolute;
    bottom: 0;
    display: flex;
    animation: arceusTraverseRightToLeft 32s linear infinite;
    will-change: transform;
    transform: translateZ(0);
  }

  @keyframes arceusTraverseRightToLeft {
    0% {
      transform: translateX(1020px);
    }
    100% {
      transform: translateX(-280px);
    }
  }

  /* --- DYNAMIC VOLUMETRIC LIGHT BEAMS ACROSS PILLARS --- */
  .terminal-volumetric-shaft {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
  }

  .volumetric-ray {
    position: absolute;
    top: -160px;
    right: 180px;
    width: 300px;
    height: 1100px;
    transform-origin: top center;
    transform: rotate(-38deg);
    mix-blend-mode: screen;
    pointer-events: none;
  }

  .volumetric-ray.ray-primary {
    background: radial-gradient(
      ellipse 50% 100% at 50% 0%,
      rgba(255, 255, 255, 0.28) 0%,
      rgba(215, 228, 255, 0.15) 30%,
      rgba(175, 195, 235, 0.05) 60%,
      transparent 85%
    );
    animation: beamShimmerPrimary 9s ease-in-out infinite alternate;
    will-change: opacity, transform;
  }

  .volumetric-ray.ray-secondary {
    right: 250px;
    width: 200px;
    background: radial-gradient(
      ellipse 50% 100% at 50% 0%,
      rgba(255, 255, 255, 0.18) 0%,
      rgba(195, 215, 250, 0.09) 35%,
      rgba(150, 180, 225, 0.03) 65%,
      transparent 85%
    );
    animation: beamShimmerSecondary 7s ease-in-out infinite alternate;
    will-change: opacity, transform;
  }

  .volumetric-caustic-sheen {
    position: absolute;
    top: 0;
    right: 100px;
    width: 500px;
    height: 100%;
    background: radial-gradient(
      ellipse 60% 80% at 75% 30%,
      rgba(255, 255, 255, 0.14) 0%,
      rgba(180, 205, 245, 0.06) 50%,
      transparent 80%
    );
    mix-blend-mode: screen;
    animation: causticBreathing 11s ease-in-out infinite alternate;
    will-change: opacity;
  }

  @keyframes beamShimmerPrimary {
    0% {
      opacity: 0.45;
      transform: rotate(-39deg) scaleX(0.95);
    }
    50% {
      opacity: 0.88;
      transform: rotate(-37.5deg) scaleX(1.10);
    }
    100% {
      opacity: 0.55;
      transform: rotate(-38.5deg) scaleX(1.02);
    }
  }

  @keyframes beamShimmerSecondary {
    0% {
      opacity: 0.35;
      transform: rotate(-36.5deg) scaleX(1.05);
    }
    50% {
      opacity: 0.78;
      transform: rotate(-38.5deg) scaleX(0.92);
    }
    100% {
      opacity: 0.42;
      transform: rotate(-37deg) scaleX(1.0);
    }
  }

  @keyframes causticBreathing {
    0% {
      opacity: 0.45;
      transform: scale(0.97) translateY(0);
    }
    100% {
      opacity: 0.92;
      transform: scale(1.05) translateY(-10px);
    }
  }



  .arceus-ascii-sprite {
    width: 216px;
    height: 240px;
    background-image: url('/assets/arceus_ascii_spritesheet.png');
    background-size: 1728px 240px;
    background-repeat: no-repeat;
    background-position: 0 0;
    animation: arceusStride 1.05s steps(8) infinite, arceusGaitBob 0.525s ease-in-out infinite alternate;
    filter: drop-shadow(0 0 18px rgba(255, 255, 255, 0.16));
    opacity: 0.98;
  }

  @keyframes arceusStride {
    from {
      background-position: 0 0;
    }
    to {
      background-position: -1728px 0;
    }
  }

  @keyframes arceusGaitBob {
    0% {
      transform: translateY(0);
    }
    100% {
      transform: translateY(-4px);
    }
  }

  /* --- RICH CARD STAGGER & HOVER MICRO-ANIMATIONS --- */
  @keyframes cardFadeIn {
    0% {
      opacity: 0;
      transform: translateY(12px) scale(0.97);
    }
    100% {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  .model-card, .skin-card, .lo-card {
    background: rgba(16, 16, 20, 0.6) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 8px !important;
    position: relative;
    overflow: hidden;
    animation: cardFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) both;
    animation-delay: calc(var(--i, 0) * 0.018s);
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.2s ease,
                border-color 0.22s ease,
                box-shadow 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  }

  /* Shimmer light reflection sweep on card hover */
  .model-card::after, .skin-card::after, .lo-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: -150%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.07), transparent);
    transform: skewX(-25deg);
    transition: left 0.65s ease;
    pointer-events: none;
  }

  .model-card:hover::after, .skin-card:hover::after, .lo-card:hover::after {
    left: 200%;
  }

  .model-card:hover, .skin-card:hover, .lo-card:hover {
    transform: translateY(-4px) scale(1.015) !important;
    background: rgba(28, 28, 35, 0.82) !important;
    border-color: rgba(255, 255, 255, 0.45) !important;
    box-shadow: 0 14px 35px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255, 255, 255, 0.08) !important;
  }

  .model-img, .skin-img {
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), filter 0.28s ease;
  }

  .model-card:hover .model-img, .skin-card:hover .skin-img {
    transform: scale(1.08) rotate(-1deg);
    filter: drop-shadow(0 8px 18px rgba(255, 255, 255, 0.16));
  }

  /* Smooth Nav Item Slide & Glow */
  .nav-item {
    transition: transform 0.18s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.15s ease,
                color 0.15s ease,
                border-color 0.15s ease,
                padding-left 0.18s ease;
  }
  .nav-item:hover {
    transform: translateX(4px);
    padding-left: 14px;
    background: rgba(255, 255, 255, 0.06);
    color: #ffffff;
  }
  .nav-item.active {
    background: rgba(255, 255, 255, 0.09) !important;
    border-left: 2px solid #ffffff !important;
    color: #ffffff !important;
    box-shadow: inset 4px 0 14px rgba(255, 255, 255, 0.06);
  }

  /* Tactile Button Press Ripple */
  button:active, .model-card:active, .skin-card:active {
    transform: scale(0.97) !important;
    transition: transform 0.06s ease !important;
  }





  /* ═══════════════════════════════════════════════════════════════
     ARCEUS CYBERPUNK HUD LICENSE BADGE (SLEEK & HIGH-END)
     ═══════════════════════════════════════════════════════════════ */
  .arceus-license-hud {
    background: linear-gradient(145deg, rgba(14, 16, 22, 0.95), rgba(7, 8, 12, 0.98));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 12px 14px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    margin-top: auto;
  }
  .arceus-license-hud::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.6), transparent);
  }
  .hud-top-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  .hud-status-badge {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .hud-pulse-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 10px #10b981, 0 0 20px rgba(16, 185, 129, 0.4);
    animation: hudPulse 2s infinite ease-in-out;
  }
  @keyframes hudPulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
  }
  .hud-sys-label {
    font-family: var(--font-mono, monospace);
    font-size: 8.5px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #71717a;
    text-transform: uppercase;
  }
  .hud-plan-tag {
    font-family: var(--font-mono, monospace);
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #10b981;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.25);
    padding: 2px 6px;
    border-radius: 4px;
    text-transform: uppercase;
  }
  .hud-timer-display {
    margin: 6px 0 10px 0;
  }
  .hud-timer-sub {
    font-family: var(--font-mono, monospace);
    font-size: 8px;
    color: #52525b;
    letter-spacing: 0.12em;
    margin-bottom: 2px;
  }
  .hud-timer-value {
    font-family: var(--font-mono, monospace);
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #f4f4f5;
    text-shadow: 0 0 12px rgba(255, 255, 255, 0.15);
  }
  .hud-footer-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-top: 6px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    font-family: var(--font-mono, monospace);
    font-size: 8.5px;
    color: #52525b;
  }
  .hud-sec-lock {
    display: flex;
    align-items: center;
    gap: 4px;
    color: #a1a1aa;
    letter-spacing: 0.05em;
  }
  .hud-bridge-state {
    color: #10b981;
    letter-spacing: 0.05em;
    font-weight: 600;
  }
</style>

</head>
<body>

  <!-- ARCEUS LOGIN WINDOW (EXACT CLASSICAL DITHER REFERENCE) -->
    <!-- ARCEUS LOGIN WINDOW (SEAMLESS TERMINAL & PILLARS // ZERO DELIMITATION) -->
  <div class="arceus-login-screen" id="arceusLoginScreen">
    <div class="login-header-bar">
      <div class="login-bar-left pywebview-drag-region">
        <span class="login-badge-dot"></span>
        <span class="login-title-txt">ARCEUS // TERMINAL_ACCESS_GATE_01</span>
      </div>

    </div>

    <!-- DYNAMIC VOLUMETRIC LIGHT BEAMS ACROSS PILLARS -->
    <div class="terminal-volumetric-shaft">
      <div class="volumetric-ray ray-primary"></div>
      <div class="volumetric-ray ray-secondary"></div>
      <div class="volumetric-caustic-sheen"></div>
    </div>

    <div class="login-inner-stage">
      <div class="login-terminal-card">
        <div class="login-stealth-form" id="loginFormBox">
          <div class="login-field-group">
            <label class="login-field-label">IDENTITY</label>
            <div class="login-field-input-wrap">
              <span class="login-prompt-glyph">></span>
              <input type="text" id="loginPseudoInput" class="login-field-input" placeholder="username" autocomplete="off" spellcheck="false" value="dj" onkeydown="if(event.key==='Enter') submitArceusLogin()">
            </div>
          </div>

          <div class="login-field-group">
            <div class="login-label-row">
              <label class="login-field-label">ACCESS KEY</label>
              <button class="login-quick-dev-btn" type="button" onclick="fillDemoKey(event)">[ AUTO-FILL ]</button>
            </div>
            <div class="login-field-input-wrap">
              <span class="login-prompt-glyph">#</span>
              <input type="password" id="loginKeyInput" class="login-field-input" placeholder="ARCEUS-XXXX-XXXX" autocomplete="off" spellcheck="false" onkeydown="if(event.key==='Enter') submitArceusLogin()">
            </div>
          </div>

          <div class="login-error-msg" id="loginErrorMsg"></div>

          <button class="login-stealth-submit" id="loginSubmitBtn" onclick="submitArceusLogin()">
            <span id="loginBtnText">AUTHENTICATE</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>

        <div class="login-loading-phase" id="loginLoadingPhase" style="display: none;">
          <div class="login-loading-spinner"></div>
          <div class="login-loading-title" id="loginLoadingTitle">AUTHENTIFICATION EN COURS...</div>
          <div class="login-loading-sub" id="loginLoadingSub">> INITIALIZING TERMINAL CS2 HOOKS</div>
          <div class="login-loading-bar-wrap">
            <div class="login-loading-bar-fill" id="loginLoadingBarFill"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ARCEUS DITHER ASCII WALKER (WALKING RIGHT TO LEFT BEHIND LOGIN CARD) -->
      <div class="arceus-walker-lane">
        <div class="arceus-walker-entity">
          <div class="arceus-ascii-sprite"></div>
        </div>
      </div>

    </div>
  </div>

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar">
    <div class="brand pywebview-drag-region">
      <div class="brand-emblem">
        <img class="brand-logo" id="brandLogoImg" src="/assets/logo.png" alt="CS2">
      </div>
      <div class="brand-text-wrap">
        <div class="brand-name">CS2</div>
        <div class="brand-tag">LOADER</div>
      </div>
    </div>

    <div class="nav-section-lbl">ARSENAL</div>
    <nav class="nav-list" id="navList"></nav>

    <div class="sidebar-mid-actions">
      <button class="loadout-trigger" id="btnLoadout" onclick="openLoadoutView()">
        <div style="display:flex; align-items:center; gap:8px;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
          <span>INVENTAIRE</span>
        </div>
        <span class="loadout-badge" id="loadoutCount">0</span>
      </button>
    </div>

    <div class="sidebar-footer">
      <!-- HIGH-END CYBERPUNK LICENSE HUD -->
      <div class="arceus-license-hud" id="licenseTimerPill">
        <div class="hud-top-meta">
          <div class="hud-status-badge">
            <span class="hud-pulse-dot" id="licenseDot"></span>
            <span class="hud-sys-label">RING-0 // EN LIGNE</span>
          </div>
          <span class="hud-plan-tag" id="licensePlanName">LICENCE ACTIVE</span>
        </div>

        <div class="hud-timer-display">
          <div class="hud-timer-sub">TEMPS RESTANT</div>
          <div class="hud-timer-value" id="licenseTimerText">CHARGEMENT...</div>
        </div>

        <div class="hud-footer-meta">
          <div class="hud-sec-lock">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            <span>HWID VERROUILLÉ</span>
          </div>
          <div class="hud-bridge-state" id="bridgeStatusText">CONNECTÉ</div>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT STAGE -->
  <main class="main-stage">
    <div class="tactical-grid-overlay" id="tacticalGrid"></div>

    <header class="stage-header pywebview-drag-region">
      <!-- LEFT ZONE -->
      <div class="header-left-zone">
        <button class="back-btn" id="btnBackModels" onclick="backToModels()">
          ← RETOUR
        </button>
        <div class="stage-title" id="stageTitle" style="display:none;"></div>
      </div>

      <!-- CENTER ZONE (FILTERS) -->
      <div class="header-center-zone" id="skinFilters" style="display:none;">
        <input type="text" class="ctrl-input" id="searchInput" placeholder="Rechercher..." oninput="debounceSkins()">
        <select class="ctrl-select" id="raritySelect" onchange="loadSkinsForWeapon()">
          <option value="0">Toutes raretés</option>
          <option value="7">★ Or / Couteau</option>
          <option value="6">Secrète</option>
          <option value="5">Classifiée</option>
          <option value="4">Restreinte</option>
          <option value="3">Mil-Spec</option>
        </select>
        <select class="ctrl-select" id="sortSelect" onchange="loadSkinsForWeapon()">
          <option value="rarity_desc">Rareté ↓</option>
          <option value="name_asc">Nom A-Z</option>
        </select>
      </div>

      <!-- RIGHT ZONE -->
      <div class="header-right-zone">
        <div class="hud-mono" title="Touche pour masquer / afficher">[INSERT]</div>

      </div>
    </header>

    <div class="loadout-tabs" id="loadoutTabs">
      <button class="lo-tab active" data-filter="ALL" onclick="setLoadoutFilter('ALL')">TOUS</button>
      <button class="lo-tab" data-filter="WEAPONS" onclick="setLoadoutFilter('WEAPONS')">ARMES & COUTEAUX</button>
      <button class="lo-tab" data-filter="AGENTS_MUSIC" onclick="setLoadoutFilter('AGENTS_MUSIC')">AGENTS & MUSIQUES</button>
      <button class="lo-tab" data-filter="CONTAINERS" onclick="setLoadoutFilter('CONTAINERS')">CAISSES & CLÉS</button>
    </div>

    <div class="models-grid" id="stageContainer"></div>
  </main>

  <!-- SKIN CONFIGURATOR MODAL -->
  <div class="overlay-backdrop" id="configModal" onclick="if(event.target===this) closeConfigModal()">
    <div class="config-dialog">
      <div class="cfg-top">
        <div class="cfg-head-title" id="cfgModalHeader">CONFIGURATION</div>
        <div class="cfg-top-meta">
          <span>INVENTAIRE CS2</span>
        </div>
        <button class="cfg-close" onclick="closeConfigModal()">ESC</button>
      </div>

      <div class="cfg-body">
        <div class="cfg-left">
          <div class="cfg-stage">
            <img id="cfgImg" src="" alt="">
            <button class="cfg-inspect-btn" onclick="triggerInspectInCs2()" title="Générer le lien CEconItemPreviewDataBlock et inspecter dans CS2">INSPECTER CS2 ↗</button>
          </div>

          <div class="cfg-stickers-box" id="cfgStickerSection">
            <div class="cfg-lbl-row">
              <span>STICKERS (4 SLOTS)</span>
              <span class="cfg-lbl-val" style="cursor:pointer;" onclick="clearCurrentSkinStickers()">VIDER</span>
            </div>
            <div class="cfg-stk-grid" id="cfgStickerSlots"></div>

            <!-- REGLAGES POSITION / ROTATION / USURE DU STICKER SELECTIONNE -->
            <div class="stk-transform-panel" id="stkTransformPanel">
              <div class="cfg-lbl-row">
                <span id="stkTransformTitle">SLOT 01 // PLACEMENT</span>
                <span class="cfg-lbl-val" style="cursor:pointer;" onclick="openStickerModal(activeStickerSlotIndex)">CHANGER</span>
              </div>
              <div class="stk-tr-grid">
                <div>
                  <div class="cfg-lbl-row"><span>POS X</span><span class="cfg-lbl-val" id="stkPosXVal">0.00</span></div>
                  <input type="range" id="stkPosX" min="-1" max="1" step="0.01" value="0" oninput="updateStickerTransform()">
                </div>
                <div>
                  <div class="cfg-lbl-row"><span>POS Y</span><span class="cfg-lbl-val" id="stkPosYVal">0.00</span></div>
                  <input type="range" id="stkPosY" min="-1" max="1" step="0.01" value="0" oninput="updateStickerTransform()">
                </div>
                <div>
                  <div class="cfg-lbl-row"><span>ROTATION</span><span class="cfg-lbl-val" id="stkRotVal">0°</span></div>
                  <input type="range" id="stkRot" min="-180" max="180" step="1" value="0" oninput="updateStickerTransform()">
                </div>
                <div>
                  <div class="cfg-lbl-row"><span>USURE</span><span class="cfg-lbl-val" id="stkWearVal">0.00</span></div>
                  <input type="range" id="stkWear" min="0" max="1" step="0.01" value="0" oninput="updateStickerTransform()">
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="cfg-right">
          <div class="cfg-item-header">
            <div class="cfg-wep-name" id="cfgWeaponName">ARME</div>
            <div class="cfg-skin-name" id="cfgSkinName">Skin</div>
          </div>

          <div class="cfg-stickers-box" id="cfgWearSection">
            <div class="cfg-lbl-row">
              <span>QUALITÉ D'USURE (FLOAT CS2)</span>
              <span class="cfg-lbl-val" id="cfgFloatVal">NEUF • 0.01000</span>
            </div>
            <div class="wear-spectrum-bar">
              <div class="wear-pointer" id="wearPointer"></div>
            </div>
            <div class="wear-row" id="wearPillRow">
              <button class="wear-pill wear-fn" id="wearPillFN" onclick="selectWearTier('FN')">FN · NEUF</button>
              <button class="wear-pill wear-mw" id="wearPillMW" onclick="selectWearTier('MW')">MW · PEU USÉE</button>
              <button class="wear-pill wear-ft" id="wearPillFT" onclick="selectWearTier('FT')">FT · TESTÉE</button>
              <button class="wear-pill wear-ww" id="wearPillWW" onclick="selectWearTier('WW')">WW · USÉE</button>
              <button class="wear-pill wear-bs" id="wearPillBS" onclick="selectWearTier('BS')">BS · MARQUÉE</button>
            </div>
            <input type="range" id="cfgFloatSlider" min="0" max="1" step="0.00001" value="0.001" oninput="syncFloatSlider()">
          </div>

          <div class="cfg-2col" id="cfgSeedStSection">
            <div class="cfg-stickers-box">
              <div class="cfg-lbl-row">
                <span>PATTERN SEED</span>
                <div class="seed-chip-row">
                  <span class="seed-chip" onclick="setQuickSeed(661)" title="Tier 1 Scar Blue Gem">#661</span>
                  <span class="seed-chip" onclick="setQuickSeed(387)" title="Tier 1 Blue Gem">#387</span>
                  <span class="seed-chip" onclick="setQuickSeed(1337)" title="Leet">#1337</span>
                  <span class="seed-chip" onclick="setQuickSeed(Math.floor(Math.random()*1000)+1)">RND</span>
                </div>
              </div>
              <input type="number" class="cfg-input" id="cfgSeedInput" value="661" min="1" max="1000">
            </div>
            <div class="cfg-stickers-box" id="cfgStBox">
              <div class="cfg-lbl-row"><span>STATTRAK (-1=NON)</span></div>
              <input type="number" class="cfg-input" id="cfgStInput" value="-1" min="-1" max="999999">
            </div>
          </div>

          <div class="cfg-stickers-box" id="cfgNameSection">
            <div class="cfg-lbl-row">
              <span>NAMETAG</span>
              <div class="name-chip-row">
                <span class="seed-chip" onclick="setQuickName('Ace')">Ace</span>
                <span class="seed-chip" onclick="setQuickName('Clutch')">Clutch</span>
                <span class="seed-chip" onclick="setQuickName('Headshot')">Headshot</span>
              </div>
            </div>
            <input type="text" class="cfg-input" id="cfgNameInput" placeholder="Optionnel (ex: #001)">
          </div>

          <button class="btn-add-ingame" onclick="addInGame()">APPLIQUER IN-GAME</button>
        </div>
      </div>
    </div>
  </div>


  <!-- MODAL PROFIL UTILISATEUR -->
  <div class="overlay-backdrop" id="profileModal" onclick="if(event.target===this) closeProfileModal()">
    <div class="profile-dialog">
      <div class="cfg-top">
        <div class="cfg-head-title">PROFIL UTILISATEUR // CS2</div>
        <div class="cfg-top-meta">
          <span>COMPTE & TÉLÉMÉTRIE</span>
        </div>
        <button class="cfg-close" onclick="closeProfileModal()">ESC</button>
      </div>

      <div class="profile-modal-body">
        <div class="profile-header-banner">
          <div class="profile-hero-avatar-wrap" onclick="document.getElementById('avatarFileInput').click()" style="cursor: pointer;" title="Cliquer pour changer la photo de profil">
            <img class="profile-hero-avatar" id="modalProfileAvatar" src="/assets/logo.png" alt="Avatar">
            <span class="profile-hero-badge">LVL 10</span>
            <input type="file" id="avatarFileInput" accept="image/*" style="display:none" onchange="changeProfileAvatar(this)">
          </div>
          <div class="profile-hero-details">
            <div class="profile-hero-name-row">
              <span class="profile-hero-name" id="modalProfileName">dj</span>
              <span class="profile-hero-tag">OPERATOR</span>
            </div>
            <div class="profile-hero-steamid" id="modalSteamId">STEAM ID: 76561198000000001</div>
            <div class="profile-hero-vac">
              <span style="font-size:7px; color:#22c55e;">●</span> VALVE ANTI-CHEAT: BYPASS / ÉMULATION ACTIVE
            </div>
          </div>
        </div>

        <div class="profile-stats-grid">
          <div class="profile-stat-card">
            <div class="pstat-val" id="pstatSkinsCount">0</div>
            <div class="pstat-lbl">SKINS INVENTAIRE</div>
          </div>
          <div class="profile-stat-card">
            <div class="pstat-val" id="pstatStickersCount">0</div>
            <div class="pstat-lbl">STICKERS POSÉS</div>
          </div>
          <div class="profile-stat-card">
            <div class="pstat-val" id="pstatBridgeState">LOCAL</div>
            <div class="pstat-lbl">BRIDGE CS2</div>
          </div>
          <div class="profile-stat-card">
            <div class="pstat-val" id="pstatCatalogTotal">658</div>
            <div class="pstat-lbl">CATALOGUE TOTAL</div>
          </div>
        </div>

        <div class="profile-info-section">
          <div class="pinfo-row">
            <span class="pinfo-lbl">PSEUDO ACTUEL</span>
            <div class="pinfo-edit-wrap">
              <input type="text" class="pinfo-input" id="profileNameInput" value="dj" maxlength="24" oninput="updateProfileName(this.value)">
            </div>
          </div>
          <div class="pinfo-row">
            <span class="pinfo-lbl">TYPE DE CHARGEUR</span>
            <span class="pinfo-val">MESA / ARCEUS HYBRID NATIVE</span>
          </div>
          <div class="pinfo-row">
            <span class="pinfo-lbl">SOCACHE PROTOBUF</span>
            <span class="pinfo-val" id="pstatSocacheVer">SOID Type 1 (CS2 Econ)</span>
          </div>
          <div class="pinfo-row">
            <span class="pinfo-lbl">RACCOURCI SUPERPOSITION</span>
            <span class="pinfo-val">TOUCHE [INSERT] / [HOME] / [F6]</span>
          </div>
        </div>

        <div class="profile-actions-row">
          <button class="paction-btn" onclick="syncAndRefreshProfile()">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
            SYNCHRONISER CS2
          </button>
          <button class="paction-btn paction-btn-primary" onclick="closeProfileModal()">
            CONFIRMER & FERMER
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- STICKER PICKER MODAL -->
  <div class="sticker-backdrop" id="stickerModal" onclick="if(event.target===this) closeStickerModal()">
    <div class="sticker-dialog">
      <div class="cfg-top">
        <div class="cfg-head-title" id="stickerModalTitle">CHOISIR UN STICKER</div>
        <button class="cfg-close" onclick="closeStickerModal()">ESC</button>
      </div>
      <div class="stk-search-wrap">
        <input type="text" class="cfg-input" id="stickerSearchInput" placeholder="Rechercher un sticker (Titan, iBUYPOWER, Crown, Katowice...)" oninput="debounceStickers()">
      </div>
      <div class="stk-picker-grid" id="stickerPickerGrid"></div>
    </div>
  </div>

  <div class="toast" id="toast"></div>

<script>

  // --- USER PROFILE & TELEMETRY ---
  
  function changeProfileAvatar(fileInput) {
    if (fileInput.files && fileInput.files[0]) {
      const reader = new FileReader();
      reader.onload = function(e) {
        const dataUrl = e.target.result;
        try { localStorage.setItem('cs2_profile_avatar', dataUrl); } catch(err) {}
        const img1 = document.getElementById('profileAvatarImg');
        const img2 = document.getElementById('modalProfileAvatar');
        if (img1) img1.src = dataUrl;
        if (img2) img2.src = dataUrl;
      };
      reader.readAsDataURL(fileInput.files[0]);
    }
  }

  function openProfileModal() {
    const savedAvatar = localStorage.getItem('cs2_profile_avatar');
    if (savedAvatar) {
      const img1 = document.getElementById('profileAvatarImg');
      const img2 = document.getElementById('modalProfileAvatar');
      if (img1) img1.src = savedAvatar;
      if (img2) img2.src = savedAvatar;
    }
    const name = localStorage.getItem('cs2_profile_name') || 'dj';
    const nameDisplay = document.getElementById('profileNameDisplay');
    const modalName = document.getElementById('modalProfileName');
    const input = document.getElementById('profileNameInput');
    if (nameDisplay) nameDisplay.textContent = name;
    if (modalName) modalName.textContent = name;
    if (input) input.value = name;

    const totalSkins = cachedInventory.length;
    let totalStickers = 0;
    cachedInventory.forEach(item => {
      if (Array.isArray(item.stickers)) {
        totalStickers += item.stickers.filter(s => s && s.def_index).length;
      }
    });

    const skinsCountEl = document.getElementById('pstatSkinsCount');
    if (skinsCountEl) skinsCountEl.textContent = totalSkins;
    const stickersCountEl = document.getElementById('pstatStickersCount');
    if (stickersCountEl) stickersCountEl.textContent = totalStickers;

    const catalogTotalEl = document.getElementById('pstatCatalogTotal');
    if (catalogTotalEl && navData && navData.categories) {
      const tot = navData.categories.reduce((acc, c) => acc + (c.count || 0), 0);
      catalogTotalEl.textContent = tot > 0 ? tot : '658';
    }

    const modal = document.getElementById('profileModal');
    if (modal) modal.style.display = 'flex';
  }

  function closeProfileModal() {
    const modal = document.getElementById('profileModal');
    if (modal) modal.style.display = 'none';
  }

  function updateProfileName(newName) {
    const clean = newName.trim() || 'dj';
    localStorage.setItem('cs2_profile_name', clean);
    const nameDisplay = document.getElementById('profileNameDisplay');
    const modalName = document.getElementById('modalProfileName');
    if (nameDisplay) nameDisplay.textContent = clean;
    if (modalName) modalName.textContent = clean;
  }

  async function syncAndRefreshProfile() {
    try {
      await fetch('/api/sync', { method: 'POST' });
      await refreshLoadoutCount();
      await refreshBridgeStatus();
      openProfileModal();
    } catch(e) {
      console.warn('Sync error:', e);
    }
  }


  // ==========================================================================
  // ARCEUS AUTHENTICATION & LOGIN FLOW
  // ==========================================================================
  function showLoginError(msg) {
    const errorEl = document.getElementById('loginErrorMsg');
    if (errorEl) {
      errorEl.textContent = msg;
      errorEl.style.display = 'block';
    }
    try { playTactileSfx('click'); } catch(e) {}
  }

  function fillDemoKey(e) {
    if (e) e.preventDefault();
    const keyInput = document.getElementById('loginKeyInput');
    if (keyInput) keyInput.value = 'ARCEUS-VIP-2026';
    submitArceusLogin();
  }

  function submitVipFastLogin() {
    const keyInput = document.getElementById('loginKeyInput');
    if (keyInput) keyInput.value = 'ARCEUS-VIP-2026';
    submitArceusLogin();
  }

    let currentLicenseSession = null;
  let licenseCountdownInterval = null;
  let licenseHeartbeatInterval = null;

  function formatLicenseCountdown(sec) {
    if (sec <= 0) return "EXPIRÉ (00s)";
    const d = Math.floor(sec / 86400);
    const h = Math.floor((sec % 86400) / 3600);
    const m = Math.floor((sec % 3600) / 60);
    const s = Math.floor(sec % 60);
    const p = n => String(n).padStart(2, '0');
    if (d > 0) return `${d}j ${p(h)}h ${p(m)}m ${p(s)}s`;
    return `${p(h)}h ${p(m)}m ${p(s)}s`;
  }

  function startLicenseCountdown(authData) {
    currentLicenseSession = authData;
    const planEl = document.getElementById('licensePlanName');
    const textEl = document.getElementById('licenseTimerText');
    const dotEl = document.getElementById('licenseDot');

    if (planEl) planEl.textContent = authData.plan_name || 'LICENCE ACTIVE';

    if (authData.is_lifetime) {
      if (textEl) {
        textEl.textContent = 'À VIE (PERMANENT)';
        textEl.style.color = '#10b981';
      }
      if (dotEl) {
        dotEl.style.background = '#10b981';
        dotEl.style.boxShadow = '0 0 8px #10b981';
      }
      return;
    }

    let remaining = authData.remaining_seconds || 0;

    function tick() {
      if (remaining <= 0) {
        if (textEl) textEl.textContent = 'EXPIRÉ (00s)';
        if (dotEl) {
          dotEl.style.background = '#f43f5e';
          dotEl.style.boxShadow = '0 0 8px #f43f5e';
        }
        clearInterval(licenseCountdownInterval);
        clearInterval(licenseHeartbeatInterval);
        triggerLicenseTermination("Votre temps d'utilisation est arrivé à son terme.");
        return;
      }

      if (textEl) textEl.textContent = formatLicenseCountdown(remaining);

      // Gradient d'urgence visuel
      if (remaining < 3600) {
        if (textEl) textEl.style.color = '#f43f5e';
        if (dotEl) {
          dotEl.style.background = '#f43f5e';
          dotEl.style.boxShadow = '0 0 8px #f43f5e';
        }
      } else if (remaining < 86400) {
        if (textEl) textEl.style.color = '#f59e0b';
        if (dotEl) {
          dotEl.style.background = '#f59e0b';
          dotEl.style.boxShadow = '0 0 8px #f59e0b';
        }
      } else {
        if (textEl) textEl.style.color = '#10b981';
        if (dotEl) {
          dotEl.style.background = '#10b981';
          dotEl.style.boxShadow = '0 0 8px #10b981';
        }
      }
      remaining--;
    }

    tick();
    clearInterval(licenseCountdownInterval);
    licenseCountdownInterval = setInterval(tick, 1000);

    // Heartbeat toutes les 15 secondes pour garantir l'utilisation exclusive (1 seul PC)
    clearInterval(licenseHeartbeatInterval);
    licenseHeartbeatInterval = setInterval(async () => {
      try {
        const resp = await fetch('/api/auth/heartbeat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            key: authData.key,
            session_token: authData.session_token
          })
        });
        const hbData = await resp.json();
        if (!hbData.ok) {
          clearInterval(licenseCountdownInterval);
          clearInterval(licenseHeartbeatInterval);
          triggerLicenseTermination(hbData.error || "Session terminée ou clé utilisée sur un autre PC.");
        }
      } catch (err) {}
    }, 15000);
  }

  function triggerLicenseTermination(reasonMsg) {
    // Alerte plein écran et clôture forcée
    let ov = document.getElementById('emergencyLicenseOverlay');
    if (!ov) {
      ov = document.createElement('div');
      ov.id = 'emergencyLicenseOverlay';
      ov.style.cssText = 'position:fixed;inset:0;background:rgba(4,5,8,0.97);backdrop-filter:blur(24px);z-index:99999999;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-family:ui-monospace,monospace;text-align:center;padding:30px;';
      ov.innerHTML = `
        <div style="font-size:48px;margin-bottom:14px;">⚠️</div>
        <div style="font-size:20px;font-weight:900;letter-spacing:0.08em;color:#f43f5e;margin-bottom:10px;">LICENCE EXPIRÉE // FERMETURE IMMÉDIATE</div>
        <div style="font-size:13px;color:#a1a1aa;max-width:480px;line-height:1.6;margin-bottom:24px;">
          ${reasonMsg || "Votre temps de licence est écoulé. Counter-Strike 2 et le chargeur ARCEUS se ferment automatiquement."}
        </div>
        <div style="font-size:11px;color:#71717a;letter-spacing:0.08em;">FERMETURE DE CS2 ET DECONNEXION DU CHEAT EN COURS...</div>
      `;
      document.body.appendChild(ov);
    }

    setTimeout(() => {
      fetch('/api/auth/expire-kill', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: '{}'
      }).catch(() => {});
    }, 1200);
  }

  async function submitArceusLogin() {
    const pseudoInput = document.getElementById('loginPseudoInput');
    const keyInput = document.getElementById('loginKeyInput');
    const errorMsg = document.getElementById('loginErrorMsg');
    const pseudo = ((pseudoInput && pseudoInput.value) || '').trim() || 'dj';
    const key = ((keyInput && keyInput.value) || '').trim().toUpperCase();

    if (errorMsg) errorMsg.style.display = 'none';
    document.querySelectorAll('.login-input-wrap').forEach(w => w.classList.remove('has-error'));

    if (!key) {
      showLoginError("VEUILLEZ ENTRER VOTRE CLÉ D'ACTIVATION");
      if (keyInput) keyInput.parentElement.classList.add('has-error');
      return;
    }

    const btn = document.getElementById('loginSubmitBtn');
    if (btn) btn.disabled = true;

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pseudo: pseudo, key: key })
      });
      const data = await res.json();
      if (data && data.ok) {
        handleLoginSuccess(data);
      } else {
        showLoginError(data.error || "CLÉ INVALIDE // PAIEMENT REQUIS");
        if (keyInput) keyInput.parentElement.classList.add('has-error');
        if (btn) btn.disabled = false;
      }
    } catch(err) {
      console.error("Auth error:", err);
      showLoginError("ERREUR DE CONNEXION : " + (err.message || "SERVEUR INACCESSIBLE"));
      if (keyInput) keyInput.parentElement.classList.add('has-error');
      if (btn) btn.disabled = false;
    }
  }

  function handleLoginSuccess(authData) {
    const pseudo = authData.pseudo || 'dj';
    const key = authData.key || '';

    try { playTactileSfx('ready'); } catch(e) {}
    localStorage.setItem('cs2_profile_name', pseudo);
    localStorage.setItem('arceus_auth_key', key);
    localStorage.setItem('arceus_auth_session', authData.session_token || authData.token || '');
    localStorage.setItem('arceus_auth_time', Date.now());

    // Update profile display
    updateProfileName(pseudo);

    // Initialise le timer dynamique en bas du launcher
    startLicenseCountdown(authData);

    // Switch form to loading transition phase
    const formBox = document.getElementById('loginFormBox');
    const loadingPhase = document.getElementById('loginLoadingPhase');
    if (formBox) formBox.style.display = 'none';
    if (loadingPhase) loadingPhase.style.display = 'flex';

    const titleEl = document.getElementById('loginLoadingTitle');
    const subEl = document.getElementById('loginLoadingSub');
    const barEl = document.getElementById('loginLoadingBarFill');

    const stages = [
      { pct: 25, t: 200, title: "CLÉ VALIDÉE [" + key + "]", sub: authData.plan_name || "Session sécurisée initialisée..." },
      { pct: 55, t: 650, title: "CHARGEMENT DU PROTOBUF & SOCACHE...", sub: "Synchronisation des objets du catalogue" },
      { pct: 85, t: 1100, title: "CONNEXION CS2 BRIDGE...", sub: "Accès mémoire et émulation d'inventaire prêts" },
      { pct: 100, t: 1550, title: "ACCÈS ACCORDÉ // BIENVENUE " + pseudo.toUpperCase(), sub: "Ouverture du chargeur ARCEUS..." }
    ];

    stages.forEach(st => {
      setTimeout(() => {
        if (barEl) barEl.style.width = st.pct + '%';
        if (titleEl) titleEl.textContent = st.title;
        if (subEl) subEl.textContent = st.sub;
        if (st.pct === 100) {
          try { playTactileSfx('ready'); } catch(e) {}
        }
      }, st.t);
    });

    // Dismiss login screen
    setTimeout(() => {
      const loginScreen = document.getElementById('arceusLoginScreen');
      if (loginScreen) {
        loginScreen.classList.add('dismissed');
        setTimeout(() => { loginScreen.style.display = 'none'; }, 500);
      }
    }, 2000);
  }

  let navData = { categories: [], weapons_by_category: {} };
  let activeCategory = 'Couteaux';
  let activeWeapon = null;
  let currentMode = 'MODELS';
  let activeLoadoutFilter = 'ALL';
  let catalogItems = [];
  let cachedInventory = [];
  let selectedSkin = null;
  let searchTimer = null;
  let stickerTimer = null;
  let activeStickerSlotIndex = 0;

  /* 4 SLOTS STICKERS PAR SKIN_ID */
  const stickersBySkinId = {};

  const NON_FLOAT_CATEGORIES = new Set([
    'Agents', 'Musiques', 'Caisses', 'Clés', 'Cases', 'Keys', 'Equipment', 'Music Kits',
    'agents', 'musiques', 'caisses', 'clés', 'cases', 'keys', 'equipment'
  ]);

  /* DÉTOURAGE AUTOMATIQUE DU FOND BLANC EXTERNE DE LOGO.PNG */
  function prepareTransparentLogo() {
    try {
      const imgEl = document.getElementById('brandLogoImg');
      if (!imgEl) return;
      const probe = new Image();
      probe.crossOrigin = 'anonymous';
      probe.onload = () => {
        try {
          const size = 256;
          const canvas = document.createElement('canvas');
          canvas.width = size;
          canvas.height = size;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(probe, 0, 0, size, size);
          const imgData = ctx.getImageData(0, 0, size, size);
          const d = imgData.data;

          if (d[3] < 20) return;

          const visited = new Uint8Array(size * size);
          const queue = new Int32Array(size * size);
          let head = 0;
          let tail = 0;

          function isBgWhite(idx) {
            const r = d[idx], g = d[idx + 1], b = d[idx + 2];
            const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
            return mn >= 215 && (mx - mn) <= 28;
          }

          for (let x = 0; x < size; x++) {
            const top = x;
            const bot = (size - 1) * size + x;
            if (isBgWhite(top * 4)) { visited[top] = 1; queue[tail++] = top; }
            if (isBgWhite(bot * 4)) { visited[bot] = 1; queue[tail++] = bot; }
          }
          for (let y = 0; y < size; y++) {
            const left = y * size;
            const right = y * size + (size - 1);
            if (!visited[left] && isBgWhite(left * 4)) { visited[left] = 1; queue[tail++] = left; }
            if (!visited[right] && isBgWhite(right * 4)) { visited[right] = 1; queue[tail++] = right; }
          }

          const dirs = [-1, 1, -size, size];
          while (head < tail) {
            const cur = queue[head++];
            const p4 = cur * 4;
            d[p4 + 3] = 0;

            const cx = cur % size;
            for (let i = 0; i < 4; i++) {
              const nxt = cur + dirs[i];
              if (nxt < 0 || nxt >= size * size || visited[nxt]) continue;
              const nx = nxt % size;
              if (Math.abs(nx - cx) > 1) continue;

              const n4 = nxt * 4;
              if (isBgWhite(n4)) {
                visited[nxt] = 1;
                queue[tail++] = nxt;
              } else {
                const nr = d[n4], ng = d[n4 + 1], nb = d[n4 + 2];
                const nmin = Math.min(nr, ng, nb);
                const nmax = Math.max(nr, ng, nb);
                if (nmin >= 175 && (nmax - nmin) <= 35) {
                  d[n4 + 3] = Math.min(d[n4 + 3], Math.max(0, Math.round((230 - nmin) * 4)));
                }
              }
            }
          }

          ctx.putImageData(imgData, 0, 0);
          imgEl.src = canvas.toDataURL('image/png');
        } catch (e) {
          console.warn("Transparency processing skipped:", e);
        }
      };
      probe.src = '/assets/logo.png';
    } catch(err) {
      console.warn("Logo setup skipped:", err);
    }
  }

  function setQuickName(val) {
    const input = document.getElementById('cfgNameInput');
    if (input) input.value = val;
  }

  function toggleScanlines() {
    const grid = document.getElementById('tacticalGrid');
    const btn = document.getElementById('btnGridToggle');
    if (!grid || !btn) return;
    const active = grid.classList.toggle('active');
    btn.classList.toggle('active', active);
    showToast(active ? '[GRID] GRILLE TACTIQUE ACTIVÉE' : '[GRID] GRILLE TACTIQUE DÉSACTIVÉE');
  }

  const WEAR_TIERS = {
    FN: { key: 'FN', label: 'FN · NEUF', fullName: 'NEUF (FN)', min: 0.00, max: 0.07, mid: 0.015 },
    MW: { key: 'MW', label: 'MW · PEU USÉE', fullName: 'TRÈS PEU USÉE (MW)', min: 0.07, max: 0.15, mid: 0.09 },
    FT: { key: 'FT', label: 'FT · TESTÉE', fullName: 'TESTÉE (FT)', min: 0.15, max: 0.38, mid: 0.20 },
    WW: { key: 'WW', label: 'WW · USÉE', fullName: 'USÉE (WW)', min: 0.38, max: 0.45, mid: 0.40 },
    BS: { key: 'BS', label: 'BS · MARQUÉE', fullName: 'MARQUÉE (BS)', min: 0.45, max: 1.00, mid: 0.65 }
  };

  function isTierAvailable(tierKey, minFloat, maxFloat) {
    const t = WEAR_TIERS[tierKey];
    if (!t) return false;
    return !(maxFloat <= t.min || minFloat >= t.max);
  }

  function wearFullLabel(w) {
    if (w < 0.07) return 'NEUF (FN)';
    if (w < 0.15) return 'TRÈS PEU USÉE (MW)';
    if (w < 0.38) return 'TESTÉE (FT)';
    if (w < 0.45) return 'USÉE (WW)';
    return 'MARQUÉE (BS)';
  }

  function wearKeyForFloat(w) {
    if (w < 0.07) return 'FN';
    if (w < 0.15) return 'MW';
    if (w < 0.38) return 'FT';
    if (w < 0.45) return 'WW';
    return 'BS';
  }

  function canHaveStickers(categoryName) {
    if (!categoryName) return false;
    const c = String(categoryName).trim().toLowerCase();
    // Les couteaux, gants, musiques, caisses, cles, agents ne prennent pas de stickers
    if (c.includes('knife') || c.includes('couteau') || 
        c.includes('glove') || c.includes('gant') || 
        c.includes('agent') || c.includes('music') || c.includes('musique') || 
        c.includes('case') || c.includes('caisse') || 
        c.includes('key') || c.includes('clé') || c.includes('cle') ||
        c.includes('equip') || c.includes('pin') || c.includes('patch')) {
      return false;
    }
    // Toutes les armes à feu (Rifles, Pistols, SMGs, Heavy, Fusils, etc.) sont éligibles
    return true;
  }

  function getSkinStickerSlots(skinId) {
    if (!skinId) return [null, null, null, null];
    if (!stickersBySkinId[skinId]) {
      stickersBySkinId[skinId] = [null, null, null, null];
    }
    while (stickersBySkinId[skinId].length < 4) {
      stickersBySkinId[skinId].push(null);
    }
    if (stickersBySkinId[skinId].length > 4) {
      stickersBySkinId[skinId] = stickersBySkinId[skinId].slice(0, 4);
    }
    return stickersBySkinId[skinId];
  }

  function updateStepChips(steps) {
    const s = steps || {};
    document.getElementById('stepChipDll')?.classList.toggle('ok', Boolean(s.dll_loaded));
    document.getElementById('stepChipJson')?.classList.toggle('ok', Boolean(s.json_read));
    document.getElementById('stepChipAdd')?.classList.toggle('ok', Boolean(s.item_added));
    document.getElementById('stepChipEq')?.classList.toggle('ok', Boolean(s.item_equipped));
  }

  function runCinematicBootSequence() {
    try { playTactileSfx('boot'); } catch(e) {}

    const fillEl = document.getElementById('bootProgressFill');
    const pctEl = document.getElementById('bootPercentText');
    const statusEl = document.getElementById('bootStatusText');

    const TOTAL_DURATION_MS = 5000; // EXACT 5.0 SECONDS
    const startTime = performance.now();

    const stages = [
      { t: 0.0, label: 'INITIALISATION DU MOTEUR...' },
      { t: 1.6, label: 'SYNCHRONISATION DU CATALOGUE...' },
      { t: 3.4, label: 'CONNEXION CS2...' },
      { t: 4.7, label: 'PRÊT' }
    ];

    let lastStageIdx = -1;

    return new Promise((resolve) => {
      let resolved = false;
      function finish() {
        if (resolved) return;
        resolved = true;
        try { playTactileSfx('ready'); } catch(e) {}
        const screen = document.getElementById('arceusBootScreen');
        if (screen) {
          screen.classList.add('dismissed');
          setTimeout(() => { screen.style.display = 'none'; resolve(); }, 350);
        } else {
          resolve();
        }
      }

      // Safeguard: auto-resolve after 3.5s so it never freezes
      setTimeout(finish, 1800);

      function tick(now) {
        if (resolved) return;
        const elapsed = now - startTime;
        const progress = Math.min(1.0, elapsed / 1400);
        const percent = Math.floor(progress * 100);

        if (fillEl) fillEl.style.width = percent + '%';
        if (pctEl) pctEl.textContent = percent + '%';

        const seconds = elapsed / 1000;
        for (let i = 0; i < stages.length; i++) {
          if (seconds >= (stages[i].t * 0.6) && lastStageIdx < i) {
            lastStageIdx = i;
            if (statusEl) statusEl.textContent = stages[i].label;
          }
        }

        if (progress < 1.0) {
          requestAnimationFrame(tick);
        } else {
          setTimeout(finish, 150);
        }
      }
      requestAnimationFrame(tick);
    });
  }

  async function initApp() {
    try { prepareTransparentLogo(); } catch(e) {}

    try {
      const savedAvatar = localStorage.getItem('cs2_profile_avatar');
      if (savedAvatar) {
        const img1 = document.getElementById('profileAvatarImg');
        const img2 = document.getElementById('modalProfileAvatar');
        if (img1) img1.src = savedAvatar;
        if (img2) img2.src = savedAvatar;
      }
      const savedProfileName = localStorage.getItem('cs2_profile_name') || 'dj';
      const nameEl = document.getElementById('profileNameDisplay');
      if (nameEl) nameEl.textContent = savedProfileName;

      const res = await fetch('/api/nav');
      navData = await res.json();
      if (navData.categories && navData.categories.length > 0) {
        activeCategory = navData.categories[0].name;
      }
      await refreshLoadoutCount();
      await refreshBridgeStatus();
      renderSidebar();
      openCategoryModels(activeCategory);
    } catch(err) {
      console.error("InitApp background load error:", err);
    }

    }

  async function refreshBridgeStatus() {
    try {
      const res = await fetch('/api/status');
      const st = await res.json();
      const pill = document.getElementById('bridgeStatusPill');
      const txt = document.getElementById('bridgeStatusText');
      const steps = st.steps || {};
      updateStepChips(steps);
      const pstatBridge = document.getElementById('pstatBridgeState');
      const pSub = document.getElementById('profileSubDisplay');
      if (st.synced) {
        if (pstatBridge) pstatBridge.textContent = 'CONNECTÉ';
        if (pSub) pSub.textContent = 'CS2 CONNECTÉ';
        pill.classList.add('connected');
        txt.textContent = 'CS2 CONNECTÉ';
        pill.title = st.reason || 'Bridge actif dans cs2.exe';
      } else if (steps.dll_loaded) {
        pill.classList.remove('connected');
        txt.textContent = 'DLL CHARGÉE';
        pill.title = st.reason || 'DLL chargée, en attente de lecture JSON';
      } else {
        if (pstatBridge) pstatBridge.textContent = 'LOCAL';
        if (pSub) pSub.textContent = 'STEAM EN LIGNE';
        pill.classList.remove('connected');
        txt.textContent = 'MODE LOCAL';
        pill.title = st.reason || 'Bridge non injecté';
      }
    } catch (e) {}
  }

  function renderSidebar() {
    const list = document.getElementById('navList');
    list.innerHTML = navData.categories.map(c => `
      <button class="nav-item ${(currentMode !== 'LOADOUT' && c.name === activeCategory) ? 'active' : ''}"
              onclick="openCategoryModels('${c.name.replace(/'/g, "\\'")}')">
        ${c.icon ? `<img class="nav-icon" src="${c.icon}" alt="">` : ''}
        <span class="nav-label">${c.name}</span>
        <span class="nav-cnt">${c.count}</span>
      </button>
    `).join('');
  }

  function openCategoryModels(catName) {
    activeCategory = catName;
    activeWeapon = null;
    currentMode = 'MODELS';

    document.getElementById('btnLoadout').classList.remove('active');
    document.getElementById('loadoutTabs').style.display = 'none';
    renderSidebar();

    const weapons = navData.weapons_by_category[activeCategory] || [];
    if (weapons.length === 1) {
      openWeaponSkins(weapons[0].weapon_name, true);
      return;
    }

    document.getElementById('btnBackModels').style.display = 'none';
    document.getElementById('skinFilters').style.display = 'none';
    document.getElementById('stageTitle').innerHTML =
      `${activeCategory.toUpperCase()} <span>${weapons.length} MODÈLES</span>`;

    const container = document.getElementById('stageContainer');
    container.className = 'models-grid';
    container.innerHTML = weapons.map((w, idx) => `
      <div class="model-card" style="--i: ${idx}" onclick="openWeaponSkins('${w.weapon_name.replace(/'/g, "\\'")}', false)">
        <div class="model-top-row">
          <span class="model-cnt">${w.count}</span>
        </div>
        <div class="model-img-wrap">
          ${w.icon ? `<img class="model-img" src="${w.icon}" alt="">` : ''}
        </div>
        <div class="model-footer">
          <div class="model-name">${w.weapon_name}</div>
        </div>
      </div>
    `).join('');
  }

  async function openWeaponSkins(weaponName, singleGroup = false) {
    activeWeapon = weaponName;
    currentMode = 'SKINS';

    document.getElementById('btnBackModels').style.display = singleGroup ? 'none' : 'flex';
    document.getElementById('skinFilters').style.display = 'flex';
    document.getElementById('loadoutTabs').style.display = 'none';
    document.getElementById('searchInput').value = '';

    await loadSkinsForWeapon();
  }

  function backToModels() {
    openCategoryModels(activeCategory);
  }

  function debounceSkins() {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(loadSkinsForWeapon, 140);
  }

  async function loadSkinsForWeapon() {
    if (currentMode !== 'SKINS') return;

    const q = document.getElementById('searchInput').value.trim();
    const rarity = document.getElementById('raritySelect').value;
    const sort = document.getElementById('sortSelect').value;

    const params = new URLSearchParams({
      category: activeCategory,
      weapon: activeWeapon || 'Toutes',
      q,
      rarity,
      sort,
      st: '0'
    });

    const res = await fetch(`/api/catalog?${params.toString()}`);
    const data = await res.json();
    catalogItems = data.items || [];

    document.getElementById('stageTitle').innerHTML =
      `${activeCategory.toUpperCase()} › ${activeWeapon.toUpperCase()} <span>${catalogItems.length}</span>`;

    const container = document.getElementById('stageContainer');
    container.className = 'skins-grid';
    container.innerHTML = catalogItems.map((item, idx) => `
      <div class="skin-card"
           style="--i: ${idx}; --rarity-col: ${item.rarity_color || '#FFFFFF'}"
           onclick="openSkinConfig(${idx})">
        <div class="skin-card-top">
          <span><i class="rarity-dot"></i> #${item.paint_index}</span>
          ${item.stattrak ? '<span class="st-tag">ST™</span>' : '<span></span>'}
        </div>
        <div class="skin-img-box">
          <img class="skin-img" loading="lazy" src="${item.image_url}" alt="">
        </div>
        <div class="skin-card-bottom">
          <div class="skin-wep-sub">${item.weapon_name}</div>
          <div class="skin-title">${item.skin_name}</div>
        </div>
      </div>
    `).join('');
  }

  function openSkinConfig(index) {
    const item = catalogItems[index];
    if (!item) return;
    selectedSkin = item;
    activeStickerSlotIndex = 0;

    document.getElementById('cfgModalHeader').textContent = `${item.category_name} // #${item.paint_index}`;
    document.getElementById('cfgImg').src = item.image_url;
    document.getElementById('cfgWeaponName').textContent = item.weapon_name;
    document.getElementById('cfgSkinName').textContent = item.skin_name;

    const catLower = String(item.category_name || '').toLowerCase();
    const noFloat = NON_FLOAT_CATEGORIES.has(item.category_name) || catLower.includes('case') || catLower.includes('caisse') || catLower.includes('key') || catLower.includes('agent') || catLower.includes('music');
    const eligibleForStickers = canHaveStickers(item.category_name);
    const isGlove = catLower.includes('glove') || catLower.includes('gant');
    const isContainer = catLower.includes('case') || catLower.includes('caisse') || catLower.includes('key') || catLower.includes('clé') || catLower.includes('cle');

    document.getElementById('cfgWearSection').style.display = noFloat ? 'none' : 'flex';
    document.getElementById('cfgSeedStSection').style.display = noFloat ? 'none' : 'grid';
    document.getElementById('cfgStBox').style.display = isGlove ? 'none' : 'flex';
    document.getElementById('cfgStickerSection').style.display = eligibleForStickers ? 'flex' : 'none';
    document.getElementById('cfgNameSection').style.display = (noFloat || isGlove || isContainer) ? 'none' : 'flex';

    if (!noFloat) {
      const minF = Number(item.min_float !== undefined ? item.min_float : 0.00);
      const maxF = Number(item.max_float !== undefined ? item.max_float : 1.00);
      const slider = document.getElementById('cfgFloatSlider');
      slider.min = minF;
      slider.max = maxF;
      slider.step = '0.00001';

      // Lock wear tier buttons to what physically exists for this skin in CS2
      let firstAvailableTier = null;
      for (const [key, tier] of Object.entries(WEAR_TIERS)) {
        const btn = document.getElementById(`wearPill${key}`);
        const available = isTierAvailable(key, minF, maxF);
        if (btn) {
          btn.disabled = !available;
          btn.classList.toggle('wear-disabled', !available);
        }
        if (available && !firstAvailableTier) {
          firstAvailableTier = tier;
        }
      }

      // Default float value: closest available tier midpoint or min_float
      const initialFloat = firstAvailableTier
        ? Math.max(minF, Math.min(maxF, firstAvailableTier.mid))
        : minF;
      slider.value = initialFloat;
      syncFloatSlider();
    }

    renderConfigStickerSlots();
    document.getElementById('configModal').style.display = 'flex';
  }

  function closeConfigModal() {
    document.getElementById('configModal').style.display = 'none';
  }

  function selectWearTier(tierKey) {
    if (!selectedSkin) return;
    const minF = Number(selectedSkin.min_float !== undefined ? selectedSkin.min_float : 0.00);
    const maxF = Number(selectedSkin.max_float !== undefined ? selectedSkin.max_float : 1.00);
    if (!isTierAvailable(tierKey, minF, maxF)) return;

    const tier = WEAR_TIERS[tierKey];
    if (!tier) return;

    const targetVal = Math.max(minF, Math.min(maxF, tier.mid));
    const slider = document.getElementById('cfgFloatSlider');
    slider.value = targetVal;
    syncFloatSlider();
  }

  function setWear(val, btn) {
    selectWearTier(wearKeyForFloat(val));
  }

  function syncFloatSlider() {
    const slider = document.getElementById('cfgFloatSlider');
    const val = parseFloat(slider.value || 0.001);
    const currentKey = wearKeyForFloat(val);

    document.getElementById('cfgFloatVal').textContent = `${wearFullLabel(val)} • ${val.toFixed(5)}`;
    const ptr = document.getElementById('wearPointer');
    if (ptr) {
      ptr.style.left = `${Math.max(1, Math.min(99, val * 100))}%`;
    }

    for (const key of Object.keys(WEAR_TIERS)) {
      const btn = document.getElementById(`wearPill${key}`);
      if (btn) {
        btn.classList.toggle('active', key === currentKey && !btn.disabled);
      }
    }
  }

  function setQuickSeed(seedVal) {
    const inp = document.getElementById('cfgSeedInput');
    if (inp) inp.value = seedVal;
  }

  function renderConfigStickerSlots() {
    const grid = document.getElementById('cfgStickerSlots');
    const trPanel = document.getElementById('stkTransformPanel');
    if (!selectedSkin || !canHaveStickers(selectedSkin.category_name)) {
      grid.innerHTML = '';
      trPanel.style.display = 'none';
      return;
    }

    const slots = getSkinStickerSlots(selectedSkin.skin_id);
    grid.innerHTML = slots.map((stk, idx) => {
      if (!stk) {
        return `
          <div class="cfg-stk-slot ${idx === activeStickerSlotIndex ? 'active-slot' : ''}" onclick="openStickerModal(${idx})" title="Choisir sticker pour Slot 0${idx + 1}">
            <span style="font-size:14px;color:var(--white);font-weight:700;line-height:1;">+</span>
            <span style="font-size:8px;font-family:'JetBrains Mono',monospace;color:var(--text-mid);letter-spacing:0.5px;">SLOT 0${idx + 1}</span>
          </div>
        `;
      }
      return `
        <div class="cfg-stk-slot has-stk ${idx === activeStickerSlotIndex ? 'active-slot' : ''}" onclick="focusFilledStickerSlot(${idx})" title="${stk.name}">
          <button class="stk-rm-btn" onclick="removeStickerSlot(event, ${idx})">✕</button>
          <img src="${stk.image_url}" alt="">
        </div>
      `;
    }).join('');

    const currentStk = slots[activeStickerSlotIndex];
    if (currentStk) {
      trPanel.style.display = 'flex';
      document.getElementById('stkTransformTitle').textContent = `SLOT 0${activeStickerSlotIndex + 1} // ${currentStk.name.slice(0, 18)}`;
      document.getElementById('stkPosX').value = currentStk.offset_x || 0;
      document.getElementById('stkPosY').value = currentStk.offset_y || 0;
      document.getElementById('stkRot').value = currentStk.rotation || 0;
      document.getElementById('stkWear').value = currentStk.wear || 0;
      document.getElementById('stkPosXVal').textContent = Number(currentStk.offset_x || 0).toFixed(2);
      document.getElementById('stkPosYVal').textContent = Number(currentStk.offset_y || 0).toFixed(2);
      document.getElementById('stkRotVal').textContent = `${Math.round(currentStk.rotation || 0)}°`;
      document.getElementById('stkWearVal').textContent = Number(currentStk.wear || 0).toFixed(2);
    } else {
      trPanel.style.display = 'none';
    }
  }

  function focusFilledStickerSlot(slotIdx) {
    activeStickerSlotIndex = slotIdx;
    renderConfigStickerSlots();
  }

  function updateStickerTransform() {
    if (!selectedSkin) return;
    const slots = getSkinStickerSlots(selectedSkin.skin_id);
    const stk = slots[activeStickerSlotIndex];
    if (!stk) return;
    stk.offset_x = parseFloat(document.getElementById('stkPosX').value || '0');
    stk.offset_y = parseFloat(document.getElementById('stkPosY').value || '0');
    stk.rotation = parseFloat(document.getElementById('stkRot').value || '0');
    stk.wear = parseFloat(document.getElementById('stkWear').value || '0');
    document.getElementById('stkPosXVal').textContent = stk.offset_x.toFixed(2);
    document.getElementById('stkPosYVal').textContent = stk.offset_y.toFixed(2);
    document.getElementById('stkRotVal').textContent = `${Math.round(stk.rotation)}°`;
    document.getElementById('stkWearVal').textContent = stk.wear.toFixed(2);
  }

  function removeStickerSlot(ev, slotIdx) {
    ev.stopPropagation();
    if (!selectedSkin) return;
    const slots = getSkinStickerSlots(selectedSkin.skin_id);
    slots[slotIdx] = null;
    renderConfigStickerSlots();
  }

  function clearCurrentSkinStickers() {
    if (!selectedSkin) return;
    stickersBySkinId[selectedSkin.skin_id] = [null, null, null, null];
    renderConfigStickerSlots();
  }

  async function openStickerModal(slotIdx) {
    if (!selectedSkin || !canHaveStickers(selectedSkin.category_name)) return;
    activeStickerSlotIndex = slotIdx;
    document.getElementById('stickerModalTitle').textContent = `STICKER // ${selectedSkin.skin_name} (SLOT 0${slotIdx + 1})`;
    document.getElementById('stickerModal').style.display = 'flex';
    document.getElementById('stickerSearchInput').focus();
    await loadStickers();
  }

  function closeStickerModal() {
    document.getElementById('stickerModal').style.display = 'none';
  }

  function debounceStickers() {
    clearTimeout(stickerTimer);
    stickerTimer = setTimeout(loadStickers, 140);
  }

  async function loadStickers() {
    const q = document.getElementById('stickerSearchInput').value.trim();
    const res = await fetch(`/api/stickers?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    const items = data.items || [];
    const grid = document.getElementById('stickerPickerGrid');
    grid.innerHTML = items.map(stk => `
      <div class="stk-item"
           onclick='selectStickerForSlot(${JSON.stringify(stk).replace(/'/g, "&#39;")})'>
        <img loading="lazy" src="${stk.image_url}" alt="">
        <div class="stk-item-title">${stk.name}</div>
      </div>
    `).join('');
  }

  function selectStickerForSlot(stk) {
    if (!selectedSkin || !canHaveStickers(selectedSkin.category_name)) return;
    const slots = getSkinStickerSlots(selectedSkin.skin_id);
    slots[activeStickerSlotIndex] = {
      slot: activeStickerSlotIndex,
      sticker_id: stk.def_index,
      def_index: stk.def_index,
      name: stk.name,
      image_url: stk.image_url,
      wear: 0.0,
      scale: 1.0,
      rotation: 0.0,
      offset_x: 0.0,
      offset_y: 0.0
    };
    renderConfigStickerSlots();
    closeStickerModal();
  }

  function getActiveStickersPayload() {
    if (!selectedSkin || !canHaveStickers(selectedSkin.category_name)) {
      return [];
    }
    return getSkinStickerSlots(selectedSkin.skin_id).filter(Boolean);
  }

  async function triggerInspectInCs2() {
    if (!selectedSkin) return;
    const payload = {
      skin_id: selectedSkin.skin_id,
      paint_wear: parseFloat(document.getElementById('cfgFloatSlider').value || '0.001'),
      paint_seed: parseInt(document.getElementById('cfgSeedInput').value || '661', 10),
      stattrak_count: parseInt(document.getElementById('cfgStInput').value || '-1', 10),
      custom_name: document.getElementById('cfgNameInput').value.trim(),
      stickers: getActiveStickersPayload()
    };
    const res = await fetch('/api/inspect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.ok) {
      showToast('LIEN INSPECT PROTOBUF ENVOYÉ À STEAM / CS2', true);
    }
  }

  async function addInGame() {
    if (!selectedSkin) return;
    const isCTOnlyAgent = selectedSkin.category_name === 'Agents' && selectedSkin.weapon_name.includes('CT');
    const isTOnlyAgent = selectedSkin.category_name === 'Agents' && !selectedSkin.weapon_name.includes('CT');

    const payload = {
      skin_id: selectedSkin.skin_id,
      paint_wear: parseFloat(document.getElementById('cfgFloatSlider').value || '0.001'),
      paint_seed: parseInt(document.getElementById('cfgSeedInput').value || '661', 10),
      stattrak_count: parseInt(document.getElementById('cfgStInput').value || '-1', 10),
      custom_name: document.getElementById('cfgNameInput').value.trim(),
      equip_t: !isCTOnlyAgent,
      equip_ct: !isTOnlyAgent,
      stickers: getActiveStickersPayload()
    };

    const res = await fetch('/api/import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (data.ok) {
      playTactileSfx('apply');
      await refreshLoadoutCount();
      await refreshBridgeStatus();
      closeConfigModal();
      const s = data.steps || {};
      updateStepChips(s);
      const stepSummary = [
        `DLL chargée: ${s.dll_loaded ? 'OUI' : 'NON'}`,
        `JSON lu: ${s.json_read ? 'OUI' : 'NON'}`,
        `Objet ajouté: ${s.item_added ? 'OUI' : 'NON'}`,
        `Objet équipé: ${s.item_equipped ? 'OUI' : 'NON'}`
      ].join(' | ');
      const allVerified = Boolean(s.dll_loaded && s.json_read && s.item_added && s.item_equipped);
      if (allVerified) {
        showToast(`SYNCHRONISÉ DANS CS2 [${stepSummary}]`, true);
      } else {
        showToast(`LOADOUT LOCAL [${stepSummary}] (${data.bridge_reason || 'CS2 non vérifié'})`, false);
      }
    }
  }

  async function refreshLoadoutCount() {
    const res = await fetch('/api/inventory');
    const data = await res.json();
    cachedInventory = data.items || [];
    document.getElementById('loadoutCount').textContent = cachedInventory.length;
    cachedInventory.forEach(item => {
      if (item.skin_id && canHaveStickers(item.category_name) && Array.isArray(item.stickers) && item.stickers.length > 0) {
        const slots = [null, null, null, null];
        item.stickers.forEach(s => {
          if (s && s.slot >= 0 && s.slot < 4) slots[s.slot] = s;
        });
        stickersBySkinId[item.skin_id] = slots;
      }
    });
  }

  async function openLoadoutView() {
    currentMode = 'LOADOUT';
    document.getElementById('btnLoadout').classList.add('active');
    document.getElementById('btnBackModels').style.display = 'none';
    document.getElementById('skinFilters').style.display = 'none';
    document.getElementById('loadoutTabs').style.display = 'flex';
    renderSidebar();
    await renderLoadoutGrid();
  }

  function setLoadoutFilter(filterKey) {
    activeLoadoutFilter = filterKey;
    document.querySelectorAll('.lo-tab').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.filter === filterKey);
    });
    renderLoadoutGrid();
  }

  function wearTag(w) {
    if (w < 0.07) return 'FN';
    if (w < 0.15) return 'MW';
    if (w < 0.38) return 'FT';
    if (w < 0.45) return 'WW';
    return 'BS';
  }

  async function renderLoadoutGrid() {
    await refreshLoadoutCount();

    let filtered = cachedInventory;
    if (activeLoadoutFilter === 'WEAPONS') {
      filtered = cachedInventory.filter(x => !NON_FLOAT_CATEGORIES.has(x.category_name));
    } else if (activeLoadoutFilter === 'AGENTS_MUSIC') {
      filtered = cachedInventory.filter(x => x.category_name === 'Agents' || x.category_name === 'Musiques');
    } else if (activeLoadoutFilter === 'CONTAINERS') {
      filtered = cachedInventory.filter(x => x.category_name === 'Caisses' || x.category_name === 'Clés');
    }

    document.getElementById('stageTitle').innerHTML =
      `LOADOUT <span>${filtered.length} ACTIFS</span>`;

    const container = document.getElementById('stageContainer');
    container.className = 'loadout-grid';

    if (filtered.length === 0) {
      container.innerHTML = `<div style="color:var(--text-lo);font-size:11px;padding:12px;">Aucun élément actif dans cette vue.</div>`;
      return;
    }

    container.innerHTML = filtered.map(item => {
      const eligible = canHaveStickers(item.category_name);
      let stickerRowHtml = '';
      if (eligible) {
        const slotMap = { 0: null, 1: null, 2: null, 3: null };
        (item.stickers || []).forEach(s => { slotMap[s.slot] = s; });
        const boxes = [0, 1, 2, 3].map(slotIdx => {
          const s = slotMap[slotIdx];
          if (!s) return `<div class="lo-stk"></div>`;
          return `<div class="lo-stk filled" title="${s.name}"><img src="${s.image_url}" alt=""></div>`;
        }).join('');
        stickerRowHtml = `<div class="lo-stickers">${boxes}</div>`;
      }

      const isNonFloat = NON_FLOAT_CATEGORIES.has(item.category_name);

      return `
        <div class="lo-card">
          <div class="lo-thumb">
            <img src="${item.image_url}" alt="">
          </div>
          <div class="lo-info">
            <div class="lo-wep">${item.weapon_name}</div>
            <div class="lo-name">${item.skin_name}</div>
            <div class="lo-meta">
              ${!isNonFloat ? `<span class="lo-meta-pill">${wearTag(item.paint_wear)} ${Number(item.paint_wear).toFixed(4)}</span><span class="lo-meta-pill">SEED #${item.paint_seed}</span>` : `<span class="lo-meta-pill">${item.category_name}</span>`}
            </div>
            ${stickerRowHtml}
          </div>
          <button class="lo-del-btn" onclick="removeInventoryItem(${item.item_id})">RETIRER</button>
        </div>
      `;
    }).join('');
  }

  async function removeInventoryItem(itemId) {
    await fetch('/api/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_id: itemId })
    });
    await renderLoadoutGrid();
    showToast(`RETIRÉ DU LOADOUT`, false);
  }

  function showToast(msg, isOk) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = isOk ? 'toast ok' : 'toast';
    t.style.display = 'block';
    clearTimeout(t._timer);
    t._timer = setTimeout(() => { t.style.display = 'none'; }, 3800);
  }

  // --- TACTILE SCI-FI SOUND SYNTHESIZER (WEB AUDIO API) ---
  let audioCtx = null;
  function getAudioCtx() {
    if (!audioCtx && typeof window !== 'undefined') {
      try {
        const AudioClass = window.AudioContext || window.webkitAudioContext;
        if (AudioClass) audioCtx = new AudioClass();
      } catch(e) {}
    }
    return audioCtx;
  }
  function playTactileSfx(type) {
    if (!audioCtx) return;
    try {
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      const now = audioCtx.currentTime;
      if (type === 'hover') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(950, now);
        osc.frequency.exponentialRampToValueAtTime(1400, now + 0.035);
        gain.gain.setValueAtTime(0.012, now);
        gain.gain.linearRampToValueAtTime(0.0, now + 0.035);
        osc.start(now);
        osc.stop(now + 0.035);
      } else if (type === 'click') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1600, now);
        osc.frequency.exponentialRampToValueAtTime(500, now + 0.05);
        gain.gain.setValueAtTime(0.035, now);
        gain.gain.linearRampToValueAtTime(0.0, now + 0.05);
        osc.start(now);
        osc.stop(now + 0.05);
      } else if (type === 'apply') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.exponentialRampToValueAtTime(720, now + 0.16);
        gain.gain.setValueAtTime(0.04, now);
        gain.gain.linearRampToValueAtTime(0.0, now + 0.18);
        osc.start(now);
        osc.stop(now + 0.18);
      } else if (type === 'boot') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(50, now);
        osc.frequency.exponentialRampToValueAtTime(160, now + 0.35);
        gain.gain.setValueAtTime(0.04, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
        osc.start(now);
        osc.stop(now + 0.4);
      } else if (type === 'ready') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, now);
        osc.frequency.setValueAtTime(1320, now + 0.08);
        osc.frequency.setValueAtTime(1760, now + 0.16);
        gain.gain.setValueAtTime(0.035, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
        osc.start(now);
        osc.stop(now + 0.35);
      }
    } catch(e) {}
  }

  // Bind sound triggers to interactions
  document.addEventListener('click', (e) => {
    if (e.target.closest('button, .nav-btn, .skin-card, .lo-item')) {
      playTactileSfx('click');
    }
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Insert') {
      e.preventDefault();
      fetch('/api/overlay/toggle', { method: 'POST' }).catch(() => {});
    } else if (e.key === 'Escape') {
      if (document.getElementById('profileModal') && document.getElementById('profileModal').style.display === 'flex') {
        closeProfileModal();
      } else if (document.getElementById('stickerModal') && document.getElementById('stickerModal').style.display === 'flex') {
        closeStickerModal();
      } else if (document.getElementById('configModal') && document.getElementById('configModal').style.display === 'flex') {
        closeConfigModal();
      } else {
        // Toggle/hide in-game overlay
        fetch('/api/overlay/toggle', { method: 'POST' }).catch(() => {});
      }
    }
  });

  /* Window Controls Handlers for Login & Global View */
  function closeLoaderWindow() {
    try {
      fetch('/api/window/close', { method: 'POST' }).catch(() => {});
    } catch(e) {}
    try {
      if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.close();
      }
    } catch(e) {}
    try {
      if (window.pywebview && window.pywebview.window) {
        window.pywebview.window.destroy();
      }
    } catch(e) {}
    try { window.close(); } catch(e) {}
  }

  function minimizeLoaderWindow() {
    try {
      fetch('/api/window/minimize', { method: 'POST' }).catch(() => {});
    } catch(e) {}
    try {
      if (window.pywebview && window.pywebview.api) {
        window.pywebview.api.minimize();
      }
    } catch(e) {}
    try {
      if (window.pywebview && window.pywebview.window) {
        window.pywebview.window.minimize();
      }
    } catch(e) {}
  }

  initApp();
</script>
</body>
</html>
"""
