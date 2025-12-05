# APAN5400_Group
## Pipelines & Required Files

### SQL pipeline
To identify the artist who has the popularity higher than average level for two days.

### Pipeline 1: `graph1`
**Required files (5 days):**
- `spotify_artist_top10_albums_{today}.json`  
  *(One file per day for five days)*
**Output**
- `combined_spotify_daily_with_ids.csv`
 *(One file contains five continuous dates)*
---

### Pipeline 2: `graph2`
**Required files:**
- `spotify_artist_info_{today}.json`
- `spotify_artist_tracks_{today}.json`
**Output**
- `spotify_artists_with_top10_tracks.csv`
 *Each artist has no more than 10 tracks included*


