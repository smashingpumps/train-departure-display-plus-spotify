# spotify_display.py
#
# Renders a "Now Playing" screen using the Spotify Web API (SpotifyOAuth).
# Requires user login once to grant access for playback state.

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class SpotifyNowPlaying:
    def __init__(self, client_id, client_secret, redirect_uri="http://localhost:8080"):
        """Initialize the Spotify client with OAuth (user login required once)."""
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="user-read-playback-state",
                open_browser=True,
                cache_path=".spotifycache",
            )
        )

    def get_now_playing(self):
        """Return track and artist currently playing."""
        try:
            current = self.sp.current_playback()
        except Exception as e:
            print(f"Spotify API error: {e}")
            return None

        if not current or not current.get("item"):
            return None

        track = current["item"]["name"]
        artist = ", ".join([a["name"] for a in current["item"]["artists"]])
        return f"{track} — {artist}"

    def render_screen(self, width=256, height=64):
        """Return a PIL image ready for display."""
        img = Image.new("1", (width, height), color=0)  # 1-bit image for OLED
        draw = ImageDraw.Draw(img)
        font_large = ImageFont.truetype(FONT_PATH, 14)
        font_small = ImageFont.truetype(FONT_PATH, 10)

        title = "🎵 Spotify Now Playing"
        draw.text((4, 4), title, font=font_small, fill=1)

        info = self.get_now_playing()
        if info:
            draw.text((4, 24), info, font=font_large, fill=1)
        else:
            draw.text((4, 24), "No track currently playing", font=font_large, fill=1)

        return img
