#!/usr/local/bin/python
# coding: utf-8
"""
Author: Olivier Cloux
Date: 23.06.2018

Goal: Download images of people@epfl according to their scipers
"""

import random
import time
import threading
from pprint import pprint
import requests
import csv

MOCK = False
NUM_THREADS = 10
BASEPAGE = "https://people.epfl.ch/cgi-bin/people/getPhoto?id="
FACES_FOLDER = "/storage/Documents/" + \
    "Programming/Python/FaceScraper/faces/"
SCIPERS_RANGE = range(160000, 350000)


def chunks(target, num):
    """Yield successive n-sized chunks from target."""
    if num == 0:
        yield target
    else:
        for i in range(0, len(target), num):
            yield target[i:i + num]


class MyThread(threading.Thread):
    """
    Subclass to threading.Thread for multithreading purpose.
    """

    def __init__(self, scipers_list, thread_id):
        super().__init__()
        self.scipers_list = scipers_list
        self.thread_id = thread_id
        self.active_images = set()

    def run(self):
        for sciper in self.scipers_list:
            req = requests.get(BASEPAGE+str(sciper))
            if req.status_code != 200:
                print("Error with sciper {}, status is {}".format(
                    sciper, req.status_code))
                continue
            if req.content and 'html' not in str(req.content[:30]):
                url = str(req.content)[12:-3]
                self.active_images.add((sciper, url))
                print("Thread {} sciper {} url {}".format(
                    self.thread_id, sciper, url
                ))

    def join(self):
        super().join()
        return self.active_images


def save_result(filename, data):
    with open(filename, 'a') as file:
        csv_out = csv.writer(file)
        # csv_out.writerow(['sciper', 'pic_url'])
        for row in data:
            csv_out.writerow(row)


def main():
    """
    Takes all scipers and download
    """
    start_time = time.time()
    if MOCK:
        all_scipers = [random.sample(SCIPERS_RANGE, 200)]
    else:
        all_scipers = list(chunks(SCIPERS_RANGE, len(SCIPERS_RANGE)//10))

    for subrange in all_scipers:
        print("Starting with {} threads from scipers {} to {}".format(
            NUM_THREADS, subrange[0], subrange[-1]
        ))
        sublists = list(chunks(subrange, len(subrange)//NUM_THREADS))
        threads_list = []
        for num_thread in range(NUM_THREADS):
            thread = MyThread(sublists[num_thread], num_thread)
            thread.start()
            threads_list.append(thread)

        all_active_scipers = set()
        for thread in threads_list:
            all_active_scipers = all_active_scipers.union(thread.join())
        save_result(FACES_FOLDER+"active_scipers.csv", all_active_scipers)
    end_time = time.time()
    pprint("Spent time with {} threads: {}".format(
        NUM_THREADS, end_time-start_time))


if __name__ == "__main__":
    main()
