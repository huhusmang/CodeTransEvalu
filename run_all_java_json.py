import os
import subprocess
import json
import logging
import datetime
import re
from utils.gen_test_java import insert_code_str, generate_test_code, insert_testcases


def json_data(task, problem_id, prediciton_id, answer_type, number):
    data = {
        "task": task,
        "problem_id": problem_id,
        "prediction_id": prediciton_id,
        "answer_type": answer_type,
        "Passed_testcase_nums": number,
    }

    return data


def load_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        datas = json.load(file)

    return datas


def run_tests(
    start,
    end,
    except_,
    template_path,
    answer_json_path,
    unit_tests_path,
    results_path,
    json_file_path,
    prediction_num,
    logger,
):
    results = [[0] * prediction_num for _ in range(end - start)]
    json_results = []

    datas = load_json(json_file_path)
    answer_json = load_json(answer_json_path)

    task = answer_json[0]["task"]

    for i in range(start, end):
        if i in except_:
            continue

        for j in range(prediction_num):
            task_id = str(i) + "_" + str(j)
            index = (i - 1) * prediction_num + j
            answer = answer_json[index]["pro_prediction"]
            main_fun_name = answer_json[index]["main_fun_name"]

            insert_code_str(answer, template_path, unit_tests_path, main_fun_name)

            input_type = datas[i - 1]["params"]["java"]["paramsType"]
            output_type = datas[i - 1]["params"]["java"]["returnType"]
            code = generate_test_code(input_type, output_type, i)

            insert_testcases(code, unit_tests_path, unit_tests_path)

            logger.info(f"Running task: {task_id}...")
            try:
                run_output = subprocess.check_output(
                    ["java", unit_tests_path], stderr=subprocess.STDOUT, timeout=60
                )
            except subprocess.TimeoutExpired:
                run_output = "Timeout"
            except Exception as e:
                run_output = e.output
            run_output = str(run_output)

            if run_output.find("Timeout") != -1:
                logger.info("Timeout!")
                results[i - start][j] = 5
            elif run_output.find("All Passed!") != -1:
                logger.info("Test Passed!\n\n")
                results[i - start][j] = 1
            elif run_output.find("compilation failed") != -1:
                logger.info("Compilation Failed!")
                logger.info(f"run_output: {run_output}" + "\n\n")
                results[i - start][j] = 2
            elif run_output.find("Exception") != -1:
                logger.info("Runtime Failed!")
                logger.info(f"run_output: {run_output}" + "\n\n")
                results[i - start][j] = 3
            elif run_output.find("Test Failed!") != -1:
                logger.info("Test Failed!")
                logger.info(f"run_output: {run_output}" + "\n\n")
                results[i - start][j] = 4

            if results[i - start][j] == 1:
                number = 5
            elif results[i - start][j] == 3 or results[i - start][j] == 4:
                match = re.search(r"Passed (\d+)/", run_output)
                if match:
                    number = int(match.group(1))
                else:
                    number = 0
            else:
                number = 0

            data = json_data(task, i, j, results[i - start][j], number)
            json_results.append(data)

    data = json_data(task, "total", "total", results, 0)
    json_results.append(data)

    with open(results_path, "w") as file:
        json.dump(json_results, file, ensure_ascii=False, indent=4)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", default=1, type=int, help="Start index for test")
    parser.add_argument("--end", default=51, type=int, help="End index for test")
    parser.add_argument(
        "--template_path",
        default="/home/ubuntu/test_codellm/template/template.java",
        help="Path to the template file",
    )
    parser.add_argument(
        "--answer_json_path",
        default="/home/ubuntu/test_codellm/result/spark/python_java/prediction.json",
        help="Path to the answer file",
    )
    parser.add_argument(
        "--unit_tests_path",
        default="/home/ubuntu/test_codellm/unit_tests/spark/python_java/test.java",
        help="Path to the unit tests file",
    )
    parser.add_argument(
        "--results_path",
        default="/home/ubuntu/test_codellm/result/spark/python_java/results.json",
        help="Path to the results file",
    )
    parser.add_argument(
        "--json_file_path",
        default="/home/ubuntu/test_codellm/datas/datas.json",
        help="Path to the json file",
    )
    parser.add_argument(
        "--prediction_num", default=5, type=int, help="Number of predictions"
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)

    except_ = []

    results = run_tests(
        start=args.start,
        end=args.end,
        except_=except_,
        template_path=args.template_path,
        answer_json_path=args.answer_json_path,
        unit_tests_path=args.unit_tests_path,
        results_path=args.results_path,
        json_file_path=args.json_file_path,
        prediction_num=args.prediction_num,
        logger=logger,
    )

    logger.info(results)

    # python3 run_all_java_json.py --start 1 --end 50 --template_path /home/ubuntu/test_codellm/template/template.java --answer_json_path /home/ubuntu/test_codellm/result/spark/python_java/prediction.json --unit_tests_path /home/ubuntu/test_codellm/unit_tests/spark/python_java/test.java --results_path /home/ubuntu/test_codellm/result/spark/python_java/results.json --json_file_path /home/ubuntu/test_codellm/datas/datas.json --prediction_num 5 --log_dir /home/ubuntu/test_codellm/logs/spark/python_java
