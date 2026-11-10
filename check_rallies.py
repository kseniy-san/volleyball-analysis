from app.database import SessionLocal
from app.models import Rally, Video

# Открываем сессию
db = SessionLocal()

print("Проверяем данные в базе")

# Видео
videos = db.query(Video).all()
print(f"\nНайдено видео в базе: {len(videos)}")
for v in videos:
    print(f" - ID: {v.id}, Файл: {v.filename}, Статус: {v.status}")

# Розыгрыши
rallies = db.query(Rally).all()
print(f"\nНайдено розыгрышей в базе: {len(rallies)}")

for r in rallies:
    print(f"Розыгрыш #{r.number}: с {r.start_time} сек по {r.end_time} сек (видео ID: {r.video_id}, подача: {r.serve_side})")

db.close()