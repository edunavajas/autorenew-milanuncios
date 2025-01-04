from playwright.sync_api import sync_playwright
import os
import time
import subprocess
import sys
import json
import random
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

load_dotenv()

# Environment variables for email and password
EMAIL = os.getenv('MILANUNCIOS_EMAIL')
PASSWORD = os.getenv('MILANUNCIOS_PASSWORD')

# URLs
URL = "https://www.milanuncios.com/"
ADS = "mis-anuncios/"
COOKIES_FILE = "cookies.json"

def renew_ads():
    with sync_playwright() as p:
        browser, page = initialize_playwright_session(p)
        
        # monitor_network(page)

        print("Go to the login page")
        page.goto(URL, wait_until="networkidle")
        
        human_scroll_and_interact(page)
        
        page.screenshot(path="first_content.png")
        
        handle_cookie_consent(page)    
        
        page.screenshot(path="second_content.png")

        fill_login_credentials(page)

        page.screenshot(path="thirst_content.png")
        # Navigate to "My Ads" page
        
        time.sleep(3)
        # page.goto(URL + ADS)
        page.screenshot(path="four_content.png")
        skip_tutorial(page)     
            
        print("Waiting for the ads to load")
        page.wait_for_selector('.ma-AdCardV2')
        
        page.screenshot(path="four_content.png")

        #click_renew_buttons(page)

        # Close the browser
        browser.close()

def monitor_network(page):
    # Manejar solicitudes fallidas
    page.on("requestfailed", lambda request: print(
        f"❌ Request failed: {request.url} ({request.failure})"
    ))

    # Registrar todas las respuestas
    page.on("response", lambda response: print(
        f"➡️ Response: {response.url} ({response.status})"
    ))


def click_renew_buttons(page):
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

def skip_tutorial(page):
    try:
        page.wait_for_selector('button[aria-label="Cerrar"][title="Cerrar"]')
        page.click('button[aria-label="Cerrar"][title="Cerrar"]')
    except Exception as e:
        page.screenshot(path="error_skip_tutorial.png")
        print("No tutorial displayed, continuing...")

def handle_cookie_consent(page):
    try:
        page.wait_for_selector("#didomi-notice-agree-button")
        page.click("#didomi-notice-agree-button")
    except Exception as e:
        print("No cookies advert, continuing...")

def fill_login_credentials(page):
    print("Filling in the email and password")
    page.fill('#email', EMAIL)
    page.fill('#password', PASSWORD)

    print("Submitting the login form")
    page.click('.ma-FormLogin-submitButton')

def human_scroll_and_interact(page):
    for _ in range(random.randint(3, 7)):
        x, y = random.randint(0, 800), random.randint(0, 600)
        page.mouse.move(x, y, steps=random.randint(10, 30))
        time.sleep(random.uniform(0.5, 2))  # Pausa más larga
    page.mouse.wheel(delta_x=0, delta_y=random.randint(200, 500))
    page.wait_for_timeout(random.uniform(1, 3))  # Espera antes de la próxima acción

def random_coordinates_in_spain():
    # Rango aproximado de latitudes y longitudes de España
    lat_min, lat_max = 36.0, 43.0  # Desde el sur (Andalucía) al norte (Galicia)
    lon_min, lon_max = -9.3, 3.3   # Desde el oeste (Galicia) al este (Cataluña)

    latitude = round(random.uniform(lat_min, lat_max), 6)
    longitude = round(random.uniform(lon_min, lon_max), 6)
    
    return {"latitude": latitude, "longitude": longitude, "accuracy": 10}

def initialize_playwright_session(p):
    browser = p.chromium.launch(
            headless=True,
            args=["--disable-webrtc"])

    geo = random_coordinates_in_spain()
    print(f"Simulando ubicación: {geo}")
    context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            java_script_enabled=True,
            ignore_https_errors=True,
            bypass_csp=True,
            locale="es-ES",
            timezone_id="Europe/Madrid",
            geolocation=geo,
            permissions=["geolocation"])
        
   #with open(COOKIES_FILE, "r") as f:
   #    cookies = json.load(f)
   #context.add_cookies(cookies)
    
    context.route("**/*", lambda route, request: time.sleep(random.uniform(0.1, 0.3)) or route.continue_())
    
    page = context.new_page()
    
    page.evaluate("""
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    """)

    
    page.set_extra_http_headers({
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9",
    "Sec-CH-UA": '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": URL,
    "DNT": "1"
    })
  
    
    stealth_sync(page)
    
    return browser,page

if __name__ == "__main__":
     renew_ads()