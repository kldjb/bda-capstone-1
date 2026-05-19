import csv
import time
from multiprocessing import Pool
from library import (
    calculate_time_diff,
    download_video,
    load_urls_from_csv,
    write_time_to_report,
)


if __name__ == "__main__":
    # Start timer
    start = time.perf_counter()

    # Load videos
    videos_file = r"data/video_urls.csv"
    urls = load_urls_from_csv(videos_file)

    # Serial download videos
    serial_download = False
    if serial_download:
        for url in urls:
            download_video(url)

    # Parallel download videos
    with Pool() as pool:
        metadata_rows = pool.map(download_video, urls)

    # Save metadata rows
    metadata_path = "data/video_metadata.csv"
    with open(metadata_path, "w", newline="") as file:
        fieldnames = [
            "Title", "Duration", "Uploader", "Views", "Extension", "URL"
            ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(metadata_rows)
        print(f"Metadata successfully saved to {metadata_path}.")

    # End timer
    end = time.perf_counter()

    # Calculate elapsed time
    elapsed = end - start
    parallel_time = round(elapsed, 2)
    print(f"Parallel execution: {parallel_time}")

    # Write time to report
    report_file = r"reports/sequential_report.md"
    write_to_report = False
    if write_to_report:
        write_time_to_report(report_file, round(elapsed, 2))
    
    # Calculate time difference between serial and parallel
    calc_time_diff = False
    if calc_time_diff:
        calculate_time_diff(report_file, parallel_time)


    