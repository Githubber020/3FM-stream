"""
3FM Stream Scraper - Test Version with Selenium
Scrapes .mpd stream URL from NPO 3FM and updates 3fmstream.txt immediately
Waits for JavaScript to load the stream URL
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from datetime import datetime


def scrape_3fm_mpd():
    """
    Scrape the .mpd stream URL from NPO 3FM live page using Selenium
    Waits for JavaScript to load the stream
    
    Returns:
        str: The .mpd URL if found, None otherwise
    """
    driver = None
    try:
        print("Starting browser...")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        
        driver = webdriver.Chrome(options=options)
        
        print("Loading NPO 3FM page...")
        driver.get('https://www.npo3fm.nl/live')
        
        print("Waiting for page to load and JavaScript to render (10 seconds)...")
        time.sleep(10)
        
        # Get the page content after JavaScript has loaded
        page_content = driver.page_source
        print(f"✓ Page loaded. Content length: {len(page_content)} characters")
        
        # Look for .mpd URL patterns
        mpd_patterns = [
            r'https?://[^\s"\'<>]+\.mpd',
            r'https?://[^\s"\'<>]+\.m3u8',
        ]
        
        for pattern in mpd_patterns:
            matches = re.findall(pattern, page_content)
            if matches:
                stream_url = matches[0]
                print(f"✓ Found stream URL: {stream_url}")
                return stream_url
        
        print("✗ No .mpd or .m3u8 URL found in page content")
        return None
        
    except Exception as e:
        print(f"✗ Error during scraping: {e}")
        return None
    finally:
        if driver:
            print("Closing browser...")
            driver.quit()


def update_mpd_file(filepath, new_mpd):
    """
    Update the 3fmstream.txt file with new .mpd URL
    
    Args:
        filepath (str): Path to 3fmstream.txt
        new_mpd (str): The new .mpd URL
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        content = f"{new_mpd}\n"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✓ Successfully updated {filepath}")
        return True
        
    except Exception as e:
        print(f"✗ Error writing to file: {e}")
        return False


def main():
    """Main function"""
    
    filepath = '3fmstream.txt'
    
    print("=" * 60)
    print("3FM Stream Scraper - TEST VERSION (with Selenium)")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Scrape new .mpd
    new_mpd = scrape_3fm_mpd()
    
    if not new_mpd:
        print("\n✗ Failed to scrape .mpd URL")
        return False
    
    # Update the file
    if update_mpd_file(filepath, new_mpd):
        print(f"\n✓ File updated successfully!")
        print(f"Stream URL saved to {filepath}")
        return True
    else:
        print(f"\n✗ Failed to update {filepath}")
        return False


if __name__ == '__main__':
    success = main()
    input("\nPress Enter to exit...")
