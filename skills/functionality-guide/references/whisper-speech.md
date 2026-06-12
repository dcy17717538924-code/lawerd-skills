# 语音识别 (whisper)

## 能力

`openai-whisper` 本地语音转文字，`medium` 模型，中文识别效果好，无需联网。

## 调用路径

```
Python: {{CODEX_PYTHON}}
模型:   {{HOME_WIN}}\.cache\whisper\medium.pt (1.53 GB)
包:     openai-whisper==20250625
```

## 使用

```python
import whisper
model = whisper.load_model("medium")
result = model.transcribe("音频文件.mp3")
print(result["text"])
```

## 注意

- 模型全局共享，首次加载需数秒
- 长音频建议先切片再逐段转写
- 仅此一个 Python 环境可用
