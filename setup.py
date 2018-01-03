import sys
import os
import glob

from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = 'C:\\LOCAL_TO_PYTHON\\tcl\\tcl8.6' #Tkinter 라이브러리 파일 위치
os.environ['TK_LIBRARY'] = 'C:\\LOCAL_TO_PYTHON\\tcl\\tk8.6' #Tkinter 라이브러리 파일 위치

build_exe_options = {'packages': ['pandas', 'numpy', 'requests', 'idna'],
                     'excludes': ['PyQt5', 'bokeh', 'cffi', 'Cython', 'sqlite3'],
                     # 'includes': ['tkinter','numpy', 'PIL', 'converter', 'threading', 'xlsxwriter', 'datetime'],
                     'include_msvcr': True,
                     # 'optimize' : 2,
                     }
base = None

if sys.platform == 'win32':
	base = 'Win32GUI'

setup(
	name='Naver Asset',
	version='0.0',
	description='web crawling Naver Asset for YHC',
	author='Wanseok Kim',
	options={'build_exe': build_exe_options},
	executables=[Executable('land.py', base=base)]
)
