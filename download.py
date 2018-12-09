import pytumblr
import os
import urllib
import re
from tumblr_keys import *
import codecs

client = pytumblr.TumblrRestClient(
    consumer_key,
    consumer_secret,
    token_key,
    token_secret
)

# Get the info on the user
info = client.info()

# Get the user name and number of likes
dirname = info['user']['name']
blogurl = info['user']['blogs'][0]['url']
likescount = int(info['user']['likes'])

# Create directory
if not os.path.exists(dirname):
    os.makedirs(dirname)

# Number of likes to fetch in one request. Should be no more than 50.
# Currently the Tumblr API returns no more than 1000 likes
limit = 30

# Number of files downloaded
count = 0

# Number of posts downloaded
posts = 0

# Likes required offset, i.e. start from which like. If too many likes need to be download, 
# we should run this script for several times and change offset. 
offset = 0

# Number of requires
pages = 0

# If more than 1000 files were downloaded, set this flag False
downloadFlag = True

# Display the number of likes
print("Tumblr user {0} has {1} likes".format(dirname, likescount))
print("Fetch approximately {0} likes in one page.".format(limit))
print("Current offset: {0}.".format(offset))

def CheckDownloadLimitation():
	if count>=1000:
		print("Exceed the limitation of download! Current offset is {0}. Please run this script 24 hours later and change the offset to {0}.".format(offset))
		return False
	else:
		return True

def download_photo(liked):
    global downloadFlag
    global count
    photos = liked["photos"]
    # Parse photos
    for photo in photos:
        if not downloadFlag:
            break
        # Get the original size
        url = photo["original_size"]["url"]
        imgname = url.split('/')[-1]

        # Create a unique name
        filename = dirname + "/" + imgname

        # Check if image is already on local disk
        if (os.path.isfile(filename)):
            print("File already exists : " + imgname)
        else:
            if CheckDownloadLimitation():
                print("Downloading " + imgname + " from " + liked["blog_name"])
                urllib.request.urlretrieve(url, filename)
                count += 1
            else:
                downloadFlag = False
                break           

def download_video(liked):
    global downloadFlag
    global count
    url = liked["video_url"]
    vidname = url.split('/')[-1]
    filename = dirname + "/" + vidname
    if (os.path.isfile(filename)):
        print("File already exists : " + vidname)
    else:
        if CheckDownloadLimitation():
            print("Downloading " + vidname + " from " + liked["blog_name"])
            urllib.request.urlretrieve(url, filename)
            count += 1
        else:
            downloadFlag = False
 

def download_other(liked):
    global downloadFlag
    global count
    # Create a unique name. Write the content to a html file.
    filename = dirname + "/" + liked["blog_name"] + "-" + str(liked["id"]) + ".html"
    with codecs.open(filename, "w", "utf-8") as ds:
        ds.write('<!doctype html><html><head><meta http-equiv="content-type" content="text/html; charset=utf-8"><title></title></head><body>')
        ds.write(liked["body"])
        ds.write('</body></html>')
    # Download the images and videos in this post.
    pattern = re.compile(r'(https?://)([\w\/\-\.]+)(bmp|jpg|tiff|gif|png|mp4)')
    list_raw = re.findall(pattern, liked["body"])
    list_img_url = [''.join(i) for i in list_raw]
    newlist = []
    for item in list_img_url:
        if item not in newlist:
            newlist.append(item)
    for imgItem in newlist:
        imgname = imgItem.split('/')[-1]
        filename = dirname + "/" + imgname
        if (os.path.isfile(filename)):
            print("File already exists : " + imgname)
        else:
            if CheckDownloadLimitation():
                print("Downloading " + imgname + " from " + liked["blog_name"])
                urllib.request.urlretrieve(imgItem, filename)
                count += 1
            else:
                downloadFlag = False
                break

maxPages = 100

while(True):
    likes = client.likes(offset=offset, limit=limit)["liked_posts"]
    if len(likes)==0 :
        break
    if pages>maxPages:
        print("Reach the max page.")
        break
    offset = offset+len(likes)
    print("{0} likes in Page {1}, {2} totally.".format(len(likes), pages, offset))
    pages = pages+1
    for idx, liked in enumerate(likes):
        print("Processing like #{0}".format(offset-len(likes)+idx))
        posts += 1
        if not downloadFlag:
            posts -= 1
            break
        if "photos" in liked:
            print("This like is a photo post.")
            download_photo(liked)
        elif "video_url" in liked:
            print("This like is a video post.")
            download_video(liked)
        elif "body" in liked:
            print("This like is a {0} post.".format(liked["type"]))
            download_other(liked)
        else:
            # If not a photo or a video, dump the JSON
            with open(str(liked["id"]) + "-" + str(liked["blog_name"]) + ".json", "w") as f:
                json.dump(liked, f)
        print("Downloaded {0} items totally till this post.".format(count)) 

print("{0} pages ({1} posts, {2} items) were fetched. Current offset {3}".format(pages, posts, count, offset))