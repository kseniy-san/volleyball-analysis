import cv2
import os

input_video = "full_game.mp4"
output_video = "test_video.mp4"
duration_seconds = 60

# Проверяем, существует ли файл вообще
if not os.path.exists(input_video):
    print(f"ОШИБКА: Файл {input_video} не найден в папке {os.getcwd()}")
    exit()

cap = cv2.VideoCapture(input_video)

# Проверяем, смогла ли OpenCV открыть видео
if not cap.isOpened():
    print("ОШИБКА: OpenCV не может открыть видео. Возможно, проблема с кодеком.")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

frames_to_cut = int(fps * duration_seconds)
for i in range(frames_to_cut):
    ret, frame = cap.read()
    if not ret:
        print(f"Видео закончилось на кадре {i}")
        break
    out.write(frame)

cap.release()
out.release()
print(f"УСПЕХ! Вырезано {duration_seconds} секунд в файл {output_video}")