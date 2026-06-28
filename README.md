# Sharify

A music-discovery platform built on the **Spotify API** — explore your
listening taste, follow other users, and surface playlist recommendations.

<!-- Add a screenshot or GIF here, e.g. ![sharify](docs/screenshot.png) -->

## Features
- Spotify **OAuth2** login and real-time playlist sync
- Listening/taste data pulled from the Spotify Web API into a SQL database
- Follower relationships, laying the foundation for a personalised discovery feed

## Stack
- **Backend:** Python, Flask (app-factory pattern — see `website/`)
- **Data:** SQL, Spotify Web API
- **Auth:** OAuth2

## Run
The entry point is `main.py`, which builds the Flask app via
`website.create_app()`. You'll need Spotify API credentials (client ID/secret)
configured as environment variables before running.
