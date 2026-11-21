"""Posts the next reel from posts.json to Instagram, then records it in posted.json.

Runs on GitHub Actions once a day. Uses the official Instagram API
(Instagram API with Instagram Login, Content Publishing).
"""
import json, os, sys, time, urllib.parse, urllib.request

API = "https://graph.instagram.com/v25.0"
TOKEN = os.environ["IG_ACCESS_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]            # e.g. leo/leaguecoach-autopost
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")


def call(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{API}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{API}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Instagram API error on {path}: {e.read().decode()}")


PER_RUN = int(os.environ.get("POSTS_PER_RUN", "1"))
GAP = int(os.environ.get("MINUTES_BETWEEN_POSTS", "3"))


def main():
    user_id = os.environ.get("IG_USER_ID") or call("GET", "me", fields="user_id,username")["user_id"]
    for n in range(PER_RUN):
        if n: time.sleep(GAP * 60)
        if not post_next(user_id):
            break


def post_next(user_id):
    posts = json.load(open("posts.json"))
    posted = json.load(open("posted.json"))
    todo = [p for p in posts if p["file"] not in posted]
    if not todo:
        print("All reels have been posted. Add more to posts.json.")
        return False
    post = todo[0]
    video_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/videos/{urllib.parse.quote(post['file'])}"
    print(f"Posting {post['file']} from {video_url}")

    container = call("POST", f"{user_id}/media", media_type="REELS", video_url=video_url,
                     caption=post["caption"], share_to_feed="true")["id"]

    for _ in range(40):                       # wait up to ~10 minutes for Instagram to process the video
        status = call("GET", container, fields="status_code").get("status_code")
        print("status:", status)
        if status == "FINISHED":
            break
        if status in ("ERROR", "EXPIRED"):
            sys.exit(f"Instagram could not process {post['file']} (status {status}).")
        time.sleep(15)
    else:
        sys.exit("Timed out waiting for Instagram to process the video.")

    media = call("POST", f"{user_id}/media_publish", creation_id=container)
    print("Published, media id:", media.get("id"))
    posted.append(post["file"])
    json.dump(posted, open("posted.json", "w"), indent=2)
    return True


if __name__ == "__main__":
    main()
