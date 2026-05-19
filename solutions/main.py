import time
from multiprocessing import Pool
from library import (
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
    # for url in urls:
    #     download_video(url)

    # Parallel download videos
    with Pool() as pool:
        results = pool.map(download_video, urls)

    # End timer
    end = time.perf_counter()

    # Calculate elapsed time
    elapsed = end - start
    parallel_time = round(elapsed, 2)
    print(f"Parallel execution: {parallel_time}")

    # Write time to report
    report_file = r"reports/sequential_report.md"
    # write_time_to_report(report_file, serial_time)
    
    # Calculate time difference between serial and parallel
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

    