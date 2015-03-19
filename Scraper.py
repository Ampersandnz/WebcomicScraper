__author__ = 'Michael'
# Thanks to http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

import urllib.request
import os
from pathlib import Path
from multiprocessing.pool import Pool

# TODO: Allow users to specify webcomic name (folder it'll be saved in).
webcomic_name = "Unsounded"

# TODO: Allow users to specify whether subsets of the comic are called volumes or chapters.
subset_type = "Chapter"

# TODO: Allow users to specify how many subsets there are.
num_subsets = 11

# TODO: Allow users to specify how many pages the largest subset has.
pages_per_subset = 150

# TODO: Allow users to specify format of urls (does not allow comic title, only subset and page number.


def main():
    home = os.getcwd()
    for i in range(1, num_subsets + 1):
        download_dir = Path(os.getcwd() + "/" + webcomic_name)

        if not download_dir.exists():
            download_dir.mkdir()
        os.chdir(download_dir.name)

        urls = []
        for j in range(1, pages_per_subset + 1):
            url = str("http://www.casualvillain.com/Unsounded/comic/ch" + str(i).zfill(2) + "/pageart/ch" + str(i).zfill(2) + "_" + str(j).zfill(2) + ".jpg")
            urls.append(url)

        with Pool(12) as p:
            p.map(download_file, urls)

        # Move downloaded files into a .cbr archive.
        rar_name = ("\"Chapter " + str(i) + ".cbr\"")
        os.system('rar m -m0 ' + rar_name + " *.jpg")


def download_file(url):
    filename = url.split("/")[-1]

    try:
        urllib.request.urlretrieve(url, filename)
    except:
        pass

    if os.path.exists(filename):
        if os.path.getsize(filename) < 25 * 1024:
            os.remove(filename)


if __name__ == "__main__":
    main()