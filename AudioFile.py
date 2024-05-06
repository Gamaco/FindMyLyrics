import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

def main():
    # Set up the Spotify OAuth2 manager with your application's credentials and desired access scope
    sp_oauth = SpotifyOAuth(
        client_id = '757e5ebc8e2945d4808de6fca9ac4b7b',
        client_secret = '794bbce4d11e4978b03b96e0ae5de4af',
        redirect_uri = 'http://localhost:8888/callback',
        scope = 'user-read-currently-playing'
    )

    # Try to get a cached token, which may be available if the user has already authenticated and the token hasn't expired
    token_info = sp_oauth.get_cached_token()

    # If there is no cached token, initiate the authorization process
    if not token_info:
        # Get the URL where the user will authenticate and authorize the application
        auth_url = sp_oauth.get_authorize_url()
        # Open the user's default web browser to the authorization URL
        webbrowser.open(auth_url)
        # Prompt the user to paste the URL they were redirected to after authorizing the app
        print("Please authorize access and paste the URL you were redirected to: ")
        response = input()
        # Extract the authorization code from the response URL
        code = sp_oauth.parse_response_code(response)
        # Exchange the code for an access token
        token_info = sp_oauth.get_access_token(code)

    # Create a Spotify client with the access token
    spotify = spotipy.Spotify(auth=token_info['access_token'])

    # Use the Spotify client to fetch the currently playing track
    current_track = spotify.current_user_playing_track()
    if current_track:
        # Print details of the currently playing track
        print(f"Currently playing: {current_track['item']['name']} by {', '.join(artist['name'] for artist in current_track['item']['artists'])}")
    else:
        # Inform the user if no track is currently playing
        print("No track is currently playing.")

if __name__ == '__main__':
    main()