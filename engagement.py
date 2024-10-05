from playwright.async_api import async_playwright
import asyncio
from time import sleep

async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        )

        page = await context.new_page()
        await page.goto("https://www.tiktok.com/")
        input("Login Done ?")
        url = input("Input Video Url: ")
        await page.goto(url)
        await page.wait_for_load_state('domcontentloaded')

        #Like
        await page.click('span[data-e2e="like-icon"]')

        #comment
        await page.click('span[data-e2e="comment-icon"]')

        await sleep(89999)
if __name__ == '__main__':
    asyncio.run(main())
