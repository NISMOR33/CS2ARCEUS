MESA_HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>ARCEUS // CS2 PREMIUM CHEAT</title>
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
    height: 68px;
    padding: 0 12px;
    border-bottom: 1px solid var(--line);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, transparent 100%);
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
    position: relative;
    cursor: pointer;
  }

  .brand-emblem {
    width: 46px;
    height: 46px;
    border-radius: 6px;
    background: radial-gradient(circle at 50% 50%, #1c1c1c 0%, #080808 100%);
    border: 1px solid var(--line-mid);
    box-shadow: 0 0 16px rgba(255, 255, 255, 0.09), inset 0 0 10px rgba(255, 255, 255, 0.04);
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
    box-shadow: 0 0 24px rgba(255, 255, 255, 0.35);
  }

  .brand-logo {
    width: 38px;
    height: 38px;
    object-fit: contain;
    display: block;
    filter: grayscale(1) contrast(1.3) brightness(1.7) drop-shadow(0 0 6px rgba(255, 255, 255, 0.4));
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
    font-size: 14.5px;
    font-weight: 900;
    letter-spacing: 3px;
    color: var(--white);
    line-height: 1;
    display: flex;
    align-items: center;
    gap: 5px;
  }

  .brand-dot {
    width: 4px;
    height: 4px;
    background: var(--white);
    border-radius: 50%;
    box-shadow: 0 0 6px var(--white);
    display: inline-block;
  }

  .brand-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: var(--text-mid);
    text-transform: uppercase;
  }

  .brand-lore-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5px;
    font-weight: 500;
    color: var(--text-lo);
    letter-spacing: 0.8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
    width: 380px;
    height: 380px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -46%);
    background: url('/assets/logo.png') no-repeat center center;
    background-size: contain;
    filter: grayscale(1) brightness(1.8) contrast(1.5);
    opacity: 0.035;
    pointer-events: none;
    z-index: 0;
  }

  .stage-header {
    height: 50px;
    padding: 0 14px;
    background: var(--bg-header);
    border-bottom: 1px solid var(--line);
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    position: relative;
    z-index: 10;
  }

  .plate-matrix-bar {
    display: flex;
    align-items: center;
    gap: 3px;
    background: #060606;
    border: 1px solid var(--line);
    padding: 2px 5px;
    border-radius: var(--radius);
  }

  .plate-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5px;
    font-weight: 700;
    letter-spacing: 1px;
    color: var(--text-lo);
    margin-right: 2px;
  }

  .plate-chip {
    height: 20px;
    padding: 0 6px;
    background: transparent;
    border: 1px solid transparent;
    border-radius: 2px;
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: all 0.12s ease;
  }

  .plate-chip:hover {
    color: var(--white);
    background: #141414;
    border-color: var(--line-mid);
  }

  .plate-chip.active {
    background: var(--white);
    border-color: var(--white);
    color: #050505;
    font-weight: 700;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
  }

  .header-hud-badge {
    display: flex;
    align-items: center;
    gap: 5px;
    margin-left: auto;
  }

  .hud-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
    font-weight: 600;
    color: #666;
    letter-spacing: 0.8px;
    padding: 3px 6px;
    border: 1px solid var(--line);
    border-radius: 2px;
    background: #080808;
    white-space: nowrap;
  }

  .hud-grid-toggle {
    height: 22px;
    padding: 0 6px;
    background: #0a0a0a;
    border: 1px solid var(--line-mid);
    border-radius: 2px;
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5px;
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
    font-family: 'Inter', sans-serif;
    font-size: 12.5px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--white);
    margin-right: auto;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .stage-title span {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 500;
    padding: 2px 6px;
    border-radius: 2px;
    background: #111111;
    border: 1px solid var(--line);
    color: var(--text-mid);
    letter-spacing: 0.3px;
  }

  .header-controls {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .ctrl-input, .ctrl-select {
    height: 28px;
    background: var(--bg-input);
    border: 1px solid var(--line-mid);
    border-radius: var(--radius);
    color: var(--white);
    padding: 0 9px;
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    outline: none;
    transition: border-color 0.1s ease;
  }

  .ctrl-input { width: 170px; }
  .ctrl-input::placeholder { color: var(--text-lo); }
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
    height: 150px;
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

  .cfg-stage::before {
    content: "";
    position: absolute;
    width: 140px;
    height: 140px;
    background: url('/assets/logo.png') no-repeat center center;
    background-size: contain;
    filter: grayscale(1) brightness(1.7) contrast(1.4);
    opacity: 0.07;
    animation: arceus-wheel-rotate 80s linear infinite;
    pointer-events: none;
  }

  @keyframes arceus-wheel-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
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

  /* 5 STICKER SLOTS */
  .cfg-stk-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px;
  }

  .cfg-stk-slot {
    height: 46px;
    background: var(--bg-input);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: relative;
  }

  .cfg-stk-slot:hover, .cfg-stk-slot.active-slot {
    border-color: var(--line-hi);
  }

  .cfg-stk-slot.has-stk {
    border-color: var(--white);
    background: var(--bg-card);
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

  /* MONOCHROME WEAR TRACK & PILLS */
  .wear-spectrum-bar {
    height: 4px;
    width: 100%;
    background: #1A1A1A;
    border-radius: 2px;
    margin: 2px 0 3px;
    position: relative;
  }

  .wear-pointer {
    position: absolute;
    top: -3px;
    width: 3px;
    height: 10px;
    background: var(--white);
    transform: translateX(-50%);
    left: 0.1%;
    pointer-events: none;
  }

  .wear-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 4px;
  }

  .wear-pill {
    height: 24px;
    background: var(--bg-input);
    border: 1px solid var(--line);
    border-radius: 2px;
    color: var(--text-mid);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.1s ease;
  }

  .wear-pill:hover {
    border-color: var(--line-hi);
    color: var(--white);
  }

  .wear-pill.active {
    background: var(--white);
    border-color: var(--white);
    color: #050505;
    font-weight: 700;
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
</style>
</head>
<body>

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar">
    <div class="brand" onclick="triggerJudgmentEasterEgg()" title="ARCEUS #0493 // CLIC POUR PROTOCOLE JUGEMENT">
      <div class="brand-emblem">
        <img class="brand-logo" id="brandLogoImg" src="/assets/logo.png" alt="ARCEUS">
      </div>
      <div class="brand-text-wrap">
        <div class="brand-name">ARCEUS <span class="brand-dot"></span></div>
        <div class="brand-tag">#0493 // CS2 CHANGER</div>
        <div class="brand-lore-pill">HALL OF ORIGIN // 1000 ARMS</div>
      </div>
    </div>

    <div class="nav-section-lbl">ARSENAL</div>
    <nav class="nav-list" id="navList"></nav>

    <div class="sidebar-footer">
      <div class="arceus-lore-box">
        <div class="lore-row">
          <span class="lore-k">CORE</span>
          <span class="lore-v">ORIGIN FORME #493</span>
        </div>
        <div class="lore-row">
          <span class="lore-k">MATRIX</span>
          <span class="lore-v" id="activePlateStatus">MULTITYPE // CELESTIAL</span>
        </div>
      </div>

      <div class="telemetry-card">
        <div class="bridge-pill" id="bridgeStatusPill" title="Statut de connexion avec cs2.exe">
          <span class="bridge-dot"></span>
          <span id="bridgeStatusText">MODE LOCAL</span>
        </div>
        <div class="step-mini-row">
          <div class="step-chip" id="stepChipDll" title="Étape 1 : DLL chargée">DLL</div>
          <div class="step-chip" id="stepChipJson" title="Étape 2 : JSON lu">JSON</div>
          <div class="step-chip" id="stepChipAdd" title="Étape 3 : Objet ajouté">ADD</div>
          <div class="step-chip" id="stepChipEq" title="Étape 4 : Objet équipé">EQUIP</div>
        </div>
      </div>
      <button class="loadout-trigger" id="btnLoadout" onclick="openLoadoutView()">
        <span>LOADOUT // INVENTAIRE</span>
        <span class="loadout-badge" id="loadoutCount">0</span>
      </button>
    </div>
  </aside>

  <!-- MAIN CONTENT STAGE -->
  <main class="main-stage">
    <div class="tactical-grid-overlay" id="tacticalGrid"></div>

    <header class="stage-header">
      <button class="back-btn" id="btnBackModels" onclick="backToModels()">
        ← MODÈLES
      </button>

      <div class="stage-title" id="stageTitle">
        COUTEAUX <span>20 MODÈLES</span>
      </div>

      <!-- ARCEUS PLATE MATRIX -->
      <div class="plate-matrix-bar" id="plateMatrixBar">
        <span class="plate-lbl">PLATE :</span>
        <button class="plate-chip active" data-plate="ORIGIN" onclick="selectPlate('ORIGIN')" title="Multitype : Tous les skins">★ ORIGIN</button>
        <button class="plate-chip" data-plate="DRACO" onclick="selectPlate('DRACO')" title="Draco Plate : Secrètes & Classifiées">DRACO</button>
        <button class="plate-chip" data-plate="IRON" onclick="selectPlate('IRON')" title="Iron Plate : Case Hardened & Blue Gem">IRON</button>
        <button class="plate-chip" data-plate="DREAD" onclick="selectPlate('DREAD')" title="Dread Plate : StatTrak uniquement">DREAD</button>
        <button class="plate-chip" data-plate="PIXIE" onclick="selectPlate('PIXIE')" title="Pixie Plate : Crafts Stickers">PIXIE</button>
      </div>

      <div class="header-hud-badge">
        <span class="hud-mono">#0493 // CORE</span>
        <button class="hud-grid-toggle" id="btnGridToggle" onclick="toggleScanlines()" title="Activer / Désactiver la grille tactique">[GRID]</button>
      </div>

      <div class="header-controls" id="skinFilters" style="display:none;">
        <input type="text" class="ctrl-input" id="searchInput" placeholder="Rechercher un skin..." oninput="debounceSkins()">
        <select class="ctrl-select" id="raritySelect" onchange="loadSkinsForWeapon()">
          <option value="0">Toutes raretés</option>
          <option value="7">Or / Contrebande</option>
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
          <span class="cfg-top-pill">#0493</span>
          <span>HALL OF ORIGIN // SOCACHE INJECTOR</span>
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
              <span>STICKERS (5 SLOTS)</span>
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
              <span>USURE (FLOAT)</span>
              <span class="cfg-lbl-val" id="cfgFloatVal">FN • 0.00100</span>
            </div>
            <div class="wear-spectrum-bar">
              <div class="wear-pointer" id="wearPointer"></div>
            </div>
            <div class="wear-row">
              <button class="wear-pill" onclick="setWear(0.000493, this)" title="Origin Celestial Float 0.000493">★ 0.000493</button>
              <button class="wear-pill active" onclick="setWear(0.001, this)">FN</button>
              <button class="wear-pill" onclick="setWear(0.08, this)">MW</button>
              <button class="wear-pill" onclick="setWear(0.18, this)">FT</button>
              <button class="wear-pill" onclick="setWear(0.40, this)">WW</button>
              <button class="wear-pill" onclick="setWear(0.65, this)">BS</button>
            </div>
            <input type="range" id="cfgFloatSlider" min="0" max="1" step="0.00001" value="0.001" oninput="syncFloatSlider()">
          </div>

          <div class="cfg-2col" id="cfgSeedStSection">
            <div class="cfg-stickers-box">
              <div class="cfg-lbl-row">
                <span>PATTERN SEED</span>
                <div class="seed-chip-row">
                  <span class="seed-chip" onclick="setQuickSeed(493)" title="★ Pokedex #493 Arceus">★ #493</span>
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
                <span class="seed-chip" onclick="setQuickName('Judgement #493')">Judgement</span>
                <span class="seed-chip" onclick="setQuickName('Hall of Origin')">Origin</span>
                <span class="seed-chip" onclick="setQuickName('1000 Arms')">1000 Arms</span>
              </div>
            </div>
            <input type="text" class="cfg-input" id="cfgNameInput" placeholder="Optionnel (ex: Judgement #493)">
          </div>

          <button class="btn-add-ingame" onclick="addInGame()">APPLIQUER IN-GAME</button>
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

  /* 5 SLOTS STICKERS ISOLÉS PAR SKIN_ID */
  const stickersBySkinId = {};

  const STICKER_ELIGIBLE_CATEGORIES = new Set(['Fusils', 'Pistolets', 'PM', 'Lourde']);
  const NON_FLOAT_CATEGORIES = new Set(['Agents', 'Musiques', 'Caisses', 'Clés']);

  /* DÉTOURAGE AUTOMATIQUE DU FOND BLANC EXTERNE DE LOGO.PNG */
  function prepareTransparentLogo() {
    const imgEl = document.getElementById('brandLogoImg');
    if (!imgEl) return;
    const probe = new Image();
    probe.crossOrigin = 'anonymous';
    probe.onload = () => {
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
    };
    probe.src = '/assets/logo.png';
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

  function triggerJudgmentEasterEgg() {
    document.body.classList.remove('judgment-pulse');
    void document.body.offsetWidth;
    document.body.classList.add('judgment-pulse');
    showToast('★ ARCEUS #0493 // PROTOCOLE JUGEMENT ENGAGÉ (1000 ARMS SYNC)');
  }

  function selectPlate(plateName) {
    document.querySelectorAll('.plate-chip').forEach(b => {
      b.classList.toggle('active', b.dataset.plate === plateName);
    });

    const statusEl = document.getElementById('activePlateStatus');
    const raritySel = document.getElementById('raritySelect');
    const searchInp = document.getElementById('searchInput');

    if (plateName === 'DRACO') {
      if (raritySel) raritySel.value = '6';
      if (statusEl) statusEl.textContent = 'DRACO // COVERT MATRIX';
      showToast('[PLATE: DRACO] FILTRE SECRÈTE & CLASSIFIÉE');
    } else if (plateName === 'IRON') {
      if (searchInp) searchInp.value = 'Case Hardened';
      if (statusEl) statusEl.textContent = 'IRON // BLUE GEM MATRIX';
      showToast('[PLATE: IRON] RECHERCHE CASE HARDENED & BLEU');
    } else if (plateName === 'DREAD') {
      if (searchInp) searchInp.value = 'StatTrak';
      if (statusEl) statusEl.textContent = 'DREAD // STATTRAK MATRIX';
      showToast('[PLATE: DREAD] FOCUS STATTRAK ACTIF');
    } else if (plateName === 'PIXIE') {
      if (statusEl) statusEl.textContent = 'PIXIE // CRAFT STICKERS';
      showToast('[PLATE: PIXIE] BANC DE CRAFT STICKERS');
      openCategoryModels('Fusils');
      return;
    } else {
      if (raritySel) raritySel.value = '0';
      if (searchInp) searchInp.value = '';
      if (statusEl) statusEl.textContent = 'MULTITYPE // CELESTIAL';
      showToast('[PLATE: ORIGIN] RÉINITIALISATION MULTITYPE');
    }

    if (currentMode === 'SKINS') {
      loadSkinsForWeapon();
    }
  }

  function canHaveStickers(categoryName) {
    return STICKER_ELIGIBLE_CATEGORIES.has(categoryName);
  }

  function getSkinStickerSlots(skinId) {
    if (!skinId) return [null, null, null, null, null];
    if (!stickersBySkinId[skinId]) {
      stickersBySkinId[skinId] = [null, null, null, null, null];
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

  async function initApp() {
    prepareTransparentLogo();
    const res = await fetch('/api/nav');
    navData = await res.json();
    if (navData.categories.length > 0) {
      activeCategory = navData.categories[0].name;
    }
    await refreshLoadoutCount();
    await refreshBridgeStatus();
    renderSidebar();
    openCategoryModels(activeCategory);
  }

  async function refreshBridgeStatus() {
    try {
      const res = await fetch('/api/status');
      const st = await res.json();
      const pill = document.getElementById('bridgeStatusPill');
      const txt = document.getElementById('bridgeStatusText');
      const steps = st.steps || {};
      updateStepChips(steps);
      if (st.synced) {
        pill.classList.add('connected');
        txt.textContent = 'CS2 CONNECTÉ';
        pill.title = st.reason || 'Bridge actif dans cs2.exe';
      } else if (steps.dll_loaded) {
        pill.classList.remove('connected');
        txt.textContent = 'DLL CHARGÉE';
        pill.title = st.reason || 'DLL chargée, en attente de lecture JSON';
      } else {
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
    container.innerHTML = weapons.map(w => `
      <div class="model-card" onclick="openWeaponSkins('${w.weapon_name.replace(/'/g, "\\'")}', false)">
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
           style="--rarity-col: ${item.rarity_color || '#FFFFFF'}"
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

    const noFloat = NON_FLOAT_CATEGORIES.has(item.category_name);
    const eligibleForStickers = canHaveStickers(item.category_name);
    const isGlove = item.category_name === 'Gants';
    const isContainer = item.category_name === 'Caisses' || item.category_name === 'Clés';

    document.getElementById('cfgWearSection').style.display = noFloat ? 'none' : 'flex';
    document.getElementById('cfgSeedStSection').style.display = noFloat ? 'none' : 'grid';
    document.getElementById('cfgStBox').style.display = isGlove ? 'none' : 'flex';
    document.getElementById('cfgStickerSection').style.display = eligibleForStickers ? 'flex' : 'none';
    document.getElementById('cfgNameSection').style.display = (noFloat || isGlove || isContainer) ? 'none' : 'flex';

    if (!noFloat) {
      const slider = document.getElementById('cfgFloatSlider');
      slider.min = item.min_float;
      slider.max = item.max_float;
      slider.value = Math.max(item.min_float, Math.min(item.max_float, 0.001));
      syncFloatSlider();
    }

    renderConfigStickerSlots();
    document.getElementById('configModal').style.display = 'flex';
  }

  function closeConfigModal() {
    document.getElementById('configModal').style.display = 'none';
  }

  function setWear(val, btn) {
    if (!selectedSkin) return;
    document.querySelectorAll('.wear-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const slider = document.getElementById('cfgFloatSlider');
    slider.value = Math.max(selectedSkin.min_float, Math.min(selectedSkin.max_float, val));
    syncFloatSlider();
  }

  function syncFloatSlider() {
    const val = parseFloat(document.getElementById('cfgFloatSlider').value || 0.001);
    document.getElementById('cfgFloatVal').textContent = `${wearTag(val)} • ${val.toFixed(5)}`;
    const ptr = document.getElementById('wearPointer');
    if (ptr) {
      ptr.style.left = `${Math.max(1, Math.min(99, val * 100))}%`;
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
          <div class="cfg-stk-slot ${idx === activeStickerSlotIndex ? 'active-slot' : ''}" onclick="openStickerModal(${idx})">
            <span style="font-size:13px;color:var(--text-mid);">+</span>
            <span>0${idx + 1}</span>
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
    stickersBySkinId[selectedSkin.skin_id] = [null, null, null, null, null];
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
        const slots = [null, null, null, null, null];
        item.stickers.forEach(s => {
          if (s && s.slot >= 0 && s.slot < 5) slots[s.slot] = s;
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
        const slotMap = { 0: null, 1: null, 2: null, 3: null, 4: null };
        (item.stickers || []).forEach(s => { slotMap[s.slot] = s; });
        const boxes = [0, 1, 2, 3, 4].map(slotIdx => {
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

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (document.getElementById('stickerModal').style.display === 'flex') {
        closeStickerModal();
      } else {
        closeConfigModal();
      }
    }
  });

  initApp();
</script>
</body>
</html>
"""
