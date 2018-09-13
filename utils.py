import tqdm
import os.path
from urllib.request import urlretrieve




def file_downloader(dowload_url, filename):
    """Downloads a url file and shows progress of the file.

    Args:
        download_url(str): File to download.
        filename(str): Place to store the file to download.

    Returns:
        bool: True for success, False otherwise.

    """
    def __hook(**kwargs):
        t = tqdm.tqdm(**kwargs)
        last_b = [0]
        def inner(b=1, bsize=1, tsize=None, close=False):
            if close:
                t.close()
                return
            t.total = tsize
            t.update((b - last_b[0]) * bsize) # manually update the progressbar
            last_b[0] = b
        return inner
    try:
        hook = __hook(unit='B', unit_scale=True, leave=True, miniters=1,
                    desc=filename) # all optional kwargs

        #Download function
        urlretrieve(dowload_url,
                    filename=filename, reporthook=hook, data=None)
        hook(close=True)
    except:
        print("\nFail to download: {0}".format(dowload_url))
        return False

    return True


def download_datasets(urls, prefix=''):
    for url in urls:
        #last element in the url
        filename = prefix + url.split("/")[-1]
        if os.path.isfile(filename):
            print("File: {0}, in cache".format(filename))
            continue
        file_downloader(url, filename)
