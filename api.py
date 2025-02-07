from flask import Flask, request, jsonify
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Replace with your actual API key
my_api_key = "AIzaSyAXII413W1cHh3tqlzlX8k34J3Ehrzcw9s"

# Configure the API key
genai.configure(api_key=my_api_key)

# Create the model generation configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction="You're a tourist guide, assisting users with tourist spots and nearby attractions in an interactive manner.",
)

# Initialize chat history storage
chat_sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id', 'default')  # Unique ID for each user
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    # Retrieve or create a chat session
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])

    chat_session = chat_sessions[user_id]

    # Get response from the model
    response = chat_session.send_message(user_input)
    model_response = response.text

    # Update the history
    chat_sessions[user_id].history.append({"role": "user", "parts": [user_input]})
    chat_sessions[user_id].history.append({"role": "model", "parts": [model_response]})

    return jsonify({"response": model_response})

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
