import os
import subprocess
import json
from utils.gen_test_python import insert_code, insert_test_code


def gen_all_tests(
    start,
    end,
    except_,
    template_path,
    answer_base_path,
    unit_tests_base_path,
    json_file_path,
):
    with open(json_file_path, "r", encoding="utf-8") as file:
        datas = json.load(file)

    for i in range(start, end):
        if i in except_:
            continue
        answer_path = os.path.join(answer_base_path, str(i) + "/python")
        unit_tests_dir = os.path.join(unit_tests_base_path, str(i))
        if not os.path.exists(unit_tests_dir):
            os.makedirs(unit_tests_dir, exist_ok=True)
        unit_tests_path = os.path.join(unit_tests_dir, "test.py")

        insert_code(
            answer_path, template_path, unit_tests_path, datas[i - 1]["entry_point"]
        )
        insert_test_code(unit_tests_path, unit_tests_path, i)


def run_all_tests(start, end, except_, unit_tests_base_path, log_base_path):
    results = [0] * (end - start)

    for i in range(start, end):
        if i in except_:
            continue
        unit_tests_path = os.path.join(unit_tests_base_path, str(i) + "/test.py")

        print(f"Running test {i}...")
        try:
            run_output = subprocess.check_output(["python3", unit_tests_path], timeout=60)
        except Exception as e:
            print(e)
            run_output = e.output
        run_output = str(run_output)

        log_path = os.path.join(log_base_path, str(i) + ".txt")
        with open(log_path, "w") as file:
            file.write(run_output)

        if run_output.find("All Passed!") != -1:
            print("Test Passed!")
            results[i - start] = 1
        elif run_output.find("Test Failed!") != -1:
            print("Test Failed!")
            results[i - start] = 2
        else:
            print("Compilation Passed!")
            results[i - start] = 3

        print()

    with open(log_path, "w") as file:
        file.write(str(results))

    return results


if __name__ == "__main__":
    template_path = "/home/ubuntu/test_codellm/template/template.py"
    answer_base_path = "/home/ubuntu/test_codellm/datas/gold_answer/"
    unit_tests_base_path = "/home/ubuntu/test_codellm/unit_tests/gold_tests/"
    json_file_path = "/home/ubuntu/test_codellm/datas/datas.json"
    log_base_path = "/home/ubuntu/test_codellm/logs/python"

    start = 90
    end = 96
    except_ = [91, 92, 94]

    gen_all_tests(
        start,
        end,
        except_,
        template_path,
        answer_base_path,
        unit_tests_base_path,
        json_file_path,
    )
    results = run_all_tests(start, end, except_, unit_tests_base_path, log_base_path)
    print(results)
