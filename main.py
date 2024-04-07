import os
import openai

# Function to initialize OpenAI client
def initialize_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not found.")
    return openai.OpenAI(api_key=openai_api_key)

# Function to get response from OpenAI based on user input
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

# Main function to drive the chat
def main():
    client = initialize_openai_client()
    conversation_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Exiting the chat.")
            break
        response, conversation_history = get_openai_response(client, user_input, conversation_history)
        print(f"AI: {response}")

if __name__ == "__main__":
    main()
