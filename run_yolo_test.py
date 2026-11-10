from ultralytics import YOLO
import time

# Загружаем нашу модель
print("Загрузка модели...")
model = YOLO("yolo26s_players_ball.pt")

# Засекаем время
start_time = time.time()

# Запускаем предсказание
# save=True сохранит видео с нарисованными рамками
# conf=0.3 означает, что мы показываем только объекты, в которых модель уверена на 30% и более
print("Начинаем обработку видео...")
results = model.predict(source="test_video.mp4", save=True, conf=0.3)

end_time = time.time()
print(f"Готово, обработка выполнялась {end_time - start_time:.2f} секунд.")
print("Проверьте папку 'runs'.")