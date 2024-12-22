from libraries import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

context = "You are an AI assistant helping a user with their code."
app = Flask(__name__) 
def generate_code(prompt):
    try:
        logging.info("Generating code for prompt: %s", prompt)
        stream = client.chat.completions.create(
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-gs",
            stream=True,
        )
        response = ""
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                if content:
                    response += content
        logging.info("Code generation successful")
        return response
    except Exception as e:
        logging.error("Error generating code: %s", e, exc_info=True)
        return None

@app.route('/')
def index():
    return render_template('CodeGenUI.html')

@app.route('/generate_code', methods=['POST'])
def process_generate_code():
    try:
        data = request.json
        prompt = data.get('prompt', '').strip()
        if not prompt:
            return jsonify({"error": "Prompt is required."}), 400
        generated_code = generate_code(prompt)
        if generated_code:
            return jsonify({"code": generated_code})
        else:
            return jsonify({"error": "Failed to generate code."}), 500
    except Exception as e:
        logging.error("Error processing generate_code: %s", e, exc_info=True)
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True)
