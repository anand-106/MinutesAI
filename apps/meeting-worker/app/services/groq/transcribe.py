from uuid import UUID
from groq import Groq
import os 
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Dialogue, TranscriptionJob, TranscriptionJobStatus

load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def transcribe_audio(file_path:str,meeting_id:str):

    try:

        db:Session = SessionLocal()

        transcribe_row = TranscriptionJob(meeting_id=meeting_id,status=TranscriptionJobStatus.queued)
        db.add(transcribe_row)
        db.commit()
        db.refresh(transcribe_row)
        with open(file_path,"rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(file_path,file.read()),
                model="whisper-large-v3-turbo",
                temperature=0,
                response_format="verbose_json"
            )

            dialouges = []

            for idx,seg in enumerate(transcription.segments):

                dialouges.append(
                    Dialogue(
                        meeting_id=meeting_id,
                        speaker="Speaker 1",
                        text=seg["text"],
                        start_time=int(seg["start"]),
                        end_time=int(seg["end"]),
                        sequence=idx
                    )
                )
            
            db.bulk_save_objects(dialouges)
            transcribe_row.status=TranscriptionJobStatus.completed
            db.commit()
 
    except Exception as e:
        print(f"Transcription error: {e}")
        if transcribe_row:
            transcribe_row.status = TranscriptionJobStatus.failed
            db.commit()
        raise
    finally:
        db.close()