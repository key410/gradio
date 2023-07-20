import openai
import gradio as gr
import secret_keys

# OpenAIで発効したトークンを設定
openai.api_key = secret_keys.openai_api_key

def gpt_connect(prompt):
    # GPTに直接APIを送っている部分
    comp = openai.ChatCompletion.create(
        # 処理モデルを指定
        model = "gpt-3.5-turbo",
        messages = [
            {"role" : "user", "content" : prompt}
        ]
    )
    message = comp.choices[0].message.content
    return message.strip()

def chatbot(input, history=[]):
    # 入力音声をWhisperで文字に変換
    audiofile = open(input, "rb")
    conversion = openai.Audio.transcribe("whisper-1", audiofile)
    
    # 音声から変換した文字列をGPTへ送信
    output = gpt_connect(conversion["text"])
    history.append((conversion["text"], output))
    return history, history

if __name__ == "__main__":
    gr.Interface(fn = chatbot,
                 inputs = [gr.Audio(source = "microphone", type = "filepath"), "state"],
                 outputs = ["chatbot", "state"]).launch(debug=True)
