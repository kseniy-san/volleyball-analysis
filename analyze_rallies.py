import json

# --- Параметры исследования ---
MIN_RALLY_DURATION = 4.0  # Минимальная длина розыгрыша в секундах
MAX_GAP = 3.0  # Максимальный пропуск мяча в секундах (если больше - розыгрыш окончен)

# Данные с координатами мяча
with open("ball_tracks.json", "r", encoding="utf-8") as f:
    ball_data = json.load(f)

# Если данных нет, выходим
if not ball_data:
    print("Нет данных о мяче")
    exit()

rallies = []
current_start = ball_data[0]["time"]  # Время начала текущего отрезка
last_seen = ball_data[0]["time"]  # Время последнего найденного мяча

print(f"Всего кадров с мячом: {len(ball_data)}")
print("Начинаем поиск розыгрышей...")

for i in range(1, len(ball_data)):
    current_time = ball_data[i]["time"]

    # Смотрим, какая пауза между текущим кадром и предыдущим
    gap = current_time - last_seen

    if gap > MAX_GAP:
        # Пропуск слишком большой! Значит, предыдущий розыгрыш закончился.
        rally_end = last_seen
        duration = rally_end - current_start

        # Проверяем, достаточно ли он длинный
        if duration >= MIN_RALLY_DURATION:
            rallies.append({
                "start": round(current_start, 2),
                "end": round(rally_end, 2),
                "duration": round(duration, 2)
            })

        # Начинаем новый розыгрыш
        current_start = current_time

    last_seen = current_time

# Добавить последний розыгрыш, если видео закончилось, пока мяч был в игре
rally_end = last_seen
duration = rally_end - current_start
if duration >= MIN_RALLY_DURATION:
    rallies.append({
        "start": round(current_start, 2),
        "end": round(rally_end, 2),
        "duration": round(duration, 2)
    })

# Выводим результат
print(f"\nНайдено розыгрышей: {len(rallies)}")
for i, rally in enumerate(rallies, 1):
    print(f"Розыгрыш {i}: {rally['start']} сек -> {rally['end']} сек (длительность: {rally['duration']} сек)")

# Сохраняем результат в новый файл
final_result = {"rallies": [{"start": r["start"], "end": r["end"]} for r in rallies]}
with open("rallies_found.json", "w", encoding="utf-8") as f:
    json.dump(final_result, f, indent=4)

print("\nИтоговый список сохранен в файл rallies_found.json")