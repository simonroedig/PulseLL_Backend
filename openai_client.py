from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

class OpenAIClient:
    def __init__(self, model="gpt-3.5-turbo-1106", max_response_tokens=1000, temperature=0.7, top_p=0.8):
        load_dotenv() 
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=api_key)

        self.model = model
        self.max_response_tokens = max_response_tokens
        self.temperature = temperature
        self.top_p = top_p

    async def get_completion(self, system_message, user_message):
        completion = await self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_response_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return completion

    def print_response_info(self, completion):
        finish_reason = completion.choices[0].finish_reason
        model = completion.model
        completion_tokens = completion.usage.completion_tokens
        prompt_tokens = completion.usage.prompt_tokens
        total_tokens = completion.usage.total_tokens
        
        content = completion.choices[0].message.content
        
        print("Request Information:\n")
        print(f"Finish Reason: {finish_reason}")
        print(f"Model: {model}")
        print(f"Response Tokens: {completion_tokens}")
        print(f"Prompt Tokens: {prompt_tokens}")
        print(f"Total Tokens: {total_tokens}")
        print(f"\nResponse: \n\n{content}")
