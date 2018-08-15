from bs4 import BeautifulSoup
import urllib
import urllib.request as urllib2
from PIL import Image
import requests
from io import BytesIO

def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')

def make_url_str(query):
    arr = query.split(" ")
    print(arr)
    query='+'.join(arr)
    print(query)
    return query


def get_filenames(dir_name):
    return [fname
            for fname in os.listdir(dir_name)
            if fname.endswith('.mp3')]

def save_gif(url, fname):
    f = open(fname,'wb')
    im = urllib.request.urlopen(url, timeout=1000).read()
    f.write(im)
    f.close()

def geturl(url,folder_name, i, ext):
    if ext:
        try:
            print("ok")

            if ext.count("?") > 0:
                ext = ext[:ext.index('?')]
                print('truncate ext', ext)
            fname = "{}/{}{}".format(folder_name, i,ext)
            response = requests.get(url)
            im_data = BytesIO(response.content)
            if ext == ".gif":
                save_gif(url, fname)
            else:
                im = Image.open(im_data)
                # im.load()
                # im.verify()
                width = im.size[0]
                if width > 1280:
                    basewidth = 1280
                    wpercent = (basewidth/float(im.size[0]))
                    hsize = int((float(im.size[1])*float(wpercent)))
                    im = im.resize((basewidth,hsize), Image.ANTIALIAS)
                im.save(fname)


        except OSError as err:
            print('not a valid img file', err)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print('Other exception', e)

def delete_old(folder_name):
    for the_file in os.listdir(folder_name):
        file_path = os.path.join(folder_name, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def make_url_str(query):
    whitelist = set('abcdefghijklmnopqrstuvwxy ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    query = ''.join(filter(whitelist.__contains__, query))
    arr = query.split()
    query='+'.join(arr)
    return query
