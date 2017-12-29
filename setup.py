import sys
import os
import glob

from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'C:\\LOCAL_TO_PYTHON\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\LOCAL_TO_PYTHON\\tcl\\tk8.6'

# exclude_module_path = os.path.join(
# 	os.path.split(sys.executable)[0], 'Lib/site-packages/*')

# fileList = glob.glob(exclude_module_path)

# moduleList = []
# for mod in fileList:
#     modules = os.path.splitext(os.path.basename(mod))[0]
#     moduleList.append(modules)

build_exe_options = {'packages': ['pandas', 'numpy', 'requests'],
                     'excludes': ['PyQt5', 'bokeh', 'cffi', 'Cython', 'sqlite3'],
                     # 'includes': ['tkinter','numpy', 'PIL', 'converter', 'threading', 'xlsxwriter', 'datetime'],
                     'include_msvcr': True,
                     # 'optimize' : 2,
                     }
base = None

if sys.platform == 'win32':
	base = 'Win32GUI'

setup(
	name='Order Converter',
	version='0.0',
	description='Woochang Order Converter',
	author='Wanseok Kim',
	options={'build_exe': build_exe_options},
	executables=[Executable('land.py', base=base)]
)
