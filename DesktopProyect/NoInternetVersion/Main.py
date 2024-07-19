import subprocess
import os

def download_single_audio(url, quality='high'):
    quality_map = {
        'low': 'worstaudio',
        'medium': 'bestaudio[abr<=128k]',
        'high': 'bestaudio'
    }

    selected_quality = quality_map.get(quality, 'bestaudio')

    # Create the output directory if it doesn't exist
    output_dir = 'audios'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Downloading from {url} with quality {quality}...")

    command = [
        'yt-dlp',
        '-f', selected_quality,
        '--extract-audio',
        '--audio-format', 'mp3',
        '--output', os.path.join(output_dir, '%(title)s.%(ext)s'),
        url
    ]

    subprocess.run(command)

    print("Download and conversion complete.")


def download_playlist_audio(url, quality='high'):
    quality_map = {
        'low': 'worstaudio',
        'medium': 'bestaudio[abr<=128k]',
        'high': 'bestaudio'
    }

    selected_quality = quality_map.get(quality, 'bestaudio')

    # Create the output directory if it doesn't exist
    output_dir = 'audios'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Downloading playlist from {url} with quality {quality}...")

    command = [
        'yt-dlp',
        '--yes-playlist',
        '-f', selected_quality,
        '--extract-audio',
        '--audio-format', 'mp3',
        '--output', os.path.join(output_dir, '%(playlist)s/%(title)s.%(ext)s'),
        url
    ]

    subprocess.run(command)

    print("Download and conversion of playlist complete.")

# Example usage:
url = input("Enter the YouTube URL or Playlist URL: ")
quality = input("Enter the quality (low, medium, high): ")

if 'playlist' in url:
    download_playlist_audio(url, quality)
else:
    download_single_audio(url, quality)
