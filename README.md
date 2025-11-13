# APAN5400_Group


# Data Acquistion
📍 Overview

This module handles data acquisition from 3 platforms:

Spotify Web API

YouTube Data API v3

Google Trends (via pytrends)

It supports:

API integration

Data pulling [frequency to be defined]

Data validation

Data export (JSON / CSV)

🎧 Spotify Data Acquisition

Endpoints used:

GET /v1/artists/{id}

GET /v1/artists/{id}/top-tracks

GET /v1/audio-features/{id}

Outputs:

Artist metadata JSON

Track metadata JSON/CSV

Audio features JSON [require double check ]

🎬 YouTube Data Acquisition

Endpoints used:

channels().list

videos().list

search().list

Outputs:

Channel metadata JSON

Video metadata JSON/CSV

🔥 Google Trends Data Acquisition

Implemented via pytrends

Time series (interest over time)

Interest by region

Related queries

Outputs:

JSON + CSV files with timestamp [been blocked...sample file not available]

🔍 Validation- check list

Missing keys

Datatype check

Numerical range (e.g., popularity 0–100)

Empty dataframe detection

🧩 Final Deliverables

Raw JSON data files

Clean CSV tables

Data Dictionary [version 1 uploaded]

Validated metadata ready for ingestion
