import asyncio
# 비동기

from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        for browser_type in [p.chromium]:
            browser = await browser_type.launch()
            page = await browser.new_page()
            await page.goto('http://whatsmyuseragent.org/')
            await page.screenshot(path=f'example-{browser_type.name}.png')
            await browser.close()

# [ 출처: https://choiseokwon.tistory.com/ ]
asyncio.run(main())