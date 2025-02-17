import openai
import os

# Set API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",  # Use the latest available model
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=1,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    prompt = "Enter your prompt here"
    response = generate_response(prompt)
    print("Response:", response)
