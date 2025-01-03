from playwright.sync_api import sync_playwright
import os
import time
import subprocess
import sys

# Environment variables for email and password
EMAIL = os.getenv('MILANUNCIOS_EMAIL')
PASSWORD = os.getenv('MILANUNCIOS_PASSWORD')

# URLs
URL_LOGIN = "https://www.milanuncios.com/"
URL_MY_ADS = "https://www.milanuncios.com/mis-anuncios/"

VPN_CONFIG = "esp_vpn.ovpn"

def renew_ads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        page = context.new_page()

        print("Go to the login page")
        page.goto(URL_LOGIN)
        
        print(page.content())

        print("Clicking the login button")
        page.click('.ma-NavigationTopNav-mainActions-action')


        print("Clicking the continue with email button")
        page.click('.sui-AtomButton--outline')


        print("Filling in the email and password")
        page.fill('#email', EMAIL)
        page.fill('#password', PASSWORD)

        print("Submitting the login form")
        page.click('.ma-FormLogin-submitButton')

        # Navigate to "My Ads" page
        page.goto(URL_MY_ADS)

        print("Waiting for the ads to load")
        page.wait_for_selector('.ma-AdCardV2')

        print("Selecting all ads")
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
    try:
        print("Conecting to VPN...")
        subprocess.run(["sudo", "wg-quick", "up", VPN_CONFIG], check=True)

        print("VPN connected.")
        renew_ads()
    except subprocess.CalledProcessError as e:
        print(f"Error executting command: {e}", file=sys.stderr)
    finally:
        print("Disconnecting from VPN...")
        subprocess.run(["sudo", "wg-quick", "down", VPN_CONFIG], check=True)
        print("VPN disconnected.")
