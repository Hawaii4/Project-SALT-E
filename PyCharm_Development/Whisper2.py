import whisper

model = whisper.load_model("tiny")
result = model.transcribe(r"rec.wav")
print(result["text"])

#https://chatgpt.com/share/68ecf7d6-17f4-800f-b9ab-ef982afbbd40
