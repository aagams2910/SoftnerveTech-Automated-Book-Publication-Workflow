import os
import asyncio
from playwright.async_api import async_playwright

def get_output_paths(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    text_path = os.path.join(output_dir, "chapter.txt")
    screenshot_path = os.path.join(output_dir, "screenshot.png")
    return text_path, screenshot_path

async def async_scrape_chapter(url: str, output_dir: str):
    text_path, screenshot_path = get_output_paths(output_dir)
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        await page.screenshot(path=screenshot_path, full_page=True)
        content = await page.query_selector('.mw-parser-output')
        if content:
            text = await content.inner_text()
        else:
            text = await page.content()
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)
        await browser.close()
    return text_path, screenshot_path

def scrape_chapter(url: str, output_dir: str):
    """
    Synchronous wrapper for async_scrape_chapter.
    """
    return asyncio.run(async_scrape_chapter(url, output_dir)) 