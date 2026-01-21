from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def launch_browser():

    playwright =await async_playwright().start()

    browser = await playwright.chromium.launch(
        headless=True,
        args=[
            "--use-fake-ui-for-media-stream",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
             "--use-fake-device-for-media-stream",

        ]
    )

    context = await browser.new_context(
        permissions=["microphone", "camera"],
        viewport={"width":1280,"height":720},
        storage_state="auth.json"
    )


    page = await context.new_page()

    return browser,page