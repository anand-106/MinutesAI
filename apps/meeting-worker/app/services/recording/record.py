import asyncio
import os
import subprocess
from app.services.browser.join_button import join_button
from app.services.browser.confirm_join import confirm_join
from playwright.async_api import async_playwright


class RecordingJob:
    def __init__(self,meeting_id:str,meet_link:str,user_id:str):
        self.meeting_id = meeting_id
        self.meet_link = meet_link
        self.user_id = user_id
        self.display = ":99"
        self.audio_sink = "meeting_sink"
        self.audio_module_id=None
        self.ffmpeg_process = None
        self.context = None
        self.browser = None
        self.playwright = None
        self.page = None
        self.outputFileName = f"recordings/{meeting_id}.mp4"
        self.s3_key = f"{user_id}/meetings/{self.meeting_id}.mp4"
        self.duration = 0
    
    def start_display(self):
        os.environ["DISPLAY"] = self.display
        xvfb_process = subprocess.Popen([
        "Xvfb", self.display, "-screen", "0", "1280x720x24", "-ac"
        ])
        import time
        time.sleep(2)  
        return xvfb_process
    

    def start_audio(self):

        result = subprocess.run(
            [
                "pactl",
                "load-module",
                "module-null-sink",
                f"sink_name={self.audio_sink}",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        self.audio_module_id = result.stdout.strip()
        subprocess.run([
        "pactl", "set-default-sink", self.audio_sink
         ], check=True)

    async def start_browser(self):
        os.environ["DISPLAY"] = self.display
        self.playwright =await async_playwright().start()

        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=[
                "--use-fake-ui-for-media-stream",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--use-fake-device-for-media-stream",

            ]
        )

        self.context = await self.browser.new_context(
            permissions=["microphone", "camera"],
            viewport={"width":1280,"height":720},
            storage_state="auth.json"
        )


        self.page = await self.context.new_page()

        await self.page.goto(self.meet_link,timeout=60000)

        await self.page.wait_for_selector("button",timeout=30000)

        mic_btn = self.page.get_by_role("button",name="Turn off microphone")

        await mic_btn.click()

        cam_btn = self.page.get_by_role("button",name="Turn off camera")

        await cam_btn.click()

        await join_button(self.page)
        print("clicked join button")

        await confirm_join(self.page)

        print("Joined google meet")


    def start_ffmpeg(self):
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "x11grab",
            "-video_size", "1280x720",
            "-i", self.display,
            "-f", "pulse",
            "-i", f"{self.audio_sink}.monitor",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            self.outputFileName
        ]

        self.ffmpeg_process = subprocess.Popen(cmd)


    async def stop(self):
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
        
            result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                self.outputFileName,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        self.duration = int(float(result.stdout.strip()))
        
        from app.services.s3.s3_uploader import multipart_upload_file

        multipart_upload_file(
            file_path=self.outputFileName,
            key=self.s3_key,
            meeting_id= self.meeting_id,
            duration=self.duration
        )
        
        if self.audio_module_id:
            subprocess.run(
                ["pactl", "unload-module", self.audio_module_id],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

        try:
            os.remove(self.outputFileName)
        except OSError:
            pass

    def cleanup(self):
        pass