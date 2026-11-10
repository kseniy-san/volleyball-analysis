import json
from app.database import SessionLocal, engine
from app.models import Base, Rally, Video, User, VideoStatus

# Для теста мы создадим базу заново, чтобы не было конфликтов
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# 1. Создадим тестового пользователя
user = db.query(User).filter(User.email == "test@test.ru").first()
if not user:
    user = User(email="test@test.ru", password_hash="12345")
    db.add(user)
    db.commit()

# 2. Создадим запись о нашем тестовом видео
video = db.query(Video).filter(Video.filename == "test_video.mp4").first()
if not video:
    video = Video(
        user_id=user.id,
        filename="test_video.mp4",
        duration=60.0,
        fps=30.0,
        width=1920,
        height=1080,
        status=VideoStatus.completed
    )
    db.add(video)
    db.commit()

# 3. Загружаем наши найденные розыгрыши из JSON
with open("rallies_found.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 4. Сохраняем их в базу
for i, r in enumerate(data["rallies"], start=1):
    # Проверяем, нет ли уже такого розыгрыша (чтобы не дублировать)
    existing = db.query(Rally).filter(Rally.video_id == video.id, Rally.number == i).first()
    if not existing:
        new_rally = Rally(
            video_id=video.id,
            number=i,
            start_time=r["start"],
            end_time=r["end"],
            start_frame=int(r["start"] * 30),
            end_frame=int(r["end"] * 30),
            serve_side="unknown"
        )
        db.add(new_rally)

db.commit()
db.close()
print(f"Готово, {len(data['rallies'])} розыгрышей сохранены в базу данных.")