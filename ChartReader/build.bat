pyinstaller --name ChartReader.exe --onefile --windowed --hidden-import=numpy._core.multiarray --paths=. __init__.py