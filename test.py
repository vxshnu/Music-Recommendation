
import spotipy
from flask import Flask,render_template,request

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id='a24c797e8e9a487a8c6f9aaceadd3eab', client_secret='87183cc80b114379b637810a397c3f60', redirect_uri='http://127.0.0.1:5000/'))

access_token = sp.auth_manager.get_access_token()['access_token']

app=Flask(__name__)

@app.route('/')
def home():
   return render_template("firstpg.html")

@app.route('/login')
def login():
   return render_template("LogInPg.html")

@app.route('/signup')
def signup():
   return render_template("signup.html")

@app.route('/artist')
def artist(name):
        artist_name=name
        find_artist = sp.search(q=f'artist:"{artist_name}"', type='artist',limit=1)

        if find_artist['artists']['items']:
            artist_uri = find_artist['artists']['items'][0]['uri']
        else:
            return render_template("error.html")

        if artist_uri:
            top_tracks = sp.artist_top_tracks(artist_uri)
            artist_tracks = top_tracks['tracks']
            embed_links = [f"{track['id']}" for track in artist_tracks]
            print(f"Embed link: {embed_links}")

            return render_template("rec.html",recommendation=top_tracks,urls=embed_links,names=artist_name)
        else:
            return "No artist found"

@app.route('/track')
def track(name):
        track_name=name

        seed_track=sp.search(q=track_name,type="track",limit=1)
        if seed_track['tracks']['items']:
            track_uri = seed_track['tracks']['items'][0]['uri']
        else:
            return render_template("error.html")
        print(track_uri)
        recommendations = sp.recommendations(seed_tracks=[track_uri], limit=8)
        embed_links = [f"{track['id']}" for track in recommendations['tracks']]
        print(recommendations)
        if embed_links:
            return render_template("rec.html",recommendation=recommendations,urls=embed_links,names=track_name)
        else:
            return "Track not found 404"

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form["aname"]
        options = request.form.get('dropdown')
        if options == "artist":
            return artist(name) 
        elif options == "track":
            return track(name) 
        else:
            return render_template("ioption.html")
    else:
        return "Method not allowed" 



@app.route('/genre', methods =["GET", "POST"])
def genre():
    if request.method=="POST":
        genre_name=request.form["aname"]
        recommendations=sp.recommendations(seed_genres=genre_name, limit=12)
        print(recommendations)
        if recommendations['tracks']:
            embed_links = [f"https://open.spotify.com/embed/track/{track['id']}" for track in recommendations['tracks']]
            print(f"Embed link: {embed_links}")
            if embed_links:
                return render_template("rec.html", recommendation=recommendations, urls=embed_links,names=genre_name)
            else:
                return "No embed links found."
        else:
            return "No recommendations found for the selected genre."
    else:
        return "GO BACK AND SEARCH IN SEARCH BAR!"


if __name__=="__main__":
    app.run(debug=True)


# Handle the case when the method is not POST (e.g., when the user accesses the page)

        # if recommendations["tracks"]:
        #     recommendation = recommendations['tracks']
        #     for i, track in enumerate(recommendation, 1):
        #         print(f"{i}. {track['name']} by {', '.join([artist['name'] for artist in track['artists']])}")
        #     else:
        #         print(f"No tracks found for genre '{genre}'")

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
