import sys
import os
import urllib.request
import json
url=sys.argv[1].split("?")[0]
media_id=url.split("/p/")[1].replace("/", "")
url+="?__a=1"
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
    else:
        img_url=post_obj["display_resources"][-1]["src"]
        media_id+=".jpg"
        # print(img_url)
        with urllib.request.urlopen(img_url) as img_url:
            img_decode = img_url.read()
            open(media_id, "wb").write(img_decode)
            print("Done. saved as {}".format(media_id))
            os.system(media_id)
