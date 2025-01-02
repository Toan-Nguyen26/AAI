import os
import torch
from vllm import LLM, SamplingParams
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import ast
from sklearn.metrics import precision_score, recall_score, f1_score
from collections import defaultdict


def setup_vllm_model(model_path: str):

    # Check if the model exists locally
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path {model_path} does not exist.")

    # Initialize vLLM model with local directory
    llm = LLM(
        model=model_path,  # This should work if vLLM supports local paths
        trust_remote_code=True,
        dtype="float16", 
        gpu_memory_utilization=0.4,
        max_model_len=1024,
    )
    
    return llm

llm = setup_vllm_model('/home/tinh/kawaii/parenting_llm/models/outputs-son/new_intensity_qwen/checkpoint-182')

# Generate intensity
def model_generate(prompt: str, llm: LLM) -> str:
    # Sử dụng prompt_style để phù hợp với dạng prompt đã huấn luyện
    prompt_style = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response in JSON format that appropriately completes the request.

    ### Instruction:
    You are an intelligent assistant capable of understanding questions and providing structured responses in JSON format. Please analyze the user's question and provide a JSON response with fields for "observation" and "function" as described. 
    Just Return Json format, not anything else. Do not explain any thing.
    ### Input:
    Question: {}

    ### Response:
    """
    
    # Chuẩn bị prompt với câu hỏi của người dùng
    full_prompt = prompt_style.format(prompt, "{}")
    
    # Tham số sampling
    sampling_params = SamplingParams(
        temperature=0.3,      # Cân bằng giữa sáng tạo và nhất quán
        top_p=0.95,          # Cho phép nhiều lựa chọn token hơn
        top_k=50,            # Giữ nguyên vì đã tốt
        max_tokens=128,      # Tăng lên để đủ độ dài
        repetition_penalty=1.1, # Tránh lặp lại
        stop=[
            "</s>", "<|im_end|>", "<|endoftext|>", "<|eos|>", "\n", "<eos>", "<|im_start|>", "<|startoftext|>", "<|endofdoc|>", "<|sep|>"
        ],
    )

    # Sinh phản hồi từ mô hình
    outputs = llm.generate(full_prompt, sampling_params)
    response = outputs[0].outputs[0].text

    return response

def accuracy_test(df):
    total_questions = len(df)
    correct_answers = 0

    # Initialize metrics tracking
    true_labels = []
    predicted_labels = []
    
    # Dictionary to track errors for each case
    error_counts = {}
    case_predictions = {}  # To track what incorrect predictions were made for each case
    wrong_questions = {}  # To track wrong questions for each case

    start_time = time.time()

    for index, ques in tqdm(enumerate(df['Question']), total=total_questions, desc="Processing Questions"):
        expected_case = df['Case'][index]

        response_text = model_generate(ques, llm)
        response_text = response_text.strip()

        try:
            response = json.loads(response_text)
            function_name = response['function']['name']

            # Append true and predicted labels for overall metrics
            true_labels.append(expected_case)
            predicted_labels.append(function_name)

            if function_name == expected_case:
                correct_answers += 1
            else:
                # Track errors for each case
                if expected_case not in error_counts:
                    error_counts[expected_case] = 0
                    case_predictions[expected_case] = {}
                    wrong_questions[expected_case] = []

                error_counts[expected_case] += 1

                # Track what it was incorrectly predicted as
                if function_name not in case_predictions[expected_case]:
                    case_predictions[expected_case][function_name] = 0
                case_predictions[expected_case][function_name] += 1

                # Track the wrong question and its prediction
                wrong_questions[expected_case].append({
                    'question': ques,
                    'predicted': function_name
                })

        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e} for question: {ques}")

    # Calculate overall metrics
    accuracy = correct_answers / total_questions if total_questions > 0 else 0
    precision = precision_score(true_labels, predicted_labels, average='macro', zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average='macro', zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, average='macro', zero_division=0)

    print("\nOverall Results:")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1-Score: {f1:.2%}")

    print("\nError Analysis by Case:")
    print("----------------------")
    for case in sorted(error_counts.keys()):
        total_case_instances = len(df[df['Case'] == case])
        error_rate = error_counts[case] / total_case_instances if total_case_instances > 0 else 0
        print(f"\nCase: {case}")
        print(f"Total instances: {total_case_instances}")
        print(f"Number of errors: {error_counts[case]}")
        print(f"Error rate: {error_rate:.2%}")

        print("Incorrectly predicted as:")
        for pred_case, count in case_predictions[case].items():
            print(f"  - {pred_case}: {count} times")

        print("\nWrong questions for this case:")
        for item in wrong_questions[case]:
            print(f"  Question: {item['question']}")
            print(f"  Predicted as: {item['predicted']}")
            print("  ---")

    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTotal time taken: {total_time:.2f} seconds")

#Build data
df= pd.read_csv('/home/tinh/kawaii/parenting_llm/test_intensity.csv')

accuracy_test(df)