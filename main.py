import sys
import os
import urllib.request
import json
import shutil
import subprocess

url=sys.argv[1]
if not url.startswith("http"):
    url="https://"+url

if not "/p/" in url:
    print("Invaild post url")
    sys.exit()

url=sys.argv[1].split("?")[0]
media_id=url.split("/p/")[1].replace("/", "")
url+="?__a=1"
try:
    with urllib.request.urlopen(url) as response:
        html = response.read()
        parsed_json = json.loads(html)
        post_obj = parsed_json["graphql"]["shortcode_media"]
        if post_obj["is_video"]:
            video_url=post_obj["video_url"]
            media_id+=".mp4"
            with urllib.request.urlopen(video_url) as video_file:
                video_decode = video_file.read()
                open(media_id, "wb").write(video_decode)
                print("Done. saved as {}".format(media_id))
                os.system(media_id)
        elif "edge_sidecar_to_children" in post_obj:
            slide_posts = post_obj["edge_sidecar_to_children"]["edges"]
            i=0
            if os.path.exists(f"./{media_id}"):
                    shutil.rmtree("./"+media_id)
            os.makedirs(media_id)
            for img in slide_posts:
                i+=1
                img_url=img["node"]
                if img_url["is_video"]:
                    img_url=img_url["video_url"]
                    with urllib.request.urlopen(img_url) as img_url:
                        img_decode = img_url.read()
                        open("./"+media_id+"/"+str(i)+".mp4", "wb").write(img_decode)
                else:
                    img_url = img_url["display_resources"][-1]["src"]
                    with urllib.request.urlopen(img_url) as img_url:
                        img_decode = img_url.read()
                        open("./"+media_id+"/"+str(i)+".jpg", "wb").write(img_decode)
            print("Done. saved as {}".format(media_id))
            if sys.platform == 'darwin':
                def openFolder(path):
                    os.system('open '+ path)
            elif sys.platform == 'linux2':
                def openFolder(path):
                    os.system('xdg-open '+ path)
            elif sys.platform == 'win32':
                def openFolder(path):
                    os.system('start '+ path)
            openFolder(media_id)
        else:
            img_url=post_obj["display_resources"][-1]["src"]
            media_id+=".jpg"
            # print(img_url)
            with urllib.request.urlopen(img_url) as img_url:
                img_decode = img_url.read()
                open(media_id, "wb").write(img_decode)
                print("Done. saved as {}".format(media_id))
                os.open(media_id)
                # os.system(media_id)
except urllib.error.HTTPError as e:
    print("Post " + e.reason)
