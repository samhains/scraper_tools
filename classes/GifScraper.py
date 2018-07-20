from classes.BaseThread import BaseThread as Parent
from utility  import *
import numpy as np
import random
import time
import giphypop
from multiprocessing.dummy import Pool as ThreadPool

class GifScraper(Parent):
    def __init__(self, max_images):
        Parent.__init__(self)
        self.max_images = max_images
        self.pool = ThreadPool(10)

    def _gif_scrape(self, query, folder_name):
        g = giphypop.Giphy()
        result_urls = [x.media_url for x in g.search(query)][:self.max_images]
        print("received  this number results:", len(result_urls))
        n_urls = len(result_urls)
        types_arr = np.full(n_urls, ".gif")
        hash = random.getrandbits(128)
        folder_name_arr = np.full(n_urls, folder_name)
        i_arr =  range(0, n_urls)
        r = random.randint(1111,9999)
        i_arr = ["{}_{}".format(i, r) for i in i_arr]
        results = self.pool.starmap(geturl, zip(result_urls, folder_name_arr, i_arr, types_arr))

    def scrape(self, query, output_dir):
        self.target = self._gif_scrape
        self.query = query
        self.output_dir = output_dir
        self.args = [self.query, self.output_dir]
        self.start()
