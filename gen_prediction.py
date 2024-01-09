import os
import json
import argparse
import logging
from utils.extract_code import extract_code
from models import call_llm


def prepare_prompt(sl, tl, sc, params):
    with open("/home/ubuntu/test_codellm/prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read().strip()

    prompt = prompt.replace("SL", sl).replace("TL", tl).replace("SC", sc).replace("PARAMS", params)

    return prompt


def save_json(
    task,
    problem_id,
    prediciton_id,
    pro_prediction,
    main_fun_name,
    raw_prediction,
    sl_gold_code,
    tl_gold_code,
):
    data = {
        "task": task,
        "problem_id": problem_id,
        "prediction_id": prediciton_id,
        "pro_prediction": pro_prediction,
        "main_fun_name": main_fun_name,
        "raw_prediction": raw_prediction,
        "sl_gold_code": sl_gold_code,
        "tl_gold_code": tl_gold_code,
    }

    return data


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return content


def load_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file:
        datas = json.load(file)

    return datas


def main(
    start,
    end,
    except_,
    model_name,
    sl,
    tl,
    prediction_base_path,
    json_path,
    jsonl_path,
    answer_base_path,
    prediction_nums,
    datas_path,
):
    """
    Generate predictions for a given range of tasks.

    Args:
        start (int): The starting task ID.
        end (int): The ending task ID.
        except_ (list): A list of task IDs to exclude.
        model_name (str): The name of the model to use for prediction.
        sl (str): The source language.
        tl (str): The target language.
        prediction_base_path (str): The base path for saving prediction files.
        json_path (str): The path to save the predictions in JSON format.
        jsonl_path (str): The path to save the predictions in JSONL format.
        answer_base_path (str): The base path for reading gold answer files.
        prediction_nums (int): The number of predictions to generate for each task.
        datas_path (str): The path to the data file.

    Returns:
        None
    """
    task = sl + "_" + tl
    model = call_llm(model_name)
    json_datas = []

    datas = load_json(datas_path)

    for i in range(start, end):
        if i in except_:
            continue

        # Reason: Because the c++ file in gold_answer is named `c`, a conversion is required
        sl_ = sl
        tl_ = tl
        if sl == "c++":
            sl_ = "c"
        if tl == "c++":
            tl_ = "c"

        sl_gold_code = read_file(answer_base_path + str(i) + "/" + f"{sl_}")
        params = str(datas[i - 1]["params"][tl])
        prompt = prepare_prompt(sl, tl, sl_gold_code, params)
        # print(prompt)

        tl_gold_code = read_file(answer_base_path + str(i) + "/" + f"{tl_}")

        for j in range(prediction_nums):
            raw_prediction = model.chat(prompt, temperature=0.1)
            prediction, main_fun_name = extract_code(
                raw_prediction,
                tl,
                datas[i - 1]["entry_point"],
            )
            result = prediction if prediction != "" else raw_prediction
            # print(f"raw_prediction: {raw_prediction}\n")
            # print(f"result: {result}")

            json_data = save_json(
                task,
                i,
                j,
                result,
                main_fun_name,
                raw_prediction,
                sl_gold_code,
                tl_gold_code,
            )
            json_datas.append(json_data)

            print("Task_id: " + str(i) + "_" + str(j) + "    done")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_datas, f, ensure_ascii=False, indent=4)

    lines = [json.dumps(x, ensure_ascii=False) for x in json_datas]
    with open(jsonl_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start", type=int, default=97, help="Start index of the test tasks"
    )
    parser.add_argument(
        "--end", type=int, default=98, help="End index of the test tasks"
    )
    parser.add_argument(
        "--model_name", type=str, default="chatglm3", help="Name of the model"
    )
    parser.add_argument(
        "--sl", type=str, default="python", help="Source program language"
    )
    parser.add_argument(
        "--tl", type=str, default="c++", help="Target program language"
    )
    parser.add_argument(
        "--prediction_base_path",
        type=str,
        default="/home/ubuntu/test_codellm/result/spark/java_python",
        help="Base path for predictions to be stored if storage for each file is necessary",
    )
    parser.add_argument(
        "--json_path",
        type=str,
        default="/home/ubuntu/test_codellm/result/spark/java_python/prediction.json",
        help="Path to the result JSON file",
    )
    parser.add_argument(
        "--jsonl_path",
        type=str,
        default="/home/ubuntu/test_codellm/result/spark/java_python/prediction.jsonl",
        help="Path to the result JSONL file",
    )
    parser.add_argument(
        "--answer_base_path",
        type=str,
        default="/home/ubuntu/test_codellm/datas/gold_answer/",
        help="Base path for gold answers",
    )
    parser.add_argument(
        "--prediction_nums",
        type=int,
        default=1,
        help="Number of predictions to be generated for each question",
    )
    parser.add_argument(
        "--datas_path",
        type=str,
        default="/home/ubuntu/test_codellm/datas/datas.json",
        help="datas_json path",
    )

    args = parser.parse_args()

    if not os.path.exists(args.prediction_base_path):
        os.makedirs(args.prediction_base_path, exist_ok=True)

    except_ = []

    main(
        start=args.start,
        end=args.end,
        except_=except_,
        model_name=args.model_name,
        sl=args.sl,
        tl=args.tl,
        prediction_base_path=args.prediction_base_path,
        json_path=args.json_path,
        jsonl_path=args.jsonl_path,
        answer_base_path=args.answer_base_path,
        prediction_nums=args.prediction_nums,
        datas_path=args.datas_path,
    )