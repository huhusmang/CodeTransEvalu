import re


def replace_func_name(code_str, entry_point):
    if code_str.find(entry_point) != -1:
        return code_str.replace(entry_point, "testfunc")
    else:
        return code_str


def camel_to_snake(name):
    """
    Convert a camelCase string to snake_case.
    """
    snake = [name[0].lower()]
    for char in name[1:]:
        if char.isupper():
            snake.append("_")
            snake.append(char.lower())
        else:
            snake.append(char)
    return "".join(snake)


def is_matched_keywords(line):
    stripped_line = line.strip()
    if (
        (("else" in line) and ((stripped_line.startswith("else")) or (stripped_line.startswith("}"))))
        or (("if" in line) and (stripped_line.startswith("if")))
        or (("for" in line) and (stripped_line.startswith("for")))
        or (("while" in line) and (stripped_line.startswith("while")))
        or (("switch" in line) and (stripped_line.startswith("switch")))
        or (("case" in line) and ((stripped_line.startswith("case")) or (stripped_line.startswith("}"))))
        or (("do" in line) and (stripped_line.startswith("do")))
        or (("try" in line) and (stripped_line.startswith("try")))
        or (("catch" in line) and ((stripped_line.startswith("catch")) or (stripped_line.startswith("}"))))
    ):
        return True
    else:
        return False
    

def extract_main_func(lines):
    function_def_pattern = re.compile(r".*\s+\b[A-Za-z_][A-Za-z0-9_]*\b\s*\(.*\)\s*\{")
    line_num = -1
    for i, line in enumerate(lines):
        if function_def_pattern.match(line.strip()) and not is_matched_keywords(line):
            if "main" in line:
                line_num = i
                break

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

    if line_num != -1:
        return extract_single_function(line_num)
    else:
        return ""    
