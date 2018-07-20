from classes.BaseThread import BaseThread as Parent
import giphypop
from utility  import *
import numpy as np
import random
import time
import json
import os
from multiprocessing.dummy import Pool as ThreadPool

class GoogleScraper(Parent):
    def __init__(self, max_images):
        Parent.__init__(self)
        self.max_images = max_images
        self.pool = ThreadPool(10)

    def _google_scrape(self, query, folder_name):
        query = make_url_str(query)
        header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
        soup = get_soup(url,header)
        ActualImages=[] # contains the link for Large original images, type of  image
        for a in soup.find_all("div",{"class":"rg_meta"}):
            link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
            ActualImages.append((link,Type))
        random.shuffle(ActualImages)
        print("scraping", query, "into", folder_name )
        result_urls = [image_data_tuple[0] for image_data_tuple in ActualImages[:self.max_images]]
        result_exts =  [os.path.splitext(urls)[1] for urls in result_urls]
        result_urls_png = [image_data_tuple[0] for image_data_tuple in ActualImages[:self.max_images] if image_data_tuple[0].endswith(".png")]
        n_urls = len(result_urls)
        folder_name_arr = np.full(n_urls, folder_name)
        i_arr =  range(0, n_urls)
        r = random.randint(1111,9999)
        i_arr = ["{}_{}".format(i, r) for i in i_arr]
        results = self.pool.starmap(geturl, zip(result_urls, folder_name_arr, i_arr, result_exts))


    def scrape(self, query, output_dir):
        self.target = self._google_scrape
        self.query = query
        self.output_dir = output_dir
        self.args = [self.query, self.output_dir]
        self.start()
