from youtube_sheets_export.main import filter_videos_by_views


def test_filter_videos_by_views():
    videos = [
        {'videoId': 'a', 'viewCount': 500},
        {'videoId': 'b', 'viewCount': 1500},
        {'videoId': 'c', 'viewCount': 1000}
    ]
    out = filter_videos_by_views(videos, 1000)
    ids = [v['videoId'] for v in out]
    assert 'b' in ids
    assert 'c' in ids
    assert 'a' not in ids
