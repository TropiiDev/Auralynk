import yt_dlp
import os
import sys

from serpapi import GoogleSearch
from datetime import datetime

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_youtube(query):
    """Search YouTube using Google and return the first video URL."""
    params = {
        "engine": "youtube",
        "search_query": query,
        "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    videos = results.get("video_results", [])

    if videos:
        return videos[0]["link"]  # Return the first YouTube video link
    else:
        return "No video found."

"""
    HEAVILY MODIFIED CODE FROM https://gist.github.com/Mohammed-Gamal/42089986026b59dce17b317452e10549#file-youtube_downloader-py THANK YOU MOHAMMED GAMAL
"""

def format_size(bytes):
    """
    Convert bytes to human readable format, making file sizes easier to understand.
    Scales from bytes up to gigabytes automatically.
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} GB"


def progress_hook(d):
    """
    Display download progress with detailed information about speed and time remaining.
    Provides real-time feedback during the download process.
    """
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)

        if total:
            percentage = (downloaded / total) * 100
            speed = d.get('speed', 0)
            speed_str = format_size(speed) + '/s' if speed else 'N/A'

            eta = d.get('eta', None)
            eta_str = str(datetime.fromtimestamp(eta).strftime('%M:%S')) if eta else 'N/A'

            progress = f"\rProgress: {percentage:.1f}% | Speed: {speed_str} | ETA: {eta_str}"
            sys.stdout.write(progress)
            sys.stdout.flush()

def download_audio(url, output_path='downloads'):
    """
    Download a YouTube video with specified quality using yt-dlp.

    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the downloaded video
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Configure yt-dlp options
        ydl_opts = {
            "extract_audio": True,
            "format": "bestaudio",
            'progress_hooks': [progress_hook],
            'outtmpl': os.path.join(output_path, '%(title)s.mp3'),
        }

        print("Fetching video information...")


        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title=info_dict['title']

            return f"{output_path}/{video_title}.mp3"

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify the video URL is correct and accessible")
        print("3. Try updating yt-dlp: `pip install --upgrade yt-dlp`")
        print("4. Make sure the video isn't private or age-restricted")
        print("5. If you want access to all quality options, run `choco install FFmpeg`")