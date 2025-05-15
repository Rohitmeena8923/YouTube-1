from pytube import YouTube, Search

def search_youtube(query):
    s = Search(query)
    s.results
    return [{'title': v.title, 'url': v.watch_url} for v in s.results[:20]]

def download_youtube_video(url, quality='1080p'):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, res=quality).first()
    if not stream:
        stream = yt.streams.get_highest_resolution()
    return stream.download(filename='video.mp4')