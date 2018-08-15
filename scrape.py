import os, os.path
from utility import *
import time

from pythonosc import udp_client
import string
from classes.GifScraper import GifScraper
from classes.GoogleScraper import GoogleScraper

from pygame import mixer
import spacy_nlp
import threading
from pythonosc import udp_client
client = udp_client.SimpleUDPClient("localhost", 7400)
max_client = udp_client.SimpleUDPClient("localhost", 7499)


threadLock = threading.Lock()
ROBOT_SPEECH_ECHO_DELAY = 8
N_ECHO_WALKS = 3
N_GOOGLE_IMAGES = 100
N_GIFS = 10

TOGGLE_NLP = True
TOGGLE_SAVE = True

if TOGGLE_NLP:
    nlp_args = spacy_nlp.prepare_nlp()
    print("finished loading nlp models")

def scrape_line(query, dir_name):
    print("scraping", dir_name)
    query = query.strip().lower()
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    GoogleScraper(N_GOOGLE_IMAGES).scrape(query, dir_name)
    GifScraper(N_GIFS).scrape(query, dir_name)

#
# def robot_speech_echoes(speech_echoes_arr):
#     print("starting robot speech echoes")
#     for i in range(N_ECHO_WALKS):
#         sleep = i*ROBOT_SPEECH_ECHO_DELAY + ROBOT_SPEECH_ECHO_DELAY
#         line = speech_echoes_arr[i]
#         print("running on line", line)
#         client.send_message("/text", line)
#     print("robot echoes finish")


def run(line):
    line = line.rstrip(string.punctuation).strip().lower()
    dir_str = make_url_str(line)
    dir_name = "./images/"+dir_str
    scrape_line(line, dir_name)

line = "energy star refrigerator"
run(line)
if TOGGLE_NLP:
     speech_echoes_arr = spacy_nlp.sentencewalk(line, *nlp_args, N_ECHO_WALKS)
     print("performing echoes on ", speech_echoes_arr)
     for line in speech_echoes_arr:
         run(line)

