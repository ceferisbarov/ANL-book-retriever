import os
import ocrmypdf

import requests
from bs4 import BeautifulSoup


def get_url_parameters(url):
    """
    @return:
    This function returns three parameters we need to iterate through URLs of a single book:
    1. base_url, which is same everywhere throughout the website,
    2. bibib, which is the book id, hence same throughout the book, and
    3. page_count, which will be used to construct a while loop (we need to know when to stop).
    It also returns book_title, which we will use to name the folder and the PDF file.

    @param url: URL
    @type url: str

    """
    # TODO: Rewrite this function with help of BeautifulSoup4
    start_bibid = url.find('bibid')
    base_url = url[:start_bibid]

    start_vtls = url.find('vtls')
    if start_vtls == -1:
        start_bibid = url.find('bibid')
        start_pno = url.find('&pno')
        bibid = url[start_bibid+6:start_pno]
    else:
        bibid = url[start_vtls + 4:]

    page_content = requests.get(url).text
    start_last_page_params = page_content.find('last_page_params')
    start_page_count = page_content.find('pno', start_last_page_params, start_last_page_params + 100)
    start_page_count_ending = page_content.find('";', start_last_page_params, start_last_page_params + 100)
    page_count = int(page_content[start_page_count + 4:start_page_count_ending])
    length = len('<h2 class="book-title font-f-book-reg">')
    start_book_title = page_content.find('<h2 class="book-title font-f-book-reg">')
    start_book_title_ending = page_content.find('</h2>')
    book_title = page_content[start_book_title + length:start_book_title_ending]
    return base_url, bibid, page_count, book_title


def save_images(url, directory, pno):
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    images = soup.findAll('img')
    
    download_images(images, directory, pno)


# CREATE FOLDER
def folder_create(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

    except Exception as e:
        print(e)


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, directory, pno):
    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"Total {len(images)} image(s) found in this page!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag ,Fetch image Source URL

            # 1.data-srcset
            # 2.data-src
            # 3.data-fallback-src
            # 4.src

            # Here we will use exception handling

            # first we will search for "data-srcset" in img tag
            try:
                # In image tag ,searching for "data-srcset"
                image_link = image["data-srcset"]

            # then we will search for "data-src" in img 
            # tag and so on..
            except:
                try:
                    # In image tag ,searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag ,searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag ,searching for "src"
                            image_link = image["src"]

                        # if no Source URL found
                        except:
                            print("No source URL found")
                            return 0

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                r = requests.get('http://web2.anl.az:81/read/' + image_link).content
                try:

                    # possibility of decode
                    r = str(r, 'utf-8')

                except UnicodeDecodeError:

                    # After checking above condition, Image Download start
                    with open(f"{directory}/images{pno}-{i+1}.jpg", "wb+") as f:
                        f.write(r)

                    if os.path.isfile(f"{directory}/images{pno}-{i}.jpg"):
                        print("Downloaded {i+1} image in this page.")
                    # counting number of image downloaded
                    count += 1
            except Exception as e:
                print(e)
