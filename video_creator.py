from moviepy.editor import *
import bs4 as bs
import urllib.request
import os
import subprocess


keyword = input("Keyword: ")
num_of_imgs = int(input("Num of Images to download: "))

print("Searching for images...")
source = urllib.request.urlopen(f"https://www.freeimages.com/search/{keyword}").read()
soup = bs.BeautifulSoup(source, 'html.parser')

img_links = [x.a.img.get('src') for x in soup.find_all('li', {"class": "item"})]

# print(imgs)
if len(img_links) == 0:
    print("No Content Found")
    exit(0)
print("Found {0}/90 Images!".format(len(img_links)))
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
