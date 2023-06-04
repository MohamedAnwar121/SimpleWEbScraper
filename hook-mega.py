from PyInstaller.utils.hooks import collect_data_files

# Include the mega module
hiddenimports = ['mega']

# Include any additional data files used by the mega module
datas = collect_data_files('mega')
