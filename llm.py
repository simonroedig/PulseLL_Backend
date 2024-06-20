"""
Using gpt-3.5-turbo-1106, because of better json output and reproducibility.
see: https://platform.openai.com/docs/models/gpt-3-5-turbo
"""
from openai import OpenAI, AsyncOpenAI
import asyncio

client = AsyncOpenAI()

gpt_model = "gpt-3.5-turbo-1106"
max_response_tokens = 100
model_temperature = 0.7
model_top_p = 1

system_message = "Answer short and precise."
user_message = "give me 10 random words."

async def main():
    completion = await client.chat.completions.create(
        model = gpt_model,
        max_tokens = max_response_tokens,      
        temperature = model_temperature,   
        top_p = model_top_p,    
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )

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

asyncio.run(main())