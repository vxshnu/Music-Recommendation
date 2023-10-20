
from matplotlib import artist
import spotipy
from flask import Flask,render_template,request

# Create a Spotipy object
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id='a24c797e8e9a487a8c6f9aaceadd3eab', client_secret='87183cc80b114379b637810a397c3f60', redirect_uri='http://127.0.0.1:5000/'))

# Get the user's access token
access_token = sp.auth_manager.get_access_token()['access_token']



app=Flask(__name__)

@app.route('/')
def home():
   return render_template("songrec.html")



@app.route('/artist', methods =["GET", "POST"])
def artist():
    if request.method == "POST":
        artist_name=request.form["aname"]
        find_artist = sp.search(q=f'artist:"{artist_name}"', type='artist',limit=1)

        if find_artist['artists']['items']:
            artist_uri = find_artist['artists']['items'][0]['uri']
        else:
            print(f"No artist found for '{artist_name}'")
        if artist_uri:
            top_tracks = sp.artist_top_tracks(artist_uri)
            artist_tracks = top_tracks['tracks']
            embed_links = [f"{track['id']}" for track in artist_tracks]
            print(f"Embed link: {embed_links}")

            return render_template("rec.html",recommendation=top_tracks,urls=embed_links)
        else:
            return "No artist found"
    else:
        return "Error"




# @app.route('/')
# def home():
#     artist_name="Martin Garrix"
#     find_artist = sp.search(q=f'artist:"{artist_name}"', type='artist',limit=1)

#     if find_artist['artists']['items']:
#         artist_uri = find_artist['artists']['items'][0]['uri']
#     else:
#         print(f"No artist found for '{artist_name}'")
#     if artist_uri:
#         top_tracks = sp.artist_top_tracks(artist_uri)
#         artist_tracks = top_tracks['tracks']
#         embed_links = [f"{track['id']}" for track in artist_tracks]
#         print(f"Embed link: {embed_links}")

#         return render_template("rec.html",recommendation=top_tracks,urls=embed_links)
#     else:
#         return "No artist found"


# @app.route('/artist', methods =["GET", "POST"])
# def artist():
#     if request.method == "POST":
#        # getting input with name = fname in HTML form
#        first_name = request.form["fname"]
#        # getting input with name = lname in HTML form 
#        last_name = request.form["lname"]
#        num=request.form["Drop"]
#        return ("Your name is "+first_name + last_name)
       
#     return "HEy"


# @app.route('/track')
# def track():
#     track_name="In the name of love"
#     seed_track=sp.search(q=track_name,type="track",limit=5)
#     if seed_track['track']['']
#     recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=1)


if __name__=="__main__":
    app.run(debug=True)







# @app.route('/')
# def home():
#     recommend = sp.recommendations(q=f"Martin Garrix", type='track',limit=1)
#     print(recommend)
#     x=[track['uri']for track in recommend['tracks']]
#     print(x)
#     seed_track_uri = x

#     # Get song recommendations based on the seed track
#     recommendations = sp.recommendations(seed_tracks=[seed_track_uri], limit=10)
#     print(recommendations)
#     # Extract Spotify embed links for recommended tracks
#     # embed_links = [f"https://open.spotify.com/embed/track/{track['id']}" for track in recommendations['tracks']]
#     embed_links = [f"{track['id']}" for track in recommendations['tracks']]
#     print(f"Embed link: {embed_links}")

#     # Render the 'rec.html' template and pass the recommendations and embed links
#     return render_template("rec.html",recommendation=recommendations,urls=embed_links)








    # #return render_template('songrec.html')
    # seed_tracks ='spotify:track:50WAStjMknUm3qavOmpc1r'

    # # Get song recommendations based on the seed tracks
    # recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=1)

    # # Print the recommended tracks
    # for i, track in enumerate(recommendations['tracks'], 1):
    #     print(f"{i}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
    
    # for track in recommendations['tracks']['items']:
    #     print(f"Track link: {track['external_urls']}")
    #     print(f"Embed link: https://open.spotify.com/embed/track/{track['id']}")
    #     return render_template ("rec.html",urls={track['id']})
    


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
# track_name="In the name of love"
# recommendations=sp.recommendations
