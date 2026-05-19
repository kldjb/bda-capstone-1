from pathlib import Path
import yt_dlp
import csv


def get_video_metadata(ydl, url):
    # Extract metadata from videos
    info = ydl.extract_info(url, download=False)

    return {
        "Title": info.get("title"),
        "Duration": info.get("duration"),
        "Uploader": info.get("uploader"),
        "Views": info.get("view_count"),
        "Extension": info.get("ext"),
        "URL": url,
    }

def download_video(url):
    # download one video
    Path("videos").mkdir(exist_ok=True)

    # Save inside videos/ using the video title as the filename
    ydl_options = {
        "outtmpl": "videos/%(title)s.%(ext)s",
        "socket_timeout": 30,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])

            # Extract video metadata
            return get_video_metadata(ydl, url)
    
    except Exception as error:
        print ({
            "url": url,
            "status": "failed",
            "error": str(error),
        })

        return {
        "Title": "",
        "Duration": "",
        "Uploader": "",
        "Views": "",
        "Extension": "",
        "URL": url,
        }

def load_urls_from_csv(videos_file):
    urls = []
    with open(videos_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            urls.append(row["url"])
    return urls

def write_time_to_report(report_file, elapsed_time):
    with open(report_file, "a", newline="") as file:
        file.write(str(elapsed_time))
        print(f"{report_file} successfully updated.")

def calculate_time_diff(report_file, parallel_time):
    with open(report_file, newline="") as readfile:
        report = readfile.readlines()
        for i, row in enumerate(report):
            if "Serial" in row:
                serial_time = report[i+2].split(":")[1].strip().strip("\r\n")

    # Write speed difference
    with open(report_file, "a", newline="") as writefile:
        speed_diff = float(serial_time) - parallel_time
        speed_diff_percent = round((speed_diff/ float(serial_time)), 2)
        writefile.write(f"{speed_diff_percent}%")
        print(f"Speed difference: {round(speed_diff_percent, 2)}%")