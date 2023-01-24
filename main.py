import inspect
import re
import inputCode as module

funcs = []
for name, value in vars(module).items():
    if name.startswith("_") or not callable(value):
        continue
    doc = inspect.getdoc(value)
    code = inspect.getsource(value).split(":", maxsplit=1)[1]
    funcs.append({"name": name, "docstring": doc, "body": code})

dic=dict()
for func in funcs:
    dic[func['name']+"()"]=func['body']


def extract_user_defined_function_calls(code: str) -> list:
    function_def_pattern = r"^def\s+(?P<func_name>\w+)\s*\("
    function_list = []
    for match in re.finditer(function_def_pattern, code, re.MULTILINE):
        function_list.append(match.group("func_name"))
    return function_list


def replace_function_calls(code: str) -> str:
    function_list = extract_user_defined_function_calls(code)
    function_calls_pattern = r"(?<=(\t))(?P<func_call>\w+\s*)\((?:[^)]+)?\)"
    normalized_code = code.replace("    ", "\t").replace("        ", "\t")
    replaced = re.sub(function_calls_pattern, lambda match: dic[match.group()] if match.group("func_call") in function_list else match.group(), normalized_code)
    return replaced


    

codeFile=open('inputCode.py')
str=""
for line in codeFile:

  str+=line

print(replace_function_calls(str))

