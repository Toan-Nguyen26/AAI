import gradio as gr
import time
import torch
import json
from huggingface_hub import InferenceClient

base_url_init="http://localhost:8007/v1/"

class JSONDetectModel:
    def __init__(self, base_url=base_url_init):
        try:
            print("Initializing JSON detection model")
            self.client = InferenceClient(
                            base_url=base_url,
                        )
            self.prompt_style = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response in JSON format that appropriately completes the request.

    ### Instruction:
    You are an intelligent assistant capable of understanding questions and providing structured responses in JSON format. Please analyze the user's question and provide a JSON response with fields for "observation" and "function" as described. 
    Just Return Json format, not anything else. Do not explain any thing.
    ### Input:
    Question: {}

    ### Response:
    """
            
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error initializing model: {e}")
            raise

    def generate_response(self, question):
        start_time = time.time()
        
        try:
            output = self.client.chat.completions.create(
                model="tgi",
                messages=[
                    {"role": "user", "content": self.prompt_style.format(question)},],
                max_tokens=128,
                temperature=0.1,
                stop=["}"],
            )
            response = output.choices[0].message["content"]
            inference_time = time.time() - start_time
           # Attempt to parse JSON
            try:
                parsed_json = json.loads(response)
                response = json.dumps(parsed_json, indent=2)
            except json.JSONDecodeError:
                response = "Error: Could not parse response as JSON"
            
            return response, f"{inference_time:.3f}"
                
        except Exception as e:
            return f"Error during generation: {str(e)}", "N/A"

def create_gradio_interface():
    model_interface = JSONDetectModel()
    
    with gr.Blocks() as demo:
        gr.Markdown("# JSON Detection Model")
        
        with gr.Row():
            input_text = gr.Textbox(label="Question", lines=3)
        with gr.Row():
            with gr.Column(scale=4):
                output_text = gr.Textbox(label="JSON Response", lines=10)
            with gr.Column(scale=1):
                inference_time = gr.Textbox(label="Inference Time (seconds)", lines=1)
        
        generate_button = gr.Button("Generate JSON Response")
        generate_button.click(
            model_interface.generate_response,
            inputs=input_text,
            outputs=[output_text, inference_time]
        )

    return demo

if __name__ == "__main__":
    demo = create_gradio_interface()
    
    print("Launching Gradio interface...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7864,
        share=True,
    )