"""
3FM Stream Scraper - Test Version with Network Monitoring
Scrapes .mpd stream URL from NPO 3FM by monitoring network requests
"""

from seleniumwire import webdriver
import re
import time
from datetime import datetime


def scrape_3fm_mpd():
    """
    Scrape the .mpd stream URL from NPO 3FM by monitoring network requests
    
    Returns:
        str: The .mpd URL if found, None otherwise
    """
    driver = None
    try:
        print("Starting browser with network monitoring...")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        
        driver = webdriver.Chrome(options=options)
        
        print("Loading NPO 3FM page...")
        driver.get('https://www.npo3fm.nl/live')
        
        print("Waiting for network requests (15 seconds)...")
        time.sleep(15)
        
        # Monitor network requests for .mpd or .m3u8 files
        print("Searching through network requests...")
        mpd_url = None
        
        for request in driver.requests:
            url = request.url
            
            # Look for .mpd or .m3u8 in the request URL
            if '.mpd' in url or '.m3u8' in url:
                print(f"✓ Found stream URL in network requests: {url}")
                mpd_url = url
                break
        
        if mpd_url:
            return mpd_url
        
        print("✗ No .mpd or .m3u8 URL found in network requests")
        print(f"Total requests captured: {len(driver.requests)}")
        
        # Debug: Show some of the requests
        print("\nSample of captured requests:")
        for i, request in enumerate(driver.requests[:10]):
            print(f"  {i+1}. {request.url[:100]}")
        
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
    print("3FM Stream Scraper - Network Monitoring Version")
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
