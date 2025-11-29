import os
import argparse
import requests
import logging
from dotenv import load_dotenv
import gspread
from typing import List, Dict

load_dotenv()

YT_API_KEY = os.getenv('YT_API_KEY')
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
SHEET_ID = os.getenv('SHEET_ID')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
YOUTUBE_VIDEOS_URL = 'https://www.googleapis.com/youtube/v3/videos'


def search_recent_videos(api_key: str, query: str, max_results: int = 50) -> List[Dict]:
    """Search YouTube for recent videos matching query and return a list of video IDs+metadata."""
    if not api_key:
        raise ValueError('YT_API_KEY is required')

    params = {
        'part': 'snippet',
        'q': query,
        'order': 'date',
        'type': 'video',
        'maxResults': min(max_results, 50),
        'key': api_key
    }
    resp = requests.get(YOUTUBE_SEARCH_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for item in data.get('items', []):
        vid = item['id']['videoId']
        snippet = item['snippet']
        results.append({'videoId': vid, 'title': snippet.get('title'), 'publishedAt': snippet.get('publishedAt'), 'channelTitle': snippet.get('channelTitle')})
    return results


def get_videos_statistics(api_key: str, video_ids: List[str]) -> List[Dict]:
    if not api_key:
        raise ValueError('YT_API_KEY is required')
    if not video_ids:
        return []

    params = {
        'part': 'statistics,snippet',
        'id': ','.join(video_ids),
        'key': api_key,
        'maxResults': len(video_ids)
    }
    resp = requests.get(YOUTUBE_VIDEOS_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    out = []
    for item in data.get('items', []):
        stats = item.get('statistics', {})
        snippet = item.get('snippet', {})
        view_count = int(stats.get('viewCount', 0))
        out.append({
            'videoId': item.get('id'),
            'title': snippet.get('title'),
            'channelTitle': snippet.get('channelTitle'),
            'publishedAt': snippet.get('publishedAt'),
            'viewCount': view_count,
            'url': f"https://www.youtube.com/watch?v={item.get('id')}"
        })
    return out


def filter_videos_by_views(videos: List[Dict], min_views: int) -> List[Dict]:
    return [v for v in videos if v.get('viewCount', 0) >= min_views]


def write_to_sheet(service_account_file: str, sheet_id: str, rows: List[List]):
    if not service_account_file or not sheet_id:
        raise ValueError('SERVICE_ACCOUNT_FILE and SHEET_ID are required to write to Google Sheets')

    gc = gspread.service_account(filename=service_account_file)
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Append rows
    for row in rows:
        worksheet.append_row(row)


def build_rows(videos: List[Dict]) -> List[List]:
    header = ['Published At', 'Title', 'Channel', 'Views', 'URL']
    rows = [header]
    for v in videos:
        rows.append([v.get('publishedAt'), v.get('title'), v.get('channelTitle'), v.get('viewCount'), v.get('url')])
    return rows


def main():
    parser = argparse.ArgumentParser(description='YouTube → Google Sheets exporter')
    parser.add_argument('--keyword', '-k', required=False, help='Search keyword', default=os.getenv('KEYWORD'))
    parser.add_argument('--min-views', type=int, default=int(os.getenv('MIN_VIEWS', '1000')))
    parser.add_argument('--max-results', type=int, default=int(os.getenv('MAX_RESULTS', '50')))
    parser.add_argument('--service-account', default=SERVICE_ACCOUNT_FILE)
    parser.add_argument('--sheet-id', default=SHEET_ID)
    args = parser.parse_args()

    if not args.keyword:
        logger.error('Please specify --keyword or set KEYWORD in the environment')
        return

    logger.info('Searching YouTube...')
    candidates = search_recent_videos(YT_API_KEY, args.keyword, max_results=args.max_results)
    ids = [c['videoId'] for c in candidates]
    logger.info(f'Found {len(ids)} candidate videos; fetching stats...')
    stats = get_videos_statistics(YT_API_KEY, ids)

    filtered = filter_videos_by_views(stats, args.min_views)
    logger.info(f'{len(filtered)} videos pass the min-views filter ({args.min_views})')

    if filtered:
        rows = build_rows(filtered)
        logger.info('Writing results to Google Sheets...')
        write_to_sheet(args.service_account, args.sheet_id, rows)
        logger.info('Done.')
    else:
        logger.info('No videos met the criteria.')


if __name__ == '__main__':
    main()
