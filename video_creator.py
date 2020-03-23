from moviepy.editor import *
import bs4 as bs
import urllib.request
import requests
import os
import subprocess


print("Video Generator - Everton Colombo | 22/03/2020 Santarem-PA, Brazil")
keyword = input("Keyword: ")
keyword.replace(' ', '%20')
num_of_imgs = int(input("Num. of Images to download: "))

print("Searching for images...")
# source = urllib.request.urlopen(f"https://www.freeimages.com/search/{keyword}").read()
source = requests.get(f'https://www.google.com.br/search?hl=en&tbm=isch&sxsrf=ALeKk02WUw82w3gRa0tPbAcgpisPQ2rrpg%3A1584'
                      f'971124890&source=hp&biw=1302&bih=637&ei=dL14XuS0NP275OUPh4qo6Ak&q={keyword}&oq={keyword}&gs_l=i'
                      f'mg.3..0l10.2708.4298..5507...0.0..0.217.749.0j3j1......0....1..gws-wiz-img.......35i39.X6qseUun'
                      f'8BY&ved=0ahUKEwjkvoHH3bDoAhX9HbkGHQcFCp0Q4dUDCAY&uact=5')
if source.status_code != 200:
    print('Err')
    exit(1)
soup = bs.BeautifulSoup(source.text, 'html.parser')
img_links = [x.get('src') for x in soup.find_all('img')]
del(img_links[0:4])
del(img_links[-1:-16:-1])
print(img_links)
# print(imgs)
if len(img_links) == 0:
    print("No Content Found")
    exit(0)
print("Found {0}/20 Images!".format(len(img_links)))
print('Downloading images...')
_ = 0
paths = []
for link in img_links:
    _ += 1
    if _ > num_of_imgs:
        break
    print(f"Downloading image No.: {_}")
    paths.append(f'images/{keyword}-{_}.png')
    urllib.request.urlretrieve(link, paths[-1])

# CREATING CLIP :
clip = concatenate_videoclips([ImageClip(m).set_duration(2) for m in paths], method='compose')
clip.write_videofile(f"{keyword}.mp4", fps=24)

# DELETE IMAGES:
print("Cleaning up...")
for img in paths:
    os.remove(img)

subprocess.call(["xdg-open", f"{keyword}.mp4"])
