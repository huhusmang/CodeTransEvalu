import re
from .extract_func_name import extract_main_function_name
from .util import is_matched_keywords


def extract_code(input_str, language, entry_point):
    """
    Extracts code from a given input string based on the specified language and entry point.

    Args:
        input_str (str): The input string containing code snippets.
        language (str): The language of the code snippets to extract.
        entry_point (str): The entry point or main function name to identify relevant code.

    Returns:
        tuple: A tuple containing the extracted code and the main function name.
    """
    if language == "c++":
        language = "cpp"

    input_str = input_str.replace("\\n", "\n").replace('\\"', '"')
    pattern = r"```" + language + r"\n(.*?)\n```"
    matches = re.findall(pattern, input_str, re.DOTALL)
    if not matches and language == "cpp":
        pattern = r"```c\+\+\n(.*?)\n```"
        matches = re.findall(pattern, input_str, re.DOTALL)

    if not matches:
        pattern = r"```\n(.*?)\n```"
        matches = re.findall(pattern, input_str, re.DOTALL)

    if matches:
        pro_code = matches[0]
    else:
        pro_code = input_str

    main_fun_name = extract_main_function_name(pro_code, entry_point, language)
    try:
        result = extract_relevant_functions(pro_code, main_fun_name, language)
    except:
        result = pro_code

    return result, main_fun_name


def extract_relevant_functions(code, main_function_name, language):
    """
    Extracts the main function and any functions it calls from the code.
    """
    if language == "python":
        return extract_relevant_python_functions(code, main_function_name)
    elif language == "java":
        return extract_relevant_java_functions(code, main_function_name)
    elif language == "cpp":
        return extract_relevant_cpp_functions(code, main_function_name)
    else:
        return code


def adjust_indentation(code_str):
    lines = code_str.split("\n")
    # Find the first non-empty line to determine the base indentation
    for line in lines:
        stripped_line = line.lstrip()
        if stripped_line:
            base_indentation = len(line) - len(stripped_line)
            break

    # Remove the base indentation from all lines
    adjusted_lines = [
        line[base_indentation:] if len(line) > base_indentation else line
        for line in lines
    ]
    return "\n".join(adjusted_lines)


def extract_relevant_python_functions(code, main_function_name):
    """
    Extracts the main function and any functions it calls from the Python code.
    """
    # Split the code into lines
    lines = code.split("\n")

    # Extract all function names and their start line numbers
    function_names = {}
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            function_name = line.split("(")[0].replace("def ", "").strip()
            if (
                function_name == "__init__"
                or function_name == "TreeNode"
                or function_name == "ListNode"
            ):
                continue
            function_names[function_name] = i

    # Helper function to extract a single function
    def extract_single_function(start_line):
        function_lines = []
        indent_level = None
        for line_num, line in enumerate(lines[start_line:]):
            stripped_line = line.strip()
            if stripped_line:
                if indent_level is None:
                    indent_level = len(line) - len(stripped_line)
                if (
                    not stripped_line.startswith("def ")
                    and len(line) - len(stripped_line) == indent_level
                ) or (
                    stripped_line.startswith("def ")
                    and len(line) - len(stripped_line) == indent_level
                    and line_num != 0
                ):
                    break
            function_lines.append(line)
        return "\n".join(function_lines)

    # Extract the main function
    extracted_functions = [extract_single_function(function_names[main_function_name])]

    # Check for and extract any called functions within the main function
    for name in function_names:
        if (
            name != main_function_name
            and name in extracted_functions[0]
            and re.findall(r"def\s+" + name + r"\s*\(", extracted_functions[0]) == []
        ):
            extracted_functions.append(extract_single_function(function_names[name]))
        elif (
            len(extracted_functions) > 1
            and name in extracted_functions[1]
            and re.findall(r"def\s+" + name + r"\s*\(", extracted_functions[1]) == []
        ):
            extracted_functions.append(extract_single_function(function_names[name]))

    code_str = "\n\n".join(extracted_functions)
    # delete self
    code_str = code_str.replace("self,", "").replace("self.", "")
    return adjust_indentation(code_str)


def add_public_static(function_lines):
    """
    Add public static to the code_str.
    """
    declare_line = function_lines[0]
    declare_line = (
        declare_line.replace("public", "")
        .replace("static", "")
        .replace("private", "")
        .replace("protected", "")
        .strip()
    )
    function_lines[0] = "public static " + declare_line


def extract_relevant_java_functions(code, main_function_name):
    """
    Extracts the main function and any functions it calls from the Java class code.
    """
    # Split the code into lines
    lines = code.split("\n")

    # Extract all function names and their start line numbers
    function_names = {}
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")
    for i, line in enumerate(lines):
        if (
            (
                line.strip().startswith("public static")
                or line.strip().startswith("public ")
                or line.strip().startswith("private static")
                or line.strip().startswith("private ")
            )
            and "(" in line
            and ")" in line
            and "{" in line
        ) or function_def_pattern.match(line.strip()):
            if is_matched_keywords(line):
                continue
            function_name = line.split("(")[0].split()[-1]
            if (
                function_name == "main"
                or function_name == "Main"
                or function_name == "TreeNode"
                or function_name == "ListNode"
                or function_name == "TreeNode*"
                or function_name == "ListNode*"
            ):
                continue
            function_names[function_name] = i

    # Helper function to extract a single function
    def extract_single_function(start_line):
        function_lines = []
        brace_count = 0
        for line in lines[start_line:]:
            if "{" in line:
                brace_count += line.count("{")
            if "}" in line:
                brace_count -= line.count("}")
            function_lines.append(line)
            if brace_count == 0:
                break
        add_public_static(function_lines)
        return "\n".join(function_lines)

    # Extract the main function
    extracted_functions = [extract_single_function(function_names[main_function_name])]

    # Check for and extract any called functions within the main function
    for name in function_names:
        if name != main_function_name:
            if name in extracted_functions[0]:
                extracted_functions.append(
                    extract_single_function(function_names[name])
                )
            elif len(extracted_functions) > 1 and name in extracted_functions[1]:
                extracted_functions.append(
                    extract_single_function(function_names[name])
                )
            elif len(extracted_functions) > 2 and name in extracted_functions[2]:
                extracted_functions.append(
                    extract_single_function(function_names[name])
                )

    return "\n\n".join(extracted_functions)


def extract_relevant_cpp_functions(code, main_function_name):
    """
    Extracts the main function and any functions it calls from the C++ code.
    """
    # Split the code into lines
    lines = code.split("\n")

    # Regex pattern for C++ function definition
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")

    # Extract all function names and their start line numbers
    function_names = {}
    for i, line in enumerate(lines):
        if function_def_pattern.match(line.strip()):
            # if (("else" in line) and ("if" in line)) or ("if (" in line) or ("for (" in line) or ("while (" in line):
            if is_matched_keywords(line):
                continue
            function_name = line.split("(")[0].split()[-1].strip()
            if (
                function_name == "main"
                or function_name == "Main"
                or function_name == "TreeNode"
                or function_name == "ListNode"
                or function_name == "TreeNode*"
                or function_name == "ListNode*"
            ):
                continue
            function_names[function_name] = i

    # Helper function to extract a single function
    def extract_single_function(start_line):
        function_lines = []
        brace_count = 0
        for line in lines[start_line:]:
            if "{" in line:
                brace_count += line.count("{")
            if "}" in line:
                brace_count -= line.count("}")
            function_lines.append(line)
            if brace_count == 0:
                break
        return "\n".join(function_lines)

    # Extract the main function
    extracted_functions = [extract_single_function(function_names[main_function_name])]

    # Check for and extract any called functions within the main function
    for name in function_names:
        if name != main_function_name:
            if name in extracted_functions[0]:
                extracted_functions.append(
                    extract_single_function(function_names[name])
                )
            elif len(extracted_functions) > 1 and name in extracted_functions[1]:
                extracted_functions.append(
                    extract_single_function(function_names[name])
                )
            elif len(extracted_functions) > 2 and name in extracted_functions[2]:
                extracted_functions.append(
                    extract_single_function(function_names[name])
                )

    return "\n\n".join(extracted_functions)


def extract_code_(input_str, language="java", pattern=2, replace=True):
    """
    Extracts the code from the given input string.

    Parameters:
    input_str (str): The input string containing the code.
    language (str, optional): The language of the code. Defaults to "java".
    pattern (int, optional): The pattern to use for extracting the code. Defaults to 2.
    replace (bool, optional): Whether to replace the escaped newline characters with actual newline characters. Defaults to True.

    Returns:
    str: The extracted code.
    """

    pattern1 = r"```" + language + r"\n(.*?)\n```"
    pattern2 = r"```" + language + r"\\n(.*?)\\n```"

    pattern_ = pattern1 if pattern == 1 else pattern2

    matches = re.findall(pattern_, input_str, re.DOTALL)

    result = matches[0] if matches else ""
    if replace:
        result = result.replace("\\n", "\n")

    return result


if __name__ == "__main__":
    """
    Response really returns `true_returned_str`, but print returns `print_returned_str`, because print escapes the string, and the string written into the file is also the escaped string. 
    However, when the string written into the file is read out, the escape character is automatically converted to the original character, that is, `true_returned_str`.
    """
    print_returned_str = " [java]:\n\n```java\npublic int testfunc(int[] nums, int k) {\n    int ans = 0;\n    for (int i = 0; i < 31; i++) {\n        int cnt1 = 0;\n        for (int x : nums) {\n            cnt1 += x >> i & 1;\n        }\n        if (cnt1 >= k) {\n            ans |= 1 << i;\n        }\n    }\n    return ans;\n}\n```"
    true_returned_str = '" [java]:\\n\\n```java\\nint testfunc(int[] nums, int k) {\\n    int ans = 0;\\n    for (int i = 0; i < 31; i++) {\\n        int cnt1 = 0;\\n        for (int x : nums) {\\n            cnt1 += x >> i & 1;\\n        }\\n        if (cnt1 >= k) {\\n            ans |= 1 << i;\\n        }\\n    }\\n    return ans;\\n}\\n```"'

    extracted_code_blocks_1 = extract_code(print_returned_str, pattern=1)
    extracted_code_blocks_2 = extract_code(true_returned_str)
    extracted_code_blocks_3 = extract_code(eval(true_returned_str), pattern=1)

    print(extracted_code_blocks_2)
