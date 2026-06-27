"""
3FM Stream Scraper - Test Version
Scrapes .mpd stream URL by clicking play button and monitoring page source
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
    Scrape the .mpd stream URL from NPO 3FM by clicking play and waiting
    
    Returns:
        str: The .mpd URL if found, None otherwise
    """
    driver = None
    try:
        print("Starting browser...")
        options = webdriver.ChromeOptions()
        
        driver = webdriver.Chrome(options=options)
        
        print("Loading NPO 3FM page...")
        driver.get('https://www.npo3fm.nl/live')
        
        print("Waiting for page to load...")
        time.sleep(3)
        
        # Try to find and click the play button
        try:
            print("Looking for play button...")
            # Try multiple selectors for play button
            play_button_selectors = [
                "button[aria-label*='Play']",
                "button[aria-label*='play']",
                ".play-button",
                "[class*='play']",
                "button[class*='Play']",
            ]
            
            play_button = None
            for selector in play_button_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        play_button = elements[0]
                        print(f"✓ Found play button with selector: {selector}")
                        play_button.click()
                        print("✓ Clicked play button")
                        break
                except:
                    continue
            
            if not play_button:
                print("⚠ Could not find play button, continuing anyway...")
        
        except Exception as e:
            print(f"⚠ Error clicking play button: {e}")
        
        print("Waiting for stream to load (10 seconds)...")
        time.sleep(10)
        
        # Get page source after stream loads
        page_source = driver.page_source
        
        # Search for .mpd or .m3u8 URLs in the page source
        mpd_patterns = [
            r'https?://[^\s"\'<>]+\.mpd(?:["\'\s<>]|$)',
            r'https?://[^\s"\'<>]+\.m3u8(?:["\'\s<>]|$)',
        ]
        
        print("Searching for stream URL...")
        for pattern in mpd_patterns:
            matches = re.findall(pattern, page_source)
            if matches:
                # Clean up the URL (remove trailing quotes/spaces)
                stream_url = matches[0].rstrip('\'" ')
                print(f"✓ Found stream URL: {stream_url}")
                return stream_url
        
        print("✗ No .mpd or .m3u8 URL found in page source")
        
        # Try alternative: search in JavaScript code
        print("Searching in page HTML for manifest URLs...")
        manifest_pattern = r'(?:src|url|href)["\']?\s*:\s*["\']?(https?://[^\s"\'<>]+\.(?:mpd|m3u8))'
        matches = re.findall(manifest_pattern, page_source)
        if matches:
            stream_url = matches[0]
            print(f"✓ Found stream URL in HTML: {stream_url}")
            return stream_url
        
        return None
        
    except Exception as e:
        print(f"✗ Error during scraping: {e}")
        import traceback
        traceback.print_exc()
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
    print("3FM Stream Scraper - Play Button Version")
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
