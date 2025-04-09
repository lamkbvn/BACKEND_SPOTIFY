from pydub import AudioSegment
import librosa
import speech_recognition as sr
import numpy as np


# Chuyển đổi file MP3 thành WAV
audio = AudioSegment.from_mp3("file_audio.mp3")
audio.export("file_audio.wav", format="wav")
# Đọc file WAV
y, sr = librosa.load("file_audio.wav", sr=None)

# Tính tổng thời gian của file âm thanh
duration = librosa.get_duration(y=y, sr=sr)

# Chia nhỏ âm thanh theo mỗi 500 mili giây (0.5 giây)
timestamps = np.arange(0, duration, 0.5)  # Mỗi đoạn dài 500 mili giây

# Lấy các đoạn âm thanh
segments = [y[int(t * sr):int((t + 0.5) * sr)] for t in timestamps]

recognizer = sr.Recognizer()

# Mở file để ghi kết quả
with open("lyrics_times.txt", "w") as file:
    for i, segment in enumerate(segments):
        # Lưu đoạn âm thanh ra file tạm thời
        librosa.output.write_wav(f"segment_{i}.wav", segment, sr)

        # Đọc đoạn âm thanh
        with sr.AudioFile(f"segment_{i}.wav") as source:
            audio = recognizer.record(source)

        # Nhận diện lời bài hát
        try:
            text = recognizer.recognize_google(audio)
            # Ghi vào file kết quả thời gian và lời bài hát
            file.write(f"Thời gian {i * 0.5}s: {text}\n")
            print(f"Thời gian {i * 0.5}s: {text}")
        except sr.UnknownValueError:
            # Ghi vào file nếu không nhận diện được lời
            file.write(f"Thời gian {i * 0.5}s: Không nhận diện được lời\n")
            print(f"Thời gian {i * 0.5}s: Không nhận diện được lời")
