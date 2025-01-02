import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    DataCollatorForLanguageModeling,
)
from peft import (
    prepare_model_for_kbit_training,
    LoraConfig,
    get_peft_model,
)
from trl import SFTTrainer
from tqdm import tqdm
import time

# Cấu hình các tham số
max_seq_length = 256
model_name = "Qwen/Qwen2.5-0.5B"

# # Cấu hình lượng tử hóa 4-bit
# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=False,
#     bnb_4bit_use_double_quant=False,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_compute_dtype=torch.float16
# )

# Khởi tạo tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    padding_side="right",
    use_fast=False,
)
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': tokenizer.eos_token})

# Khởi tạo model với lượng tử hóa 4-bit
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    # quantization_config=bnb_config,
    device_map='auto'
    # token="hf_...",  # Thêm token nếu cần
)

# # Chuẩn bị model cho kbit training
# model = prepare_model_for_kbit_training(model)

# # Cấu hình LoRA
# lora_config = LoraConfig(
#     r=16,
#     lora_alpha=16,
#     target_modules=[
#         "q_proj",
#         "k_proj",
#     ],
#     lora_dropout=0.0,
#     bias="none",
#     task_type="CAUSAL_LM",
# )

# # Áp dụng LoRA
# model = get_peft_model(model, lora_config)

# Format prompt template
prompt_style = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response in JSON format that appropriately completes the request.

### Instruction:
You are an intelligent assistant capable of understanding questions and providing structured responses in JSON format. Please analyze the user's question and provide a JSON response with fields for "observation" and "function" as described.
Just return extract Json format, not anything else. Do not explain any thing.
### Input:
Question: {}

### Response:
{}

"""

# Hàm format dữ liệu
def formatting_prompts_func(examples):
    inputs = examples["Question"]
    outputs = examples["Result"]
    texts = []
    for input, output in zip(inputs, outputs):
        text = prompt_style.format(input, output) + tokenizer.eos_token
        texts.append(text)
    return {"text": texts}

# Load dataset
dataset = load_dataset(
    "csv", 
    data_files="/home/tinh/kawaii/parenting_llm/final_intensity_en.csv",
    split='train'
)
dataset = dataset.map(
    formatting_prompts_func,
    batched=True,
)
output_dir = "/home/tinh/kawaii/parenting_llm/models/outputs-son/new_intensity_qwen"

# Khởi tạo trainer
training_args = TrainingArguments(
    output_dir = output_dir,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=2,
    num_train_epochs=2,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    optim="paged_adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=3407,
    push_to_hub=False,
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    args=training_args,
)

# Training
trainer_stats = trainer.train()
