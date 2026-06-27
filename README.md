# 3FM Stream Scraper

Automatically scrapes the NPO 3FM live stream .mpd URL every 24 hours and maintains a single `3fmstream.txt` file with the current stream URL.

## Features

- ✅ **Automated Scheduling**: Runs every 24 hours via GitHub Actions
- ✅ **Smart Updates**: Only updates the file when the stream URL changes
- ✅ **Single File Management**: Always maintains one `3fmstream.txt` file (never creates duplicates)
- ✅ **Timestamps**: Includes last update timestamp
- ✅ **Manual Trigger**: Can be manually triggered via GitHub Actions UI

## How It Works

1. **Scraper Script** (`scraper.py`):
   - Fetches the NPO 3FM live page
   - Extracts the .mpd stream URL using regex patterns
   - Compares with the existing URL in `3fmstream.txt`
   - Only updates the file if the URL has changed

2. **GitHub Actions Workflow** (`.github/workflows/scrape-stream.yml`):
   - Runs on a daily schedule (1 AM UTC)
   - Sets up Python environment
   - Installs dependencies
   - Runs the scraper
   - Automatically commits and pushes changes if file is modified

## Output Format

The `3fmstream.txt` file contains:
```
URL: https://example.com/stream.mpd
Last Updated: 2026-06-27T15:30:45.123456
```

## Usage

### Automatic (Recommended)
The workflow runs automatically every 24 hours. No action required.

### Manual Trigger
1. Go to GitHub Actions tab
2. Select "Scrape 3FM Stream" workflow
3. Click "Run workflow"

## File Structure

```
├── scraper.py              # Main scraper script
├── requirements.txt        # Python dependencies
├── .github/
│   └── workflows/
│       └── scrape-stream.yml  # GitHub Actions workflow
├── 3fmstream.txt          # Output file (auto-generated)
└── README.md              # This file
```

## Dependencies

- Python 3.11+
- requests (specified in requirements.txt)

## Configuration

To modify the schedule, edit `.github/workflows/scrape-stream.yml` and change the cron expression:

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # Change this line (1 AM UTC daily)
```

Cron format: `minute hour day month weekday`
- `0 1 * * *` = Daily at 1 AM UTC
- `0 */12 * * *` = Every 12 hours
- `0 0 * * 0` = Weekly on Sunday at midnight

## Troubleshooting

If the workflow fails:

1. Check the Actions tab for error logs
2. Verify the NPO 3FM website structure hasn't changed
3. Check if the URL pattern has changed (may need regex update)
4. Ensure Python and dependencies are correctly installed

## License

MIT
