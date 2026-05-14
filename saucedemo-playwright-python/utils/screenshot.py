import os
from datetime import datetime

def take_screenshot(page, name):
    os.makedirs("reports/screenshots", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"reports/screenshots/{name}_{timestamp}.png"
    page.screenshot(path=path)
    return path
