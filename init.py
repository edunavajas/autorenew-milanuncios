from playwright.sync_api import sync_playwright
import os
import time

# Environment variables for email and password
EMAIL = os.getenv('MILANUNCIOS_EMAIL')
PASSWORD = os.getenv('MILANUNCIOS_PASSWORD')

# URLs
URL_LOGIN = "https://www.milanuncios.com/"
URL_MY_ADS = "https://www.milanuncios.com/mis-anuncios/"

def renew_ads():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Go to the login page
        page.goto(URL_LOGIN)

        # Click "Login" button by class name
        page.click('.ma-NavigationTopNav-mainActions-action')

        # Click "Continue with email" by class name
        page.click('.sui-AtomButton--outline')

        # Fill in the email and password
        page.fill('#email', EMAIL)
        page.fill('#password', PASSWORD)

        # Submit the login form by clicking the "Submit" button
        page.click('.ma-FormLogin-submitButton')

        # Navigate to "My Ads" page
        page.goto(URL_MY_ADS)

        # Wait for the ads to load
        page.wait_for_selector('.ma-AdCardV2')

        # Select all ads
        ads = page.query_selector_all('.ma-AdCardV2')

        for ad in ads:
            try:
                # Find and click the "Renew" button by class name
                renew_button = ad.query_selector('.ma-AdCardV2-renewButton')
                if renew_button:
                    renew_button.click()
                    time.sleep(0.1)  # Delay for 100 ms
            except Exception as e:
                print(f"Error while renewing an ad: {e}")
                continue

        # Close the browser
        browser.close()

if __name__ == "__main__":
    renew_ads()
