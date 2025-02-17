import openai

# Set your API key here. Make sure to replace 'your-api-key' with your actual OpenAI API key.
openai.api_key = 'your-api-key'

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",  # Use the latest available model
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    prompt = "Enter your prompt here"
    response = generate_response(prompt)
    print("Response:", response)
