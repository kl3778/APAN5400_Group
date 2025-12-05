#this is the DEMO presentation version
import os
import pandas as pd
from flask import Flask, jsonify, render_template, request

#This version is not web-deploy compatible.


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


app = Flask(__name__)
#use flask.
#


# Helper function: normalize id
def normalize_id(x):
    if not x or not isinstance(x, str):
        return ""
    return x.strip()


#load csv. The csv file is generated for presentation DEMO purpose only.
df_playback = pd.read_csv(os.path.join(DATA_DIR, "daily_playback.csv"), parse_dates=["date"])
df_playback["artist_id"] = df_playback["artist_id"].apply(normalize_id)

df_songs = pd.read_csv(os.path.join(DATA_DIR, "songs_popularity.csv"))
df_songs["artist_id"] = df_songs["artist_id"].apply(normalize_id)

df_recommendation = pd.read_csv(os.path.join(DATA_DIR, "recommendation_scores.csv"))
df_recommendation["artist_id"] = df_recommendation["artist_id"].apply(normalize_id)



#Main page  index api.
@app.route('/')
def index():
    artists_df = df_playback[['artist_id', 'artist_name']].drop_duplicates()
    # convert to dict
    artists = artists_df.to_dict(orient='records')
    return render_template('index.html', artists=artists)

#API1 daily stream line chart
@app.route('/api/playbacks')
def api_playbacks():
    artist_id = normalize_id(request.args.get("artist_id", ""))

    df = df_playback[df_playback["artist_id"] == artist_id].sort_values("date").tail(7)

    if df.empty:
        return jsonify({"error": "Artist not found"}), 404

    return jsonify({
        "artist_name": df.iloc[0]["artist_name"],
        "dates": df["date"].dt.strftime("%Y-%m-%d").tolist(),
        "streams": df["daily_streams"].tolist()
    })


#API2 Song popularity Bar Chart
@app.route('/api/songs')
def api_songs():
    artist_id = normalize_id(request.args.get("artist_id", ""))

    df = df_songs[df_songs["artist_id"] == artist_id]

    if df.empty:
        return jsonify({"error": "Artist not found"}), 404

    return jsonify({
        "track_names": df["track_name"].tolist(),
        "track_popularities": df["track_popularity"].tolist()
    })



#API3 Recommendation score
@app.route('/api/recommendation')
def api_recommendation():
    artist_id = normalize_id(request.args.get("artist_id", ""))

    df = df_recommendation[df_recommendation["artist_id"] == artist_id]

    if df.empty:
        return jsonify({
            "artist_id": artist_id,
            "score": "N/A"
        })

    score = df.iloc[0]["avg_track_popularity"]

    return jsonify({
        "artist_id": artist_id,
        "score": score
    })



#run this at last
if __name__ == "__main__":
    from threading import Timer
    import webbrowser

    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")

    Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)


