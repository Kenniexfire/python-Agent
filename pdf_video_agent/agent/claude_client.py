import anthropic
import os

def generate_content(text):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"Generate a video script, title, description, and marketing copy from the following text:\n{text}"

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    print(response.content)