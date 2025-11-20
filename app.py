import os
import pandas as pd
from flask import Flask, jsonify, render_template, request

#current base path for webapp. can be changed for your own repository
#currently compatible for github
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')


app = Flask(__name__)
#use flask. do remember that we are going to use mongoDB
#and/or pgadmin for SQL afterwards


# Load CSV once at startup

df_playback = pd.read_csv(os.path.join(DATA_DIR, "daily_playback.csv"))
df_songs = pd.read_csv(os.path.join(DATA_DIR, "songs_popularity.csv"))
df_states = pd.read_csv(os.path.join(DATA_DIR, "state_map.csv"))


# Map for singer icons
singer_icons = {
    "Singer A": "singer_a.jpg",
    "Singer B": "singer_b.jpg"
}

#Main page and icon. we dont really need icon so we can totally delete this.
#UNLESS we want to populate the dataset with some of the icons which will multiple our work for ETL.
@app.route('/')
def index():
    # Default singer icon
    return render_template('index.html', artist_icon='placeholder.jpg')

#API1 daily stream line chart
@app.route('/api/playbacks')#remember to call this so the whole API works for line graph!!!!
def api_playbacks():
    singer = request.args.get("singer_name", "Singer A")

    df = df_playback[df_playback["singer_name"] == singer].sort_values("playback_date").tail(7)

    if df.empty:
        return jsonify({"error": "Singer not found"}), 404

    return jsonify({
        "singer_name": singer,
        "icon_filename": singer_icons.get(singer, "placeholder.jpg"),
        "playback_dates": df["playback_date"].tolist(),
        "playback_counts": df["playback_count"].tolist()
    })

#API2 Song popularity Bar Chart
@app.route('/api/songs')#remember to call this so the whole API works for line graph!!!!
def api_songs():
    singer= request.args.get("singer_name", "Singer A")

    df = df_songs[df_songs["singer_name"] == singer]

    if df.empty:
        return jsonify({"error": "Singer not found"}), 404

    return jsonify({
        "song_names": df["song_name"].tolist(),
        "popularities": df["popularity"].tolist()
    })


#API3 US state map and hottest song for each map for the selected singer
@app.route('/api/state-map')#remember to call this so the whole API works for line graph!!!!
def api_state_map():
    singer = request.args.get("singer_name", "Singer A")

    df = df_states[df_states["singer_name"] == singer ]

    if df.empty:
        return jsonify({"error": "Singer not found"}), 404

    data = []
    for _, row in df.iterrows():
        data.append({
            "name": row["state"],  # must match GeoJSON exactly
            "top_song": row["top_song"] if pd.notnull(row["top_song"]) else "N/A",
            "value": 1  # can use another metric if desired
        })
    return jsonify(data)


#run app for the "render" platform
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port, debug=True)

