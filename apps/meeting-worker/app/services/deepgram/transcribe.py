from uuid import UUID
from deepgram import DeepgramClient
import os 
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Dialogue, TranscriptionJob, TranscriptionJobStatus

load_dotenv()

client = DeepgramClient(api_key="DEEPGRAM_API_KEY")

def transcribe_audio(file_path:str,meeting_id:str):

    try:

        db:Session = SessionLocal()

        transcribe_row = TranscriptionJob(meeting_id=meeting_id,status=TranscriptionJobStatus.queued)
        db.add(transcribe_row)
        db.commit()
        db.refresh(transcribe_row)
        with open(file_path,"rb") as file:
            transcription = client.listen.v1.media.transcribe_file(
                request=file.read(),
                model="nova-2-meeting",
                diarize=True,
                smart_format=True
            )
            paragraphs = transcription.results.channels[0].alternatives[0].paragraphs.paragraphs
            dialouges = []

            for idx,para in enumerate(paragraphs):

                texts = [txt.text for txt in para.sentences]
                full_text = " ".join(texts)

                dialouges.append(
                    Dialogue(
                        meeting_id=meeting_id,
                        speaker=para.speaker,
                        text=full_text,
                        start_time=int(para.start),
                        end_time=int(para.end),
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