__author__ = 'Michael'

import argparse
import re


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='U', help='Comic page URL, with page and chapter/volume numbers substituted.')

    args = parser.parse_args()

    split_url(args.url)


# Input url of a similar form to 'http://www.xxx/yyy/{vvv}/[j].jpg' where v and p are placeholders indicating the number of digits in the volume/chapter and page numbers.
# Example: http://www.casualvillain.com/Unsounded/comic/ch{cc}/pageart/ch{cc}_[pp].jpg
def split_url(url):
    if not re.match('http(s)?://', url):
        print("Url must begin with http:// or https://")
        exit()

    p_result = re.search('\[(p)+\]', url)
    if not p_result:
        print("Url must contain a page number placeholder")
        exit()
    else:
        num_page_digits = len(p_result.group(0)) - 2
        print("Number of page digits: " + str(num_page_digits))

    c_result = re.search('\{(c)+\}', url)
    if c_result:
        num_chapter_digits = len(c_result.group(0)) - 2
        print("Number of chapter digits: " + str(num_chapter_digits))

    v_result = re.search('\{(v)+\}', url)
    if v_result:
        num_volume_digits = len(v_result.group(0)) - 2
        print("Number of volume digits: " + str(num_volume_digits))

if __name__ == "__main__":
    main()