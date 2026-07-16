import csv
from datetime import datetime
import os

def interpret_thread_dump_name(thread_dump_name : str) -> dict[str, any]:
        
    base_name = os.path.splitext(thread_dump_name)[0]

    pod_name, timestamp = base_name.rsplit("_", 1)

    pod_parts = pod_name.split("-")

    pod_suffix = pod_parts[-1]
    kubernetes_hash = pod_parts[-2]
    service_role = pod_parts[-3]
    service_name = "-".join(pod_parts[:-3])

    timestamp = datetime.strptime(timestamp, "%Y%m%d%H%M%S")

    return {
        "service_name": service_name,
        "service_role": service_role,
        "kubernetes_hash": kubernetes_hash,
        "pod_suffix": pod_suffix,
        "timestamp": timestamp,
    }

def create_thread_dumps_csv():

    # Output directory and CSV
    output_directory = "data\\interpreted"
    os.makedirs(output_directory, exist_ok=True)

    output_csv = os.path.join(output_directory, "thread_dumps.csv")

    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Header
        writer.writerow([
            "file_name",
            "service_name",
            "service_role",
            "kubernetes_hash",
            "pod_suffix",
            "timestamp",
        ])

    return output_csv

def main():
    '''
    The main function
    '''

    # directory where thread_dumps are stored
    thread_dumps_directory = "data\\crossjoin_td_test"

    

    # thread_dump_files
    thread_dump_file_names = [
        file
        for file in os.listdir(thread_dumps_directory)
        if os.path.isfile(os.path.join(thread_dumps_directory, file))
    ]

    output_csv = create_thread_dumps_csv()

    with open(output_csv, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        for thread_dump_file in thread_dump_file_names:
        
            interpreted = interpret_thread_dump_name(thread_dump_file)
    
        
    
    
            writer.writerow([
                    thread_dump_file,
                    interpreted["service_name"],
                    interpreted["service_role"],
                    interpreted["kubernetes_hash"],
                    interpreted["pod_suffix"],
                    interpreted["timestamp"].isoformat(),
                ])
    
            print(f"{thread_dump_file} -> {interpreted}")
    





if __name__ == '__main__':
    main()