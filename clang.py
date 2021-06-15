
# Linting script for cpp files
# run locally

import os
import subprocess
import sys

print("Python {}.{}.{}".format(*sys.version_info))  # Python 3.8


files = []
for dirname, _, filenames in os.walk('../Target-450'):
  if ".git" not in dirname and ".vscode" not in dirname:
    for filename in filenames:
      fileName = os.path.join(dirname, filename).split('\\')[-1] # Get the file name
      files.append(fileName)


cpp_exts = tuple(".c .c++ .cc .cpp .cu .cuh .cxx .h .h++ .hh .hpp .hxx".split())
cpp_files = [file for file in files if file.lower().endswith(cpp_exts)]

if not cpp_files:
  sys.exit(0)

subprocess.run(["clang-tidy-10", "--fix", "-p=build", "--extra-arg=-std=c++17", *cpp_files, "--"], 
    check=True, text=True, stderr=subprocess.STDOUT)

subprocess.run(["clang-format-10", "-i", "-style=file", *cpp_files], 
    check=True, text=True, stderr=subprocess.STDOUT)

space_files = [file for file in cpp_files if " " in file or "-" in file]
if space_files:
  print(f"{len(space_files)} files contain space or dash characters:")
  print("\n".join(space_files) + "\n")

nodir_files = [file for file in cpp_files if file.count(os.sep) != 1]
if nodir_files:
  print(f"{len(nodir_files)} files are not in one and only one directory:")
  print("\n".join(nodir_files) + "\n")

bad_files = len( space_files + nodir_files)
if bad_files:
  sys.exit(bad_files)