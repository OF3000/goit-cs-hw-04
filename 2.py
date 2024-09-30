import multiprocessing
from collections import defaultdict
from pathlib import Path
import time


def search_in_file(file_path, keywords, results_queue):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results_queue.put((keyword, file_path))
    except Exception as e:
        print(f"error reading file {file_path}: {e}")





def process_task(files, keywords, results_queue):
    for file in files:
        search_in_file(file, keywords, results_queue)


def main_multiprocessing(file_paths, keywords):
    start_time = time.time()

    num_processes = 4 

    processes = []
    results_queue = multiprocessing.Queue()
    results = defaultdict(list)


    if len(file_paths) < num_processes:
        th_files = 1
        num_processes = len(file_paths)
    else:
        th_files = len(file_paths) // num_processes

    amount =  len(file_paths)


    for i in range(num_processes):

        fst_file = len(file_paths) - amount
        lst_file = fst_file + th_files


        amount -= th_files
        
        if num_processes - i - 1 != 0:
            th_files = amount // (num_processes - i - 1)

        srch_files = file_paths[fst_file:lst_file]

        process = multiprocessing.Process(target = process_task, args = (srch_files, keywords, results_queue))


        
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    while not results_queue.empty():
        keyword, file_path = results_queue.get()
        results[keyword].append(file_path)

    finish_time = time.time() - start_time
    print(f"execution time: {finish_time}")

    return results


if __name__ == '__main__':

    file_paths = list(Path("input").glob("*.txt"))
    print(f"File paths: {file_paths}\n")
    keywords = ["Lorem","risus","sit"]
    results = main_multiprocessing(file_paths, keywords)
    print(results)
