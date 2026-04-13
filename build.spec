# -*- mode: python ; coding: utf-8 -*-

import os
import tomllib


block_cipher = None
# SPECPATH is provided by PyInstaller and points to this spec file's directory.
spec_dir = os.path.abspath(globals().get('SPECPATH', os.getcwd()))
main_script = os.path.join(spec_dir, 'src', 'main.py')
assets_src = os.path.join(spec_dir, 'assets')
pyproject_path = os.path.join(spec_dir, 'pyproject.toml')
with open(pyproject_path, 'rb') as f:
    pyproject_data = tomllib.load(f)
project_version = pyproject_data['project']['version']

exe_name = f"NexusDownloadFlow-v{project_version}"
datas = []
if os.path.isdir(assets_src):
    datas.append((assets_src, './assets'))


a = Analysis(
    [main_script],
    pathex=[spec_dir],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name=exe_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
