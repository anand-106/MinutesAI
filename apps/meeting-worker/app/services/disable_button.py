from playwright.async_api import Page

async def disable_button(page:Page,selector):
    try:
        
        btn = await page.wait_for_selector(selector,timeout=30000)
        pressed = await btn.get_attribute("aria-pressed")

        if pressed:
            await btn.click()
        
    except :
        pass