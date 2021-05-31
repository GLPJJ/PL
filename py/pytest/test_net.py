import ctypes
import os

print(os.name)  # nt -> windows
# print(ctypes.windll.kernel32)
# print(ctypes.cdll.msvcrt)

loadCLib = ctypes.cdll.LoadLibrary

lib = loadCLib(
    "D:\\glp\\GitHub\\PythonNetTest\\PythonNetExt\\Debug\\PythonNetExt.dll")
#lib = loadCLib("D:\\glp\\GitHub\\PythonNetTest\\Test1\\Debug\\Test1.dll")
print("add = ", lib.add(1, 3))

intro = "I'm pythoner 中文"
print(id(intro))
lib.cPrint(intro)
print('***finish1***')

main = "D:\\glp\\GitHub\\PythonNetTest\\PythonNetExt\\Debug\\PythonExe.exe"
if os.path.exists(main):
    os.system(main)
else:
    print("not find exe")

print('***finish2***')
