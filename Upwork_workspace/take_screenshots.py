import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Create context with standard screen sizes
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            device_scale_factor=1,
        )
        page = await context.new_page()

        # Define jobs
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if os.path.exists(os.path.join(script_dir, "dennisbui.github.io")):
            assets_dir = os.path.join(script_dir, "dennisbui.github.io/Portfolio_Assets/Ecommerce_Operations")
        else:
            assets_dir = os.path.join(script_dir, "../Portfolio_Assets/Ecommerce_Operations")
            
        jobs = [
            {
                "url": "https://st-unique.myshopify.com/",
                "path": os.path.join(assets_dir, "uma_store.png")
            },
            {
                "url": "https://rozzy-store-demo.myshopify.com/",
                "path": os.path.join(assets_dir, "rozzy_store.png")
            }
        ]

        for job in jobs:
            print(f"Navigating to {job['url']}...")
            try:
                # Go to page and wait for load state
                await page.goto(job['url'], timeout=60000, wait_until="networkidle")
                # Wait additional time for images/banners to render
                await page.wait_for_timeout(3000)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(job['path']), exist_ok=True)
                
                # Take screenshot of the top fold (viewport)
                await page.screenshot(path=job['path'], full_page=False)
                print(f"Saved screenshot to {job['path']}")
            except Exception as e:
                print(f"Error capturing {job['url']}: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
