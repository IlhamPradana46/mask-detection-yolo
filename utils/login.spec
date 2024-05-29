# -*- mode: python ; coding: utf-8 -*-

add_datas = [('audio/*.mp3', 'audio'),
             ('db/users.db', 'db'),
             ('image/*.jpg', 'image'),
             ('image/*.png', 'image'),
             ('models/best_new.pt', 'models'),
             ('utils/utils.py', 'utils'),
             ('ultralytics/*', 'ultralytics'),
             ('interface/*.ui', 'interface'),
             ('*.py', '.')            
]

a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[],
    datas=add_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='login',
)
