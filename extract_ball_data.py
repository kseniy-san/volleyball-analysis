import cv2
import json
from ultralytics import YOLO

# Загружаем модель
model = YOLO("yolo26s_players_ball.pt")
ball_class_id = 1  # мяч - это 1

# Получаем видео
cap = cv2.VideoCapture("test_video.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
cap.release()

print("Начинаем обработку. Пожалуйста, подождите...")

# Используем predict и stream=True
results_generator = model.predict(
    source="test_video.mp4",
    classes=[ball_class_id],
    conf=0.15,  # Низкий порог уверенности, чтобы ловить больше мячей
    stream=True,
    verbose=False
)

ball_data = []

for frame_id, result in enumerate(results_generator):
    if frame_id % 200 == 0:
        print(f"Обработано кадров: {frame_id}...")

    if result.boxes is not None and len(result.boxes) > 0:
        box = result.boxes.xyxy[0].cpu().numpy()
        conf = result.boxes.conf[0].cpu().numpy()

        x_center = float((box[0] + box[2]) / 2)
        y_center = float((box[1] + box[3]) / 2)

        ball_data.append({
            "frame": frame_id,
            "time": round(frame_id / fps, 3),
            "x": x_center,
            "y": y_center,
            "conf": float(conf)
        })

# Сохранение данных
with open("ball_tracks.json", "w", encoding="utf-8") as f:
    json.dump(ball_data, f, indent=4)

print(f"\nГотово, обработано кадров: {frame_id + 1}")
print(f"Найдено кадров с мячом: {len(ball_data)}")
print("Данные сохранены в файл ball_tracks.json")