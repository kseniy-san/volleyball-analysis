from datetime import datetime
import enum
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from app.database import Base

# --- Enum классы (строгие списки значений) ---
class VideoStatus(str, enum.Enum):
    uploaded = "uploaded"
    queued = "queued"
    processing = "processing"
    completed = "completed"
    error = "error"

class ServeSide(str, enum.Enum):
    unknown = "unknown"
    near = "near"
    far = "far"

# --- Модели (Таблицы) ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь: один пользователь -> много видео
    videos = relationship("Video", back_populates="user")

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    duration = Column(Float)
    fps = Column(Float)
    width = Column(Integer)
    height = Column(Integer)
    status = Column(Enum(VideoStatus), default=VideoStatus.uploaded)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    user = relationship("User", back_populates="videos")
    processing_jobs = relationship("ProcessingJob", back_populates="video")
    rallies = relationship("Rally", back_populates="video")
    detections = relationship("Detection", back_populates="video")

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    status = Column(String)
    progress = Column(Integer, default=0)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    video = relationship("Video", back_populates="processing_jobs")

class Rally(Base):
    __tablename__ = "rallies"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    number = Column(Integer, nullable=False)
    start_time = Column(Float, nullable=False)
    end_time = Column(Float, nullable=False)
    start_frame = Column(Integer)
    end_frame = Column(Integer)
    serve_side = Column(Enum(ServeSide), default=ServeSide.unknown)

    video = relationship("Video", back_populates="rallies")

class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    frame = Column(Integer, nullable=False)
    class_name = Column("class", String) # "class" - зарезервированное слово в Python, поэтому используем class_name
    x = Column(Float)
    y = Column(Float)
    w = Column(Float)
    h = Column(Float)
    confidence = Column(Float)

    video = relationship("Video", back_populates="detections")