import os
import subprocess
import json
from utils.gen_test_python import insert_test_code, insert_code_str


def run_single_test(
    problem_id,
    template_path,
    answer_json_path,
    unit_tests_path,
    prediction_num,
):
    results = [0] * prediction_num

    with open(answer_json_path, "r", encoding="utf-8") as file:
        answer_json = json.load(file)

    for j in range(prediction_num):
        task_id = str(problem_id) + "_" + str(j)
        index = (problem_id - 1) * prediction_num + j
        answer = answer_json[index]["pro_prediction"]
        main_fun_name = answer_json[index]["main_fun_name"]

        insert_code_str(
            answer, template_path, unit_tests_path, main_fun_name
        )
        insert_test_code(unit_tests_path, unit_tests_path, problem_id)

        print(f"Running task: {task_id}...")
        try:
            run_output = subprocess.check_output(
                ["python", unit_tests_path], timeout=20
            )
        except Exception as e:
            print(e)
            run_output = e.output
        run_output = str(run_output)

        if run_output.find("All Passed!") != -1:
            print("Test Passed!")
            results[j] = 1
        elif run_output.find("name 'testfunc' is not defined") != -1:
            print("Compilation Failed!")
            print(run_output)
            results[j] = 2
        elif run_output.find("Test Failed!") != -1:
            print("Test Failed!\n\n")
            print("Run log:\n" + run_output + "\n\n")
            results[j] = 3
        else:
            print("Unknown error!")
            print(run_output)
            results[j] = 4

    return results


if __name__ == "__main__":
    problem_id = 42
    template_path = "template\\template.py"
    answer_path = "result\\spark\\java_python\\prediction.json"
    unit_tests_path = "unit_tests\\spark\\java_python\\test.py"
    prediction_num = 1

    results = run_single_test(
        problem_id,
        template_path,
        answer_path,
        unit_tests_path,
        prediction_num,
    )

    print(results)
