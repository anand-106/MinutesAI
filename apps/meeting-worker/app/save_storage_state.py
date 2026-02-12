import asyncio
import os
import tempfile
from playwright.async_api import async_playwright
from playwright_stealth import Stealth


async def main():
    user_data_dir = os.path.join(tempfile.gettempdir(), "pw-chrome-profile")
    os.makedirs(user_data_dir, exist_ok=True)

    stealth = Stealth()

    async with stealth.use_async(async_playwright()) as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-default-browser-check",
                "--no-service-autorun",
                "--password-store=basic",
            ],
            viewport={"width": 1280, "height": 720},
            ignore_default_args=["--enable-automation"],
        )

        page = context.pages[0] if context.pages else await context.new_page()

        await page.goto("https://accounts.google.com/")

        print("Log in manually, then press Enter here when done...")
        input()

        await context.storage_state(path="auth.json")
        await context.close()


asyncio.run(main())