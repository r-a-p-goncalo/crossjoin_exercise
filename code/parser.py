import csv
from datetime import datetime
import os
import re
from thread_specific import get_thread_category_from_name, is_custom_call, interpret_single_thread_info

OUTPUT_DIRECTORY = "data\\interpreted\\csv"
THREAD_TUMPS_DIRECTORY = "data\\crossjoin_td_test"

GENERAL_THREAD_DUMP_NAME = "thread_dump_headers"
GENERAL_THREAD_DUMP_ROWS_BASIC = ["filename", "service_name", "service_role", "kubernetes_hash", "pod_suffix", "timestamp"]

GENERAL_THREAD_DUMP_ROWS = [*GENERAL_THREAD_DUMP_ROWS_BASIC,
                    "thread_count"]

TRHEAD_SPECIFIC_DUMP_NAME = "thread_specific"
THREAD_SPECIFIC_DUMP_ROWS = [*GENERAL_THREAD_DUMP_ROWS_BASIC,
                             "thread_name", "thread_category", "thread_subcategory","thread_id", "status", "cpu_ms", "time_elapsed_s", "last_call", "last_custom_call"]






def print_threads(thread_specific_texts):
    for i, thread in enumerate(thread_specific_texts):
        print(f"========== {i} ==========")
        print(thread.splitlines()[0])

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

def interpret_thread_dump_info_in_text(thread_dump_text_header : str) -> dict:
    '''
    Interprets general data regarding the specific thread dump
    '''

    info = {}

    # Number of Java threads
    match = re.search(
        r'length=(\d+)',
        thread_dump_text_header
    )

    if match:
        info["thread_count"] = int(match.group(1))

    return info



def separate_thread_text(thread_dump_text : str):

    # First thread always starts with a quoted thread name
    match = re.search(r'^"', thread_dump_text, flags=re.MULTILINE)

    if match is None:
        return thread_dump_text, []

    header = thread_dump_text[:match.start()].strip()

    thread_text = thread_dump_text[match.start():]

    # Split whenever a new thread begins
    thread_specific_texts = re.split(
        r'(?=^".*")',
        thread_text,
        flags=re.MULTILINE
    )

    thread_specific_texts = [
        thread.strip()
        for thread in thread_specific_texts
        if thread.strip()
    ]

    return header, thread_specific_texts

def create_thread_specific_dumps_csv():

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    output_csv = os.path.join(OUTPUT_DIRECTORY, f"{TRHEAD_SPECIFIC_DUMP_NAME}.csv")

    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(THREAD_SPECIFIC_DUMP_ROWS) # this is the header

    return output_csv

def create_thread_dumps_csv():

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    output_csv = os.path.join(OUTPUT_DIRECTORY, f"{GENERAL_THREAD_DUMP_NAME}.csv")

    with open(output_csv, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(GENERAL_THREAD_DUMP_ROWS) # this is the header

    return output_csv

def main():
    '''
    The main function
    '''

    # directory where thread_dumps are stored
    thread_dumps_directory = THREAD_TUMPS_DIRECTORY

    # thread_dump_files
    thread_dump_file_names = [
        file
        for file in os.listdir(thread_dumps_directory)
        if os.path.isfile(os.path.join(thread_dumps_directory, file))
    ]

    thread_dump_csv = create_thread_dumps_csv()
    thread_specific_csv = create_thread_specific_dumps_csv()

    with open(thread_dump_csv, "a", newline="", encoding="utf-8") as csv_file:
        general_thread_dump_writer = csv.DictWriter(csv_file, GENERAL_THREAD_DUMP_ROWS)

        

        for thread_dump_file in thread_dump_file_names:

            interpreted_name = interpret_thread_dump_name(thread_dump_file)

            file_path = os.path.join(thread_dumps_directory, thread_dump_file)
            with open(file_path, "r", encoding="utf-8") as f:
                text_in_file = f.read()

            header_text, thread_specific_texts = separate_thread_text(text_in_file)

            thread_dump_info = interpret_thread_dump_info_in_text(header_text)

            assert thread_dump_info["thread_count"] <= len(thread_specific_texts), (f"Thread count mismatch: header={thread_dump_info['thread_count']}, parsed={len(thread_specific_texts)}")

            general_thread_dump_writer.writerow({"filename" : thread_dump_file, **interpreted_name, **thread_dump_info})

            with open(thread_specific_csv, "a", newline="", encoding="utf-8") as thread_specific_csv_file:
                specific_thread_dump_writer = csv.DictWriter(thread_specific_csv_file, THREAD_SPECIFIC_DUMP_ROWS)
        
                for thread_specific_text in thread_specific_texts:

                    interpreted_thread_info = interpret_single_thread_info(thread_specific_text)

                    specific_thread_dump_writer.writerow({"filename" : thread_dump_file, **interpreted_name, **interpreted_thread_info})





if __name__ == '__main__':
    main()