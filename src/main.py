# main.py
#
# Modified to alternate between train departures and Spotify Now Playing screen.

import time
import json
from display import Display
from spotify_display import SpotifyNowPlaying


def load_config():
    with open("config.json") as f:
        return json.load(f)


def main():
    config = load_config()
    station_code = config.get("station", "WAT")

    # Durations (seconds)
    train_display_duration = config.get("train_display_duration", 30)
    spotify_display_duration = config.get("spotify_display_duration", 10)

    # Spotify credentials
    spotify_id = config.get("spotify_client_id")
    spotify_secret = config.get("spotify_client_secret")

    # Initialize displays
    display = Display(station_code)
    spotify = SpotifyNowPlaying(spotify_id, spotify_secret)

    print(f"Starting display rotation: Train {train_display_duration}s / Spotify {spotify_display_duration}s")

    while True:
        # Train departures
        print("Showing train departures...")
        display.update()  # existing method
        time.sleep(train_display_duration)

        # Spotify Now Playing
        print("Showing Spotify Now Playing...")
        try:
            img = spotify.render_screen()
            display.epd.display(display.epd.getbuffer(img))
        except Exception as e:
            print(f"Spotify render error: {e}")
        time.sleep(spotify_display_duration)


if __name__ == "__main__":
    main()
