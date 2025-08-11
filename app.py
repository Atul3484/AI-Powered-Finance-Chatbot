from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

#  Configure API key
genai.configure(api_key="AIzaSyDfRNhDUnZOlPYJWOiWl_m08kaK2qpoOKM")  # Don't expose your key publicly

#  model name
model = genai.GenerativeModel("models/gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sip')
def sip():
    return render_template('sip.html')


@app.route('/chat', methods=['POST'])
def chat_with_bot():
    user_message = request.json.get('message')
    try:
        response = model.generate_content(user_message)
        # Try to extract the text from the Gemini response object
        try:
            reply = response.text
        except AttributeError:
            # Fallback for Gemini's actual response structure
            reply = response.candidates[0].content.parts[0].text if hasattr(response, 'candidates') else str(response)
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)


