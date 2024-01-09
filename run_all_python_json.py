import os
import subprocess
import json
import logging
import re
from utils.gen_test_python import insert_test_code, insert_code_str


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
    prediction_num,
    logger,
):
    results = [[0] * prediction_num for _ in range(end - start)]
    json_results = []

    answer_json = load_json(answer_json_path)

    task = answer_json[0]["task"]

    for i in range(start, end):
        if i in except_:
            continue

        for j in range(prediction_num):
            task_id = str(i) + "_" + str(j)
            index = (i - 1) * prediction_num + j

            logger.info(f"Index: {index}...")
            answer = answer_json[index]["pro_prediction"]
            main_fun_name = answer_json[index]["main_fun_name"]

            insert_code_str(
                answer, template_path, unit_tests_path, main_fun_name
            )
            insert_test_code(unit_tests_path, unit_tests_path, i)

            logger.info(f"Running task: {task_id}...")
            try:
                run_output = subprocess.check_output(
                    ["python3", unit_tests_path], stderr=subprocess.STDOUT, timeout=60
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
            elif run_output.find("SyntaxError") != -1:
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


def count_passed_questions(answers):
    """
    Counts the number of questions that are passed.
    A question is considered passed if there is at least one '1' in its answer list.
    """
    passed_count = 0
    for answer in answers:
        if 1 in answer:
            passed_count += 1
    return passed_count


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--start", default=1, type=int, help="Start index for test")
    parser.add_argument("--end", default=50, type=int, help="End index for test")
    parser.add_argument(
        "--template_path",
        default="template\\template.py",
        help="Path to the template file",
    )
    parser.add_argument(
        "--answer_json_path",
        default="result\\spark\\java_python\\prediction.json",
        help="Path to the answer file",
    )
    parser.add_argument(
        "--unit_tests_path",
        default="unit_tests\\spark\\java_python\\test.py",
        help="Path to the unit tests file",
    )
    parser.add_argument(
        "--results_path",
        default="result\\spark\\java_python\\results.json",
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
        prediction_num=args.prediction_num,
        logger=logger,
    )

    logger.info(results)
    # pass_ = count_passed_questions(results)
    # pass_rate = pass_ / (end - start - 4)
    # logger.info(f"Passed_Rate: {pass_rate}")
