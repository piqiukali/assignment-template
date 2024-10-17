import gradio as gr

def validate_code(*args):
  return f"验证码是:{''.join(args)}"

with gr.Blocks(style={'css':".code-box {
  width: 60px;
  height: 60px;
  font-size: 48px; 
  display: inline-block;
  margin: 10px;
  border: 2px solid #ccc;
  border-radius: 10px;
  //....
}"}) as demo:

  gr.Markdown("<div style='font-size: 36px;'>请输入验证码</div>")

  with gr.Row():
    inp1 = gr.Textbox(placeholder="", max_length=1, elem_id="box1", label="", 
                      interactive=True, class_name="code-box")
    inp2 = gr.Textbox(placeholder="", max_length=1, elem_id="box2", label="",  
                      interactive=True, class_name="code-box") 
    inp3 = gr.Textbox(placeholder="", max_length=1, elem_id="box3", label="",
                      interactive=True, class_name="code-box")
    inp4 = gr.Textbox(placeholder="", max_length=1, elem_id="box4", label="",  
                      interactive=True, class_name="code-box")

  submit_btn = gr.Button("确定")

  submit_btn.click(validate_code, inputs=[inp1, inp2, inp3, inp4], 
                   outputs=gr.Textbox(label="结果"))

if __name__ == "__main__":
  demo.launch(share=True)