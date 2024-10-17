from flask import Flask, render_template_string, request
from diffusers import DiffusionPipeline
import torch
import os

app = Flask(__name__)

# 定义16种MBTI类型
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 初始化DiffusionPipeline
model = "runwayml/stable-diffusion-v1-5"
pipe = DiffusionPipeline.from_pretrained(model, torch_dtype=torch.float32)
pipe.to("cpu")

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, mbti_types=MBTI_TYPES)

@app.route('/generate', methods=['POST'])
def generate():
    mbti_input = request.form.get('mbti')
    prompt = f"{mbti_input} character"
    
    # 生成图像
    images = pipe(prompt, num_inference_steps=20).images
    image_path = "generated_image.png"
    images[0].save(image_path)  # 保存生成的图像
    return image_path

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
        h1, h2 {
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
        .message {
            margin-top: 20px;
            font-size: 18px;
        }
        #generatedImage {
            margin-top: 20px;
            display: none; /* 初始隐藏 */
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti"></script>
</head>
<body>
    <h1>welcome to 16 Dwarf Kingdoms!</h1>
    <h2>enter password to find your Dwarf！</h2>
    <div class="input-container">
        <input type="text" class="input-box" maxlength="1" oninput="this.nextElementSibling.focus();">
        <input type="text" class="input-box" maxlength="1" oninput="this.nextElementSibling.focus();">
        <input type="text" class="input-box" maxlength="1" oninput="this.nextElementSibling.focus();">
        <input type="text" class="input-box" maxlength="1">
    </div>
    <button class="button" onclick="validatePassword()">确认</button>
    <div class="message" id="message"></div>

    <div id="characterPrompt" style="display:none;">
        <h3>输入关键词，找到你的小矮人：</h3>
        <button class="button" onclick="generateImage()">生成图像</button>
    </div>
    
    <img id="generatedImage" src="" alt="生成的图像">

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
            const messageElement = document.getElementById('message');
            if (mbtiTypes.includes(upperCasePassword)) {
                messageElement.innerText = '密码正确，欢迎进入！';
                messageElement.style.color = 'green';
                confetti({
                    particleCount: 100,
                    spread: 70,
                    origin: { y: 0.6 }
                });
                currentMBTI = upperCasePassword; // 保存当前输入的MBTI
                document.getElementById('characterPrompt').style.display = 'block'; // 显示输入关键词的按钮
            } else {
                messageElement.innerText = '密码错误，尝试输入你的mbti？';
                messageElement.style.color = 'red';
            }
        }

        function generateImage() {
            const formData = new FormData();
            formData.append('mbti', currentMBTI);
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(imagePath => {
                const generatedImage = document.getElementById('generatedImage');
                generatedImage.src = imagePath; // 设置生成的图像路径
                generatedImage.style.display = 'block'; // 显示生成的图像
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)