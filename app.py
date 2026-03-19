from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "status": "ONLINE",
        "owner": "MR SHARABI",
        "tool": "Instagram Data Server"
    }

@app.route("/insta")
def insta_info():

    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username required"})

    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-IG-App-ID": "936619743392459"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return jsonify({"error": "Failed to fetch data"})

    data = r.json()

    user = data["data"]["user"]

    result = {
        "username": user["username"],
        "full_name": user["full_name"],
        "followers": user["edge_followed_by"]["count"],
        "following": user["edge_follow"]["count"],
        "posts": user["edge_owner_to_timeline_media"]["count"],
        "bio": user["biography"],
        "profile_pic": user["profile_pic_url_hd"]
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
