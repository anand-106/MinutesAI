from playwright.async_api import Page


async def confirm_join(page:Page):

    try:

        await page.wait_for_selector(
            'button[aria-label*="Leave call"]',
            timeout=30000
        )
    except TimeoutError:
        raise RuntimeError("Failed to join meeting")