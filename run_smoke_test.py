from youtube_sheets_export.main import filter_videos_by_views

if __name__ == '__main__':
    videos = [
        {'videoId':'a','viewCount':500},
        {'videoId':'b','viewCount':1500},
        {'videoId':'c','viewCount':1000}
    ]
    out = filter_videos_by_views(videos, 1000)
    print([v['videoId'] for v in out])
