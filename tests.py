from functions.get_files_info import get_files_info

from functions.get_file_content import get_file_content

from functions.write_file import write_file

from functions.run_python_file import run_python_file

t1 = run_python_file("calculator", "main.py")
t2 = run_python_file("calculator", "main.py", ["3 + 5"])
t3 = run_python_file("calculator", "tests.py")
t4 = run_python_file("calculator", "../main.py")
t5 = run_python_file("calculator", "nonexistent.py")

print(t1)
print(t2)
print(t3)
print(t4)
print(t5)



def getResults(directory, text):
    if directory == ".":
        return f"Result for current directory:\n" + text

    return f"Result for '{directory}' directory:\n" + text

print(getResults(".", t1))
# print(getResults("pkg", t2))
# print(getResults("/bin", t3))
# print(getResults("../", t4))