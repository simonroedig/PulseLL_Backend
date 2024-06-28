import asyncio
from openai_client import OpenAIClient

async def main():
    # test commit
    openai = OpenAIClient()
    system_message = "Answer short and precise."
    user_message = "give me 10 random words."
    
    completion = await openai.get_completion(system_message, user_message)
    openai.print_response_info(completion)

if __name__ == "__main__":
    asyncio.run(main())