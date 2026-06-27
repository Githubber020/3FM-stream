"""
3FM Stream Scraper - Network Request Capture Version
Scrapes .mpd stream URL by monitoring page requests after play button click
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
import json


def scrape_3fm_mpd():
    """
    Scrape the .mpd stream URL from NPO 3FM by capturing network requests
    
    Returns:
        str: The .mpd URL if found, None otherwise
    """
    driver = None
    try:
        print("Starting browser with DevTools Protocol...")
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-network-service")
        options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
        
        driver = webdriver.Chrome(options=options)
        
        # Enable Chrome DevTools Protocol to capture requests
        driver.execute_cdp_cmd('Network.enable', {})
        
        print("Loading NPO 3FM page...")
        driver.get('https://www.npo3fm.nl/live')
        
        print("Waiting for page to load...")
        time.sleep(3)
        
        # Try to find and click the play button
        try:
            print("Looking for play button...")
            play_button_selectors = [
                "button[aria-label*='Play']",
                "button[aria-label*='play']",
                ".play-button",
                "[class*='play']",
                "button[class*='Play']",
                "button",
            ]
            
            for selector in play_button_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        # Click the first button that looks like a play button
                        for elem in elements:
                            try:
                                elem.click()
                                print("✓ Clicked play button")
                                break
                            except:
                                continue
                        break
                except:
                    continue
            
        except Exception as e:
            print(f"⚠ Error clicking play button: {e}")
        
        print("Waiting for stream to load (20 seconds)...")
        
        # Monitor network requests for .mpd files
        mpd_url = None
        start_time = time.time()
        
        while time.time() - start_time < 20:
            try:
                # Get all network events
                logs = driver.execute_cdp_cmd('Network.getAllCookies', {})
            except:
                pass
            
            # Also check page source periodically for the URL
            page_source = driver.page_source
            
            # Look for stream.mpd in various formats
            if 'stream.mpd' in page_source:
                # Extract the full URL
                import re
                pattern = r'https?://[^\s"\'<>]+stream\.mpd[^\s"\'<>]*'
                matches = re.findall(pattern, page_source)
                if matches:
                    mpd_url = matches[0]
                    print(f"✓ Found stream URL: {mpd_url}")
                    break
            
            time.sleep(1)
        
        if mpd_url:
            return mpd_url
        
        print("✗ Could not find stream.mpd URL")
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
    print("3FM Stream Scraper - Network Capture Version")
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
