import os
import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

STEAM_USERNAME = os.getenv("STEAM_USERNAME")
STEAM_PASSWORD = os.getenv("STEAM_PASSWORD")
LOGIN_STATE_FILE = "login_state.json"

async def login_steam(context):
    page = await context.new_page()
    await page.goto("https://store.steampowered.com/login/")

    if await page.query_selector("input#input_username"):
        print("Logging into Steam...")
        await page.fill("input#input_username", STEAM_USERNAME)
        await page.fill("input#input_password", STEAM_PASSWORD)
        await page.click("button#login_btn_signin")
        print("Waiting 20 seconds for Steam Guard approval...")
        await asyncio.sleep(20)
        await context.storage_state(path=LOGIN_STATE_FILE)
        print("Steam session saved.")
    else:
        print("Steam login form not found, possibly already logged in.")
    await page.close()

async def login_rustypot(page):
    await page.goto("https://rustypot.com")

    if await page.query_selector("a.btn-steam"):
        print("Logging into Rustypot with Steam...")
        await page.click("a.btn-steam")

        if page.url.startswith("https://steamcommunity.com/openid/login"):
            if await page.query_selector("input#input_username"):
                await page.fill("input#input_username", STEAM_USERNAME)
                await page.fill("input#input_password", STEAM_PASSWORD)
                await page.click("button#login_btn_signin")
                print("Waiting 20 seconds for Steam Guard approval on OAuth login...")
                await asyncio.sleep(20)

        await page.wait_for_load_state("networkidle")
        print(f"Rustypot login complete. Current URL: {page.url}")
    else:
        print("Already logged into Rustypot.")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = None
        if os.path.exists(LOGIN_STATE_FILE):
            print("Loading existing Steam session...")
            context = await browser.new_context(storage_state=LOGIN_STATE_FILE)
        else:
            print("No existing Steam session, creating new context...")
            context = await browser.new_context()

        await login_steam(context)
        page = await context.new_page()
        await login_rustypot(page)

        await page.screenshot(path="rustypot_login_success.png")
        print("Screenshot saved as rustypot_login_success.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
