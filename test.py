
import spotipy
# Create a Spotipy object
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id='a24c797e8e9a487a8c6f9aaceadd3eab', client_secret='87183cc80b114379b637810a397c3f60', redirect_uri='http://127.0.0.1:5000/'))

# Get the user's access token
access_token = sp.auth_manager.get_access_token()['access_token']
# artist_name="Martin Garrix"
# Make the request to the Spotify API, passing in the access token as a header
#recommendations = sp.recommendations(limit=5, seed_genres=['pop'])
# recommendations = sp.search(q=f'artist:"Martin Garrix"', type='track', limit=5)
# print(recommendations)



# if not recommendations['tracks']['items']:
#     print(f"No data obtained for {artist_name}")
# else:
#     track = recommendations['tracks']['items'][0]
#     print(f"Track name: {track['name']}")

# To display the track link nd its embed link
"""
recommendations = sp.search(q=f'artist:f"{artist_name}"',type='track', limit=1)
for track in recommendations['tracks']['items']:
    print(f"Track link: {track['external_urls']}")
    print(f"Embed link: https://open.spotify.com/embed/track/{track['id']}")
"""

#To search a song by language(not possible)
#recommendations = sp.search(language="tamil",type='track', limit=1)


#To search a song by country(not possible)
"""
country_name = "United Kingdom"  
# Replace with the country you want to explore

# Perform a search for playlists or genres associated with the country
search_results = sp.search(q=f'country:{country_name}', type='playlist', limit=5)

# Print the search results
for i, playlist in enumerate(search_results['playlists']['items'], 1):
    print(f"{i}. Playlist Name: {playlist['name']}")
    print(f"   Owner: {playlist['owner']['display_name']}")
"""

#Suggest songs by inputting a song

seed_tracks = [
     'spotify:track:50WAStjMknUm3qavOmpc1r',  # Replace with a valid track URI
]

# Get song recommendations based on the seed tracks
recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=3)

# Print the recommended tracks
for i, track in enumerate(recommendations['tracks'], 1):
    print(f"{i}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")