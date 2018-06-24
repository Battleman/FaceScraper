#!/usr/local/bin/python
# coding: latin-1
"""
Author: Olivier Cloux
Date: 23.06.2018

Goal: Download images of people@epfl according to their scipers
"""

import random
import time
from io import BytesIO

import requests
from PIL import Image

BASEPAGE = "https://people.epfl.ch/cgi-bin/people/getPhoto?id="
FACES_FOLDER = "/media/battleman/DATA/Documents/" + \
    "Programming/Python/FaceScraper/faces/{}.jpeg"

SCIPERS = list(range(100000, 400000))

for s in random.sample(SCIPERS, 100):  # sample of 100 random scipers
    req = requests.get(BASEPAGE+str(s))
    if req.status_code != 200:
        print("Error with sciper {}, status is {}".format(s, req.status_code))
        continue
    if req.content and 'html' not in str(req.content[:30]):
        filename = FACES_FOLDER.format(s)
        print(filename)
        i = Image.open(BytesIO(req.content))
        i.save(filename)
        i.close()

    time.sleep(random.randint(0, 5))
