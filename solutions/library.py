from pathlib import Path
import yt_dlp
import csv


def download_video(url):
    # download one video
    Path("videos").mkdir(exist_ok=True)

    # Save inside videos/ using the video title as the filename
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download([url])

def load_urls_from_csv(videos_file):
    urls = []
    with open(videos_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            urls.append(row["url"])
    return urls

def write_time_to_report(report_file, serial_time):
    with open(report_file, "a", newline="") as file:
        file.write(str(serial_time))
        print(f"{report_file} successfully updated.")