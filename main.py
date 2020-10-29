import sys
import os
import urllib.request
import json
url=sys.argv[1]
media_id=url.split("/p/")[1].replace("/", "")+".mp4"
url+="?__a=1"
with urllib.request.urlopen(url) as response:
    html = response.read()
    parsed_json = json.loads(html)
    video_url = parsed_json["graphql"]["shortcode_media"]["video_url"]
    with urllib.request.urlopen(video_url) as video_file:
        video_decode = video_file.read()
        open(media_id, "wb").write(video_decode)
        print("Done. saved as {}".format(media_id))
        os.system(media_id)
