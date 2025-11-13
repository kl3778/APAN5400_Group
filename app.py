import os
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Load CSV once at startup
df = pd.read_csv("daily_playback.csv", parse_dates = ["playback_date"] )  # make sure this file is in project root

# Map for singer icons
singer_icons = {
    "Singer A": "singer_a.jpg",
    "Singer B": "singer_b.jpg"
}


@app.route('/')
def index():
    # Default singer icon
    return render_template('index.html', artist_icon='placeholder.jpg')

@app.route('/api/playbacks')
def get_playbacks():
    singer_name = request.args.get('singer_name', 'Singer A')

    # Filter CSV for this singer
    singer_data = df[df['singer_name'] == singer_name].sort_values('playback_date').tail(7)
    if singer_data.empty:
        return jsonify({"error": "Singer not found"}), 404

    playback_dates = singer_data['playback_date'].tolist()
    playback_counts = singer_data['playback_count'].tolist()
    icon_filename = singer_icons.get(singer_name, "placeholder.jpg")

    return jsonify({
        "singer_name": singer_name,
        "playback_dates": playback_dates,
        "playback_counts": playback_counts,
        "icon_filename": icon_filename
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT automatically
    app.run(host="0.0.0.0", port=port, debug=True)

