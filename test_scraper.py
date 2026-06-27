"""
3FM Stream Scraper - Test Version
Scrapes .mpd stream URL from NPO 3FM and updates 3fmstream.txt immediately
"""

import requests
import re
from datetime import datetime


def scrape_3fm_mpd():
    """
    Scrape the .mpd stream URL from NPO 3FM live page
    
    Returns:
        str: The .mpd URL if found, None otherwise
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print("Fetching NPO 3FM page...")
        response = requests.get('https://www.npo3fm.nl/live', headers=headers, timeout=10)
        response.raise_for_status()
        
        # Look for .mpd URL patterns in the page content
        mpd_patterns = [
            r'https?://[^\s"\'<>]+\.mpd',
            r'https?://[^\s"\'<>]+\.m3u8',
        ]
        
        content = response.text
        print(f"Page fetched successfully. Content length: {len(content)} characters")
        
        for pattern in mpd_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # Return the first match (usually the main stream)
                stream_url = matches[0]
                print(f"✓ Found stream URL: {stream_url}")
                return stream_url
        
        print("✗ No .mpd or .m3u8 URL found in page content")
        return None
        
    except requests.RequestException as e:
        print(f"✗ Error fetching page: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error during scraping: {e}")
        return None


def update_mpd_file(filepath, new_mpd):
    """
    Update the 3fmstream.txt file with new .mpd URL and timestamp
    
    Args:
        filepath (str): Path to 3fmstream.txt
        new_mpd (str): The new .mpd URL
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        timestamp = datetime.now().isoformat()
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
    print("3FM Stream Scraper - TEST VERSION")
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
