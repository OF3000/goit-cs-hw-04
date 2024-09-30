import threading
import time
from collections import defaultdict
from pathlib import Path


def search_in_file(file_path, keywords, results):

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"error reading file {file_path}: {e}")


def thread_task(files, keywords, results):
    for file in files:
        search_in_file(file, keywords, results)


def main_threading(file_paths, keywords):
    # TODO Додати вимір часу виконання
    start_time = time.time()

    num_threads = 4 
    threads = []
    results = defaultdict(list)
    if len(file_paths) < num_threads:
        th_files = 1
        num_threads = len(file_paths)
    else:
        th_files = len(file_paths) // num_threads

    amount =  len(file_paths)

    for i in range(num_threads):
        fst_file = len(file_paths) - amount
        lst_file = fst_file + th_files

        amount -= th_files
        if num_threads - i - 1 != 0:
            th_files = amount // (num_threads - i - 1)
        srch_files = file_paths[fst_file:lst_file]

        thread = threading.Thread(target = thread_task, args = (srch_files, keywords, results))



        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    finish_time = time.time() - start_time
    print(f"execution time: {finish_time}")

    return results


if __name__ == '__main__':

    file_paths = list(Path("input").glob("*.txt"))
    print(f"File paths: {file_paths}\n")
    keywords = ["Lorem","risus","sit"]
    results = main_threading(file_paths, keywords)
    print(results)
