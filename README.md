# gradioサンプル
- gradioとOpenAI API、及びVOICE VOXを使用したチャットボットサンプルになります。
gradio及びOpenAIのライブラリについては事前に取得して使用できる状態としてください。
```
pip install gradio
pip install openai
```

- VOICE VOXについてはPythonからVOICE VOXエンジンを叩く形になるため、
Pythonプログラムを実行する前に以下より取得したVOICE VOXエンジン事前に起動してください。

  - https://github.com/VOICEVOX/voicevox_engine
- OpenAIのAPIを使用するには事前にOpenAIへの登録を行い、個々に発行されるAPIキーが必要となります。
当ページではAPIキー作成方法までは記載しませんが、発効したAPIキーについてはsecret_keys.pyに記載することでPythonプログラム上で使用しています。
