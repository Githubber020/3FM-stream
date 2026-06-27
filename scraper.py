"""
3FM Stream Scraper
Scrapes .mpd stream URL from NPO 3FM every 24 hours and updates 3fmstream.txt
"""

import requests
import re
import os
import sys
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
        
        response = requests.get('https://www.npo3fm.nl/live', headers=headers, timeout=10)
        response.raise_for_status()
        
        # Look for .mpd URL patterns in the page content
        # Common patterns for HLS/DASH streams
        mpd_patterns = [
            r'https?://[^\s"\'<>]+\.mpd',
            r'https?://[^\s"\'<>]+\.m3u8',
        ]
        
        content = response.text
        
        for pattern in mpd_patterns:
            matches = re.findall(pattern, content)
            if matches:
                # Return the first match (usually the main stream)
                return matches[0]
        
        print("Warning: No .mpd or .m3u8 URL found in page content")
        return None
        
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during scraping: {e}")
        return None


def read_current_mpd(filepath):
    """
    Read the current .mpd URL from the file
    
    Args:
        filepath (str): Path to 3fmstream.txt
        
    Returns:
        str: The current .mpd URL if file exists, None otherwise
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
                return content if content else None
        except Exception as e:
            print(f"Error reading current file: {e}")
            return None
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
        content = f"URL: {new_mpd}\nLast Updated: {timestamp}\n"
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"Successfully updated {filepath}")
        return True
        
    except Exception as e:
        print(f"Error writing to file: {e}")
        return False


def main():
    """Main function to orchestrate the scraping and updating process"""
    
    filepath = '3fmstream.txt'
    
    print("=" * 50)
    print("3FM Stream Scraper")
    print(f"Started at: {datetime.now().isoformat()}")
    print("=" * 50)
    
    # Scrape new .mpd
    print("Scraping NPO 3FM for .mpd URL...")
    new_mpd = scrape_3fm_mpd()
    
    if not new_mpd:
        print("Failed to scrape new .mpd URL")
        sys.exit(1)
    
    print(f"Found .mpd: {new_mpd[:80]}..." if len(new_mpd) > 80 else f"Found .mpd: {new_mpd}")
    
    # Read current .mpd
    current_mpd = read_current_mpd(filepath)
    
    if current_mpd == new_mpd:
        print("Stream URL unchanged - no update needed")
        sys.exit(0)
    
    if current_mpd:
        print(f"Stream URL changed")
        print(f"Old: {current_mpd[:80]}..." if len(current_mpd) > 80 else f"Old: {current_mpd}")
        print(f"New: {new_mpd[:80]}..." if len(new_mpd) > 80 else f"New: {new_mpd}")
    else:
        print("Creating new stream file...")
    
    # Update the file
    if update_mpd_file(filepath, new_mpd):
        print("Update completed successfully")
        sys.exit(0)
    else:
        print("Failed to update file")
        sys.exit(1)


if __name__ == '__main__':
    main()
