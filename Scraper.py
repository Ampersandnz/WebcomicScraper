import urllib.request
import os
import argparse
import re
import subprocess

from pathlib import Path
from multiprocessing.pool import Pool

__author__ = 'Michael'
# Thanks to http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

webcomic_name = None
subset_type = None
num_subsets = None
pages_per_subset = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='U', help='Comic page URL, with page and chapter/volume numbers substituted.')
    parser.add_argument('name', metavar='N', help='Webcomic name.')
    parser.add_argument('subsets', metavar='C', help='Number of chapters/volumes.')
    parser.add_argument('pages', metavar='P', help='Maximum pages in a chapter.')

    args = parser.parse_args()

    global webcomic_name
    webcomic_name = args.name

    global num_subsets
    num_subsets = int(args.subsets)

    global pages_per_subset
    pages_per_subset = int(args.pages)

    url_as_list = split_url(args.url)

    for i in range(1, num_subsets + 1):
        download_dir = Path(os.getcwd() + "/" + webcomic_name)

        if not download_dir.exists():
            download_dir.mkdir()
        os.chdir(download_dir.name)

        global subset_type

        urls = []
        for j in range(1, pages_per_subset + 1):

            numbered_url = ''

            for sub_url in url_as_list:
                if re.match('^p+$', sub_url):
                    numbered_url += (str(j).zfill(len(sub_url)))
                elif re.match('^c+$', sub_url):
                    subset_type = "Chapter"
                    numbered_url += (str(i).zfill(len(sub_url)))
                elif re.match('^v+$', sub_url):
                    subset_type = "Volume"
                    numbered_url += (str(i).zfill(len(sub_url)))
                else:
                    numbered_url += sub_url

            print("URL " + numbered_url + " added to queue.")

            urls.append(numbered_url)

        # 12 is larger than any reasonable number of CPU cores, and a direct multiple of the most common ones.
        with Pool(12) as p:
            p.map(download_file, urls)

        if subset_type is None:
            rar_name = ("\"" + webcomic_name + ".cbr\"")
        else:
            rar_name = ("\"" + subset_type + " " + str(i) + ".cbr\"")

        # Move downloaded files into a .cbr archive.
        try:
            subprocess.call('rar m -m0 ' + rar_name + " *.jpg")

            print()

            if subset_type is None:
                print('Successfully compressed ' + webcomic_name + ' to .cbr archive.')
            else:
                print('Successfully compressed ' + subset_type + " " + i + ' to .cbr archive.')
        except OSError:
            print('Rar is not installed on this machine.')
    print('Finished downloading and archiving all files.')


def download_file(url):
    filename = url.split("/")[-1]

    try:
        urllib.request.urlretrieve(url, filename)
    except:
        pass

    if os.path.exists(filename):
        if os.path.getsize(filename) < 25 * 1024:
            os.remove(filename)


# Input url of a similar form to 'http://www.website/{vvv}/{p}.jpg',
# where v and p are placeholders indicating the number of digits in the volume/chapter and page numbers.
# Example: http://www.casualvillain.com/Unsounded/comic/ch{cc}/pageart/ch{cc}_{pp}.jpg
def split_url(url):

    if not re.match('http(s)?://', url):
        print("Url must begin with http:// or https://")
        exit()

    if not re.search('\.(jpg|jpeg|png|gif)$', url):
        print("Url must end with .jpg, .jpeg, .png, .gif (must be a direct link to the image file).")
        exit()

    if not re.findall('\{p+\}', url):
        print("Url must contain a page number placeholder!")
        exit()

    return re.split("[\{\}]", url)

if __name__ == "__main__":
    main()