import openai
import gradio as gr
import secret_keys
import requests
import json
import pyaudio

# OpenAIで発効したトークンを設定
openai.api_key = secret_keys.openai_api_key

def vvox_test(text):
    # エンジン起動時に表示されているIP、portを指定
    host = "127.0.0.1"
    port = 50021
    
    # 音声化する文言と話者を指定(3で標準ずんだもんになる)
    params = (
        ('text', text),
        ('speaker', 3),
    )
    
    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params
    )
    
    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers = {"Content-Type": "application/json"},
        params = params,
        data = json.dumps(query.json())
    )
    
    # 再生処理
    voice = synthesis.content
    pya = pyaudio.PyAudio()
    
    # サンプリングレートが24000以外だとずんだもんが高音になったり低音になったりする
    stream = pya.open(format=pyaudio.paInt16,
                      channels=1,
                      rate=24000,
                      output=True)
    
    stream.write(voice)
    stream.stop_stream()
    stream.close()
    pya.terminate()

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
    
    # 入力を履歴へ追加
    history.append({
        "role" : "user", "content" : conversion["text"]
    })
    
    # 音声から変換した文字列をGPTへ送信
    output = gpt_connect(conversion["text"])
    history.append({
        "role" : "assistant", "content" : output
    })
    vvox_test(output)
    return [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]
    
with gr.Blocks() as demo:
    chat = gr.Chatbot()
    msg = gr.Audio(source = "microphone", type = "filepath")
    btn = gr.Button("submit")
    btn.click(fn=chatbot, inputs=msg, outputs=chat)
    clear = gr.ClearButton(components=msg, value="clear")
    
if __name__ == "__main__":
    demo.launch(debug=True)
