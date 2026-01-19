import asyncio
from app.services.launch_browser import launch_browser
from app.services.disable_button import disable_button
from app.services.join_button import join_button
from app.services.confirm_join import confirm_join
from app.services.enter_name import enter_name

async def join_meeting(ctx,payload):
    
    meet_link = payload.get("meet-link")

    browser,page = await launch_browser()

    try:

        await page.goto(meet_link,timeout=60000)

        await page.wait_for_selector("button",timeout=30000)

        await enter_name(page,"Minutes AI")
        print("Entered the Name")

        # await disable_button(page,'button[aria-label*="camera"]')

        # await disable_button(page,'button[aria-label*="microphone"]')

        await join_button(page)
        print("clicked join button")

        await confirm_join(page)

        print("Joined google meet")

        await asyncio.sleep(10000)
    
    finally:
        await browser.close()