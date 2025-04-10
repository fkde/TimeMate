# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icons', 'icons'),
        ('/usr/lib/girepository-1.0/AppIndicator3-0.1.typelib', 'girepository-1.0'),
        ('/usr/lib/girepository-1.0/AyatanaAppIndicator3-0.1.typelib', 'girepository-1.0'),
    ],
    hiddenimports=[
        'gi',
        'gi.repository.GLib',
        'gi.repository.GObject',
        'gi.repository.Gtk',
        'gi.repository.AppIndicator3'
    ],
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
    a.binaries,
    a.datas,
    [],
    name='TimeMate',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
