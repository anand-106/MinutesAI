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

        # await enter_name(page,"Minutes AI")
        # print("Entered the Name")

        mic_btn = page.get_by_role("button",name="Turn off microphone")

        await mic_btn.click()

        cam_btn = page.get_by_role("button",name="Turn off camera")

        await cam_btn.click()

        # await disable_button(page,'button[aria-label*="Turn off microphone"]')

        # await disable_button(page,'button[aria-label*="Turn off camera"]')

        # await page.screenshot(
        #     path="before_join.png",
        #     full_page=False
        # )
        # print("Screenshot saved: before_join.png")

        # await asyncio.sleep(120)

        await join_button(page)
        print("clicked join button")

        await confirm_join(page)

        print("Joined google meet")

        await asyncio.sleep(10000)
    
    finally:
        await browser.close()