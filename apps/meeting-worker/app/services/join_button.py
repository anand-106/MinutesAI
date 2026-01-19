from playwright.async_api import Page

async def join_button(page:Page):

    for text in [ "Ask to join","Join now"]:
        try:
            # btn = await page.wait_for_selector(f'button:has-text("{text}")')

            # await btn.click()
            await page.get_by_text(text,exact=True).click()
            return
        except :
            continue
    
    raise RuntimeError("Join button not found")