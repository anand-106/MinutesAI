import asyncio
from app.services.recording.record import RecordingJob

async def join_meeting(ctx,payload):
    
    meet_link = payload.get("meet-link")
    meeting_id = payload.get("meeting_id")

    recorder = RecordingJob(meet_link=meet_link,meeting_id=meeting_id)

    recorder.start_display()
    recorder.start_audio()
    await recorder.start_browser()
    recorder.start_ffmpeg()

    await asyncio.sleep(30)

    await recorder.stop()