import asyncio
from app.services.recording.record import RecordingJob

async def join_meeting(ctx,payload):
    
    meet_link = payload.get("meet-link")
    meeting_id = payload.get("meeting_id")
    user_id = payload.get("user_id")

    recorder = RecordingJob(meet_link=meet_link,meeting_id=meeting_id,user_id=user_id)

    recorder.start_display()
    recorder.start_audio()
    await recorder.start_browser()
    recorder.start_ffmpeg()
    
    await recorder.page.wait_for_function(
    """
    () => {
        const texts = [
            "Your host ended the meeting for everyone",
            "You left the meeting",
            "You’ve left the call",
            "The call ended because everyone left"
        ];
        return texts.some(t => document.body.innerText.includes(t));
    }
    """,
    timeout=1000*60*60
)



    await recorder.stop()
    recorder.start_audio_convert()
    recorder.audio_convert_process.wait()
    recorder.transcribe()
    recorder.cleanup()