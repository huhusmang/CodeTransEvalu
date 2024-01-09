import re
from .util import is_matched_keywords, extract_main_func

def extract_python_main_function_name_(code):
    """
    Extracts the main function name from a given (Python) code snippet.
    The main function is considered the one that is not called within other functions.
    """
    # Split the code into lines
    lines = code.split("\n")

    # Extract all function names
    function_names = set()
    for line in lines:
        line = line.strip()
        if line.startswith("def "):
            function_name = line.split("(")[0].replace("def ", "").strip()
            function_names.add(function_name)

    # Check for function calls
    for line in lines:
        for function in function_names.copy():
            if f"{function}(" in line and not line.startswith("def "):
                function_names.discard(function)

    # The remaining function name is considered the main function
    return function_names


def extract_python_main_function_name(code):
    """
    Extracts the main function name from a given (Python) code snippet.
    The main function is considered the one that is not called within other functions.
    """
    # Split the code into lines
    lines = code.split("\n")

    # Extract all function names
    function_names = set()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("def "):
            function_name = stripped_line.split("(")[0].replace("def ", "").strip()
            if (
                function_name == "__init__"
                or function_name == "TreeNode"
                or function_name == "ListNode"
            ):
                continue
            function_names.add(function_name)

    # Initialize a variable to track whether the current line is inside a function
    inside_function = False

    # Check for function calls
    for line in lines:
        stripped_line = line.strip()

        # Check if entering or exiting a function
        if stripped_line.startswith("def "):
            inside_function = True
        elif line == "" or line.startswith("#"):
            continue
        elif inside_function and re.match(r"^\s+", line):
            # Check if the line is a function call within a function body
            for function in function_names.copy():
                if f"{function}(" in stripped_line and not stripped_line.startswith(
                    "def "
                ) and len(function_names) > 1:
                    function_names.discard(function)
        elif not re.match(r"^\s+", line):
            inside_function = False

    # The remaining function name is considered the main function
    return function_names


def extract_java_main_function_name(code):
    """
    Extracts the main function name from a given (java) code snippet.
    The main function is considered the one that is not called within other functions.
    """
    # Split the code into lines
    lines = code.split("\n")

    if "main" in code:
        main_code_str = extract_main_func(lines)
    else:
        main_code_str = ""

    # Extract all function names
    function_names = set()
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")
    for line in lines:
        line = line.strip()
        if (
            (
                line.startswith("public ")
                or line.startswith("static ")
                or line.startswith("private ")
            )
            and "(" in line
            and ")" in line
            and "{" in line
        ) or function_def_pattern.match(line.strip()):
            # if ("else " in line) or ("if " in line) or ("if(" in line) or ("for " in line) or ("for(" in line) or ("while " in line) or ("while(" in line):
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
            function_names.add(function_name)

    # Check for function calls
    for line in lines:
        line = line.strip()
        if (
            (
                line.startswith("public ")
                or line.startswith("static ")
                or line.startswith("private ")
            )
            and "(" in line
            and ")" in line
        ) or (function_def_pattern.match(line.strip()) and not is_matched_keywords(line)):
            continue
        for function in function_names.copy():
            # len(function_names) > 1 间接的保证了main函数中的调用不会删除 main_function_name
            if f"{function}(" in line and len(function_names) > 1 and (function not in main_code_str):
                function_names.discard(function)

    return function_names


def extract_cpp_main_function_name(code):
    """
    Extracts the main function name from a given C++ code snippet.
    Improved version to more accurately identify function definitions.
    """
    # Split the code into lines
    lines = code.split("\n")

    # Regex pattern for C++ function definition (simplified)
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")

    # Extract all function names
    function_names = set()
    for line in lines:
        if function_def_pattern.match(line.strip()):
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
            function_names.add(function_name)

    # Check for function calls
    for line in lines:
        for function in function_names.copy():
            if (function_def_pattern.match(line.strip()) and not is_matched_keywords(line)):
                continue
            # 修复函数调用自己的情况
            if f"{function}(" in line and len(function_names) > 1:
                function_names.discard(function)

    # The remaining function name is considered the main function
    return function_names


def extract_main_function_name(code, entry_point, language):
    if code.find(entry_point) != -1:
        return entry_point

    if language == "java":
        function_names = extract_java_main_function_name(code)
    elif language == "python":
        function_names = extract_python_main_function_name(code)
    elif language == "cpp":
        function_names = extract_cpp_main_function_name(code)
    else:
        function_names = set()

    if len(function_names) > 0:
        return function_names.pop()
    else:
        return entry_point


if __name__ == "__main__":
    code = '" [python]\ndef find_k_or(nums: List[int], k: int) -> int:\n    ANS = 0\n    for i in range(31):\n        CNT1 = 0\n        for x in nums:\n            CNT1 += (x >> i) & 1\n        if CNT1 >= k:\n            ANS |= 1 << i\n    return ANS\n\n# Test the function\nnums = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]\nk = 5\nprint(find_k_or(nums, k))  # Output: 5"'
    print(code)
    # print(extract_python_main_function_name(code))
