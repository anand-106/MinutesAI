from playwright.async_api import Page

async def enter_name(page:Page,name:str):

    try:
        await page.get_by_placeholder("Your name").fill(name)
        return
    except :
        raise RuntimeError("Error entering name")
