from flask import Flask, render_template_string, request
from diffusers import DiffusionPipeline
import torch

app = Flask(__name__)

# How to get in
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# Initialize DiffusionPipeline
model = "runwayml/stable-diffusion-v1-5"
pipe = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float32)
pipe.to("cuda")

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, mbti_types=MBTI_TYPES)

@app.route('/generate', methods=['POST'])
def generate():
    mbti_input = request.form.get('mbti')
    prompt = request.form.get('prompt')
    full_prompt = f"{prompt} {mbti_input} character"
    
    # Generate image (the generated image will be appear after finishing the generate)
    images = pipe(full_prompt, num_inference_steps=20).images
    image_path = "generated_image.png"
    images[0].save(image_path)  # Save the generated image
    images[0].show()            # Show the generated image
    return "Image generated successfully" 

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Input</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            text-align: center;
        }
        .input-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        .input-box {
            width: 40px;
            height: 40px;
            margin: 0 5px;
            text-align: center;
            font-size: 24px;
            border: 2px solid #ccc;
            border-radius: 5px;
        }
        .button-container {
            display: flex;
            justify-content: center; /* Center the button */
            margin-top: 20px;
        }
        .button {
            padding: 15px 30px;
            font-size: 18px;
            cursor: pointer;
            background-color: blue;
            color: white;
            border: none;
            border-radius: 15px;
            transition: background-color 0.3s;
        }
        .button:hover {
            background-color: darkblue;
        }
        #dwarfMessage {
            display: none; /* Initially hidden */
            font-size: 24px;
            color: green;
            margin-top: 20px;
        }
        #goFindMessage { 
            display: none; /* Initially hidden */
            font-size: 24px;
            color: orange;
            margin-top: 20px;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti"></script>
</head>
<body>
    <div id="titleSection">
        <h1 id="mainTitle">Enter the password to enter the program</h1>
    </div>
    <div id="passwordSection">
        <div class="input-container">
            <input type="text" class="input-box" maxlength="1" oninput="this.nextElementSibling?.focus();">
            <input type="text" class="input-box" maxlength="1" oninput="this.nextElementSibling?.focus();">
            <input type="text" class="input-box" maxlength="1" oninput="this.nextElementSibling?.focus();">
            <input type="text" class="input-box" maxlength="1">
        </div>
        <div class="button-container">
            <button class="button" onclick="validatePassword()">OK</button>
        </div>
    </div>
    <div id="promptSection" style="display:none;">
        <h3>Enter keywords to have your own mbti character：</h3>
        <input type="text" id="promptInput" placeholder="Enter keywords">
        <button class="button" onclick="generateImage()">GO!</button>
    </div>
    <div id="dwarfMessage">Go find your mbti character!!</div>
    
    <script>
        let currentMBTI = '';

        function validatePassword() {
            const inputs = document.querySelectorAll('.input-box');
            let password = '';
            inputs.forEach(input => {
                password += input.value;
            });
            const upperCasePassword = password.toUpperCase();
            const mbtiTypes = {{ mbti_types|tojson }};
            if (mbtiTypes.includes(upperCasePassword)) {
                document.getElementById('mainTitle').innerText = 'Welcome. You did it!'; // Update title
                document.getElementById('passwordSection').style.display = 'none'; // Hide password input and confirm button
                currentMBTI = upperCasePassword; // Save the current MBTI input
                document.getElementById('promptSection').style.display = 'block'; // Show keyword input box

                // Add confetti effect
                confetti({
                  particleCount: 100,
                  spread: 70,
                  origin: { y: 0.6 }
                });

            } else {
                alert('Come on!?!(╯▔皿▔)╯ Try entering your mbti.'); // Prompt user for incorrect input
                
                // Clear input box contents
                inputs.forEach(input => {
                    input.value = '';
                });
                inputs[0].focus(); // Focus on the first input box
            }
        }

        function generateImage() {
            const prompt = document.getElementById('promptInput').value;
            const formData = new FormData();
            formData.append('mbti', currentMBTI);
            formData.append('prompt', prompt);
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(message => {
                // Do not display image, only show success message
                document.getElementById('goFindMessage').style.display = 'block';
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
