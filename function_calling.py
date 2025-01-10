from typing import Optional, List, Dict
from param_types import WeightHeightParams, AnomalyParams
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import os
import requests

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def create_base_prompt(question: str, history: List[Dict], instructions: list[str]) -> str:
    prompt = f"Question: {question}\n\n"
    prompt += "Below are the history provided by the user.\n"
    
    # Convert history list to formatted string
    history_str = "\n".join([
        f"{entry['role']}: {entry['content']}"
        for entry in history
    ])
    prompt += f"{history_str}\n\n"
    
    prompt += "\nAnalyze the provided history and answer the question based on the following guidelines:\n"
    for i, instruction in enumerate(instructions, 1):
        prompt += f"{i}. {instruction}\n"
    return prompt

def answer_question(prompt):
    chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o-mini",
            max_tokens=500,  
            temperature=0.1, 
        )
    output = chat_completion.choices[0].message.content
    return output

class FunctionCalling:
    @staticmethod
    def ask_about_person_organize(question, history) -> str:
        # Phân tích và tổ chức thông tin về người được nhắc đến trong cuộc trò chuyện
        instructions = [
            "Extract and organize relevant information about people mentioned in the history",
            "Focus on relationships, events, and interactions between individuals",
            "If multiple instances of the same person are mentioned, consolidate the information",
            "Provide a clear, structured response that directly addresses the question",
            "If the information is not available in the history, clearly state it",
            "Do not make assumptions beyond what is explicitly stated in the history"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def normal_talk_irrelevant_to_parenting(question, history) -> None:
        # Xử lý các cuộc trò chuyện thông thường không liên quan đến việc nuôi dạy con
        instructions = [
            "Keep the conversation casual and friendly",
            "Focus on general topics unrelated to parenting",
            "Maintain appropriate boundaries and avoid sensitive topics",
            "Respond naturally to social cues in the conversation",
            "Stay within general knowledge and common experiences"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def check_childs_weight_height_with_age(params: WeightHeightParams, question, history) -> None:
        # Kiểm tra và đánh giá chiều cao, cân nặng của trẻ theo độ tuổi
        param_instructions = [
            f"Child's Information:",
            f"- Gender: {params['gender'] if params['gender'] else 'Not specified'}",
            f"- Age: {params['years_old']} years, {params['months_old']} months",
            f"- Height: {params['height'] if params['height'] else 'Not provided'} cm",
            f"- Weight: {params['weight'] if params['weight'] else 'Not provided'} kg"
        ]
        
        instructions = [
            *param_instructions,  # Add params at the beginning of instructions
            "Compare measurements with standard growth charts",
            "Consider age and gender-specific percentiles",
            "Note any significant deviations from expected ranges",
            "Provide context for the measurements in a reassuring way",
            "Recommend professional consultation if measurements are concerning",
            "Include age-appropriate developmental expectations"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def detect_anomaly_milestone_growth_by_age(params: AnomalyParams, question, history) -> None:
        # Phát hiện các bất thường trong sự phát triển của trẻ theo từng mốc tuổi
        param_instructions = [
            f"Anomaly Category: {params['anomaly_category']}"
        ]
        
        instructions = [
            *param_instructions,  # Add params at the beginning of instructions
            "Analyze developmental milestones for the given age",
            "Compare reported behaviors with expected milestones",
            "Identify any potential developmental concerns",
            "Consider individual variation in development",
            "Suggest age-appropriate activities for development",
            "Recommend professional evaluation when necessary"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def children_games(question, history) -> None:
        # Đề xuất các trò chơi phù hợp với độ tuổi của trẻ
        instructions = [
            "Focus on age-appropriate game suggestions",
            "Consider safety aspects of recommended games",
            "Include both indoor and outdoor activity options",
            "Explain educational benefits where applicable",
            "Consider group size and required materials"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def get_parenting_tips(question, history) -> None:
        # Cung cấp các lời khuyên về nuôi dạy con cái
        instructions = [
            "Provide evidence-based parenting advice",
            "Consider the child's age and developmental stage",
            "Include practical, actionable suggestions",
            "Address specific parenting challenges mentioned",
            "Emphasize positive parenting approaches",
            "Suggest resources for additional information"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def general_parenting_questions(question, history) -> None:
        # Trả lời các câu hỏi chung về nuôi dạy con
        instructions = [
            "Address common parenting concerns comprehensively",
            "Provide balanced and practical advice",
            "Include both short-term and long-term perspectives",
            "Consider family dynamics and circumstances",
            "Offer multiple approaches when appropriate",
            "Emphasize child development principles"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    # def get_current_date_time(question, history) -> None:
    #     # Lấy thông tin về ngày giờ hiện tại
    #     instructions = [
    #         "Provide accurate current date and time information",
    #         "Consider timezone context if mentioned",
    #         "Format the response clearly and consistently",
    #         "Include relevant temporal context if needed",
    #         "Address any time-related queries in the question"
    #     ]
    #     prompt = create_base_prompt(question, history, instructions)
    #     return answer_question(prompt)
    def get_current_date_time(question, history) -> str:
        try:
            response = requests.get("https://timeapi.io/api/Time/current/zone?timeZone=Asia/Ho_Chi_Minh")
            if response.status_code == 200:
                data = response.json()
                return {
                    "time": data["time"],
                    "date": data["date"],
                    "dayOfWeek": data["dayOfWeek"]
                }
            else:
                return "Failed to fetch time from API"
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    def history_question(question, history) -> None:
        # Trả lời các câu hỏi liên quan đến lịch sử cuộc trò chuyện
        instructions = [
            "Analyze historical information provided in the context",
            "Focus on relevant historical details and timeline",
            "Connect historical events to the current question",
            "Maintain accuracy in historical references",
            "Provide context for historical information",
            "Clarify any ambiguities in historical records"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def toxic_violence(question, history) -> None:
        # Xử lý các nội dung liên quan đến bạo lực hoặc độc hại
        instructions = [
            "Identify concerning behaviors or situations",
            "Maintain a professional and calm tone",
            "Provide appropriate safety resources and guidance",
            "Emphasize the importance of seeking professional help",
            "Address immediate safety concerns",
            "Avoid triggering or sensational language"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt)

    @staticmethod
    def sensitive_politic(question, history) -> None:
        # Xử lý các chủ đề nhạy cảm về chính trị
        instructions = [
            "Maintain neutral and balanced perspective",
            "Focus on factual information",
            "Avoid partisan or inflammatory language",
            "Acknowledge multiple viewpoints respectfully",
            "Direct to authoritative sources when appropriate",
            "Keep responses informative but measured"
        ]
        prompt = create_base_prompt(question, history, instructions)
        return answer_question(prompt) 



        