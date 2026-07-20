# PyInstaller spec — build with:  pyinstaller packaging/backtester.spec
# Produces dist/PythonBacktester/ (one-folder app; run PythonBacktester.exe).
#
# The strategies/ folder is bundled read-only for reference, but the app also
# loads strategies from a `strategies/` folder next to the executable at
# runtime, so users can drop in their own .py files without rebuilding.

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

project_root = Path(SPECPATH).resolve().parent

hiddenimports = (
    collect_submodules("pyqtgraph")
    + collect_submodules("backtester.strategy.examples")
)

datas = [(str(project_root / "strategies"), "strategies")]

a = Analysis(
    [str(project_root / "app.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    # Trim heavy libs we don't use to keep the bundle smaller.
    excludes=["tkinter", "matplotlib", "PyQt5", "PyQt6", "test", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PythonBacktester",
    console=False,          # GUI app: no console window
    disable_windowed_traceback=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="PythonBacktester",
)
