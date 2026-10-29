# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None

datas = [
    ('cs2_skins.sqlite3', '.'),
    ('inventory_socache.json', '.'),
    ('licenses.db', '.'),
    ('logo.ico', '.'),
    ('logo.png', '.'),
    ('STYLE.png', '.'),
    ('login_bg.jpg', '.'),
    ('arceus_ascii_spritesheet.png', '.'),
    ('arceus_terminal_pillars_master.jpg', '.'),
    ('arceus_title_ascii.png', '.'),
    ('native/mesa_bridge.dll', 'native'),
    ('native/mesa_injector.exe', 'native'),
    ('native/offsets.hpp', 'native'),
    ('Lootline/x64/Release/ARCEUS.exe', 'Lootline/x64/Release'),
    ('Lootline/x64/Release/Lootline.dll', 'Lootline/x64/Release'),
]

hiddenimports = [
    'license_manager',
    'econ_defs',
    'db',
    'ui_template',
    'webview',
    'webview.platforms.winforms',
    'clr',
    'sqlite3',
    'PIL',
    'ctypes',
    'ctypes.wintypes',
    'json',
    'http.server',
    'urllib.request',
    'urllib.parse',
    'threading',
    'subprocess',
    'shutil',
    'httpx',
    'hashlib',
    'secrets',
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'unittest', 'pydoc'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ARCEUS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='logo.ico',
)
