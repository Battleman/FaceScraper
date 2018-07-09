#!/usr/local/bin/python
# coding: latin-1
"""
Author: Olivier Cloux
Date: 23.06.2018

Goal: Download images of people@epfl according to their scipers
"""

import random
import time
import threading
from pprint import pprint
# from io import BytesIO

import requests
# from PIL import Image

MOCK = True
NUM_THREADS = 10
BASEPAGE = "https://people.epfl.ch/cgi-bin/people/getPhoto?id="
FACES_FOLDER = "/media/battleman/DATA/Documents/" + \
    "Programming/Python/FaceScraper/faces/{}.jpeg"


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

    def run(self):
        for sciper in self.scipers_list:
            req = requests.get(BASEPAGE+str(sciper))
            if req.status_code != 200:
                print("Error with sciper {}, status is {}".format(
                    sciper, req.status_code))
                continue
            if req.content and 'html' not in str(req.content[:30]):
                filename = FACES_FOLDER.format(sciper)
                pprint("Thread {}, saved sciper {}".format(
                    self.thread_id, sciper))
                url = str(req.content)[12:-3]
                img_req = requests.get("https://people.epfl.ch"+url)
                with open(filename, 'wb') as image:
                    image.write(img_req.content)
            else:
                pprint("Thead {}, no result found for sciper {}".format(
                    self.thread_id, sciper))


def main():
    """
    Takes all scipers and download
    """
    start_time = time.time()
    if MOCK:
        all_scipers = list(random.sample(range(100000, 400000), 200))
    else:
        all_scipers = list(range(100000, 400000))
    sublists = list(chunks(all_scipers, len(all_scipers)//NUM_THREADS))
    threads_list = []
    for num_thread in range(NUM_THREADS):
        thread = MyThread(sublists[num_thread], num_thread)
        thread.start()
        threads_list.append(thread)

    for thread in threads_list:
        thread.join()

    end_time = time.time()
    pprint("Spent time with {} threads: {}".format(
        NUM_THREADS, end_time-start_time))


if __name__ == "__main__":
    main()
