from function_calling import FunctionCalling
# from .param_types import WeightHeightParams, AnomalyParams
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
from datetime import datetime
import string
import time
from datetime import datetime
import random


def main():
    model = AutoModelForCausalLM.from_pretrained(
        "dohuyen/general-function-call",
        torch_dtype=torch.bfloat16,
        device_map="auto",
        offload_folder="offload_folder",
    )
    tokenizer = AutoTokenizer.from_pretrained("dohuyen/general-function-call")
    fc = FunctionCalling()
    
    # Initialize conversation history
    conversation_history = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        
        # Add user question to conversation
        conversation = get_conversation()
        conversation.append({
            "role": "user",
            "content": user_input
        })
        
        # Store in history
        conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Generate response
        response = generating_model_output(conversation, model, tokenizer)
        print("Assistant:", response)
        
        # Handle function calls in response
        if isinstance(response, list) and len(response) > 0:
            function_call = response[0]  # Get first function call
            if 'name' in function_call:
                function_name = function_call['name']
                function_args = function_call.get('arguments', {})
                try:
                    if hasattr(fc, function_name):
                        result = getattr(fc, function_name)(question=user_input, history=conversation_history)
                        print(f"Function Output: {result}")
                        response = result  # Use function output as response
                    else:
                        print(f"Function '{function_name}' not found.")
                except Exception as e:
                    print(f"Error invoking function '{function_name}': {e}")
        
        # Store response in history
        conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

tools_file = "intensity.json"

def load_json(file):
    with open(file, "r") as file:
        return json.load(file)

tools_list = load_json(tools_file)

new_tools = []
for sample in tools_list:
    new_tools.append({
        "type": "function",
        "function": sample
    })

def get_conversation():
    conversation = [{
        "role": "system",
        "content": f"""Today is {datetime.now().strftime('%d/%m/%Y')}. You are a chatbot that supports users in answering general questions.\nThere is a function to search for type of question.\nYou are given a user's query and you need to classify the function to get the desired output.\nThis is the question that the user have asked:"""
    }]
    return conversation

def generate_tool_call_id(length=9):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generating_model_output(conversation, model, tokenizer):
    inputs = tokenizer.apply_chat_template(
        conversation,
        tools=new_tools,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    )

    input_text = tokenizer.apply_chat_template(
        conversation,
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = {k: v.to(model.device) for k,v in inputs.items()}


    # Test with 1000 tokens
    generation_config = {
        "max_new_tokens": 1000,  
        "do_sample": True,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "num_beams": 1, 
    }
    start = time.time()
    print("Generating")
    output_1000 = model.generate(**inputs, **generation_config)
    print(f"Time for 1000 tokens: {time.time() - start:.2f} seconds")

    output_text = tokenizer.decode(output_1000[0])[len(input_text):].strip().replace('[TOOL_CALLS] ', "").replace('</s>', "").strip()
    output_text = output_text.split("[/INST]")[1]
    return load_output(output_text)

def load_output(response):
    try:
        response_dict = json.loads(response)
    except json.JSONDecodeError:
        try:
            response_dict = eval(response)
        except Exception as e:
            print(f"Failed to parse response with eval: {e}")
            response_dict = None
    return response_dict

if __name__ == "__main__":
    main()