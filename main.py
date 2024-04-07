from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found.")
openai_client = openai.OpenAI(api_key=openai_api_key)

# Endpoint for chatting with OpenAI
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('input')
    conversation_history = data.get('history', [])
    
    response_message, updated_history = get_openai_response(openai_client, user_input, conversation_history)
    
    return jsonify({'response': response_message, 'history': updated_history})

# Function to get response from OpenAI
def get_openai_response(client, user_input, conversation_history):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",  # Correct model name
            messages=conversation_history + [{"role": "user", "content": user_input}]
        )
        response_message = chat_completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": response_message})
    except Exception as e:
        print(f"Error while fetching response from OpenAI: {e}")
        response_message = "Sorry, I couldn't fetch a response. Please try again."
    
    return response_message, conversation_history

# Run the Flask app
if __name__ == "__main__":
    app.run(port=9090)
