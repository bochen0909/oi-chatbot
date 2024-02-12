import json
import gradio as gr
from oi_chatbot.utils import apply_profile
from interpreter import interpreter
from oi_chatbot import config
import os
import time
from oi_chatbot.config import OI_CHATBOT_HOME

apply_profile(interpreter, config.default_profile)

interpreter.auto_run = True


def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)


def update_bot(history):
    response = interpreter.chat(history[-1][0])
    response = json_to_markdown(response)
    if 0:
        history[-1][1] = ""
        for character in response:
            history[-1][1] += character
            time.sleep(0.02)
            yield history
    else:
        history[-1] = (history[-1][0], response)
        yield history


def save_history(history):
    print(history)


def new_chat(history):
    if history:
        yymmdd = time.strftime("%Y%m%d", time.localtime())
        first_chat = history[0][0]
        filename = f"{yymmdd}_{''.join(c for c in first_chat if c.isalnum() or c in ['-', '_', '.', ' '])}.json"
        filepath = os.path.join(OI_CHATBOT_HOME, filename)
        obj = {'history': history, 'interpreter_message': interpreter.messages}
        with open(filepath, 'w') as f:
            f.write(json.dumps(obj, indent=4))

    interpreter.messages = []
    return []


def create_chat_widget():
    with gr.Blocks() as chatblock:
        with gr.Row():

            dropdown_llms = gr.Dropdown(
                choices=list(config.profiles.keys()),
                label="Select an LLM:",
                value=config.current_profile_name,
                scale=3,
                interactive=True,
            )

            def on_profile_change(selected_profile):
                print("Changing profile to", selected_profile)
                previous_profile_name = config.current_profile_name
                config.current_profile_name = selected_profile
                config.current_profile = config.profiles[selected_profile]
                apply_profile(interpreter, config.current_profile)
                gr.Info(
                    f"Switched profile from `{previous_profile_name}` to `{selected_profile}`")

            dropdown_llms.change(on_profile_change, [dropdown_llms], [])

        chatbot = gr.Chatbot(
            [],
            elem_id="chatbot",
            elem_classes="chatbot",
            layout="bubble",
            bubble_full_width=False,
            height=600,
            avatar_images=(
                None, (os.path.join(os.path.dirname(__file__), "avatar.jpeg"))),
        )
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter to chat with the bot.",
            container=False,
        )
        new_chat_button = gr.Button(
            "New Chat",
            scale=3,
            interactive=True,
        )
        new_chat_button.click(new_chat, [chatbot], [chatbot]).then(
            lambda: gr.Textbox(interactive=True), None, [txt], queue=False
        )

        txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
            update_bot, chatbot, chatbot, api_name="bot_response"
        ).then(save_history, chatbot, None).then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)

        return chatblock


def json_to_markdown(json_data):
    markdown_string = ""

    for item in json_data:
        if item['role'] == 'user':
            continue
        if item['type'] == 'message':
            markdown_string += f"**{item['role'].capitalize()}:** \n{item['content']}\n\n"
        elif item['type'] == 'code':
            markdown_string += f"```{item['format']}\n{item['content']}\n```\n\n"
        elif item['type'] == 'console':
            markdown_string += f"```\n{item['content']}\n```\n\n"

    return markdown_string


def chat(message, history, system_prompt):
    response = interpreter.chat(message)
    return json_to_markdown(response)


with gr.Blocks() as demo:
    with gr.Tab("Open Interpreter Chat"):
        chat_interface = create_chat_widget()
demo.launch()
