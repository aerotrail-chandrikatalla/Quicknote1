from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------
# FastAPI app setup
# -------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class NoteDB(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)


class Note(BaseModel):
    subject: str
    description: str


@app.post("/notes")
def create_note(note: Note):
    db = SessionLocal()
    new_note = NoteDB(subject=note.subject, description=note.description)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    db.close()
    return {"message": "Note saved successfully!", "id": new_note.id}

@app.get("/notes")
def get_notes():
    db = SessionLocal()
    notes = db.query(NoteDB).all()
    db.close()
    return notes
