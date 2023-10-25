import spotipy
import mysql.connector  
from flask import Flask,render_template,request,url_for,redirect

myconn = mysql.connector.connect(host = "127.0.0.1", user = "root",passwd = "root")  
db=myconn.cursor()


sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id='a24c797e8e9a487a8c6f9aaceadd3eab', client_secret='87183cc80b114379b637810a397c3f60', redirect_uri='http://127.0.0.1:5000/'))
access_token = sp.auth_manager.get_access_token()['access_token']

app=Flask(__name__)

user_active=""
email_id=""

@app.route('/')
def home():
   if user_active:
       return render_template("firstpg.html",n=user_active)
   else:
       return render_template("firstpg.html",n="LOGIN")
   

@app.route('/artist')
def artist(name):
        artist_name=name
        find_artist = sp.search(q=f'artist:"{artist_name}"', type='artist',limit=1)

        if find_artist['artists']['items']:
            artist_uri = find_artist['artists']['items'][0]['uri']
        else:
            return render_template("error.html",message="Artist not found")
        if artist_uri:
            top_tracks = sp.artist_top_tracks(artist_uri)
            artist_tracks = top_tracks['tracks']
            embed_links = [f"{track['id']}" for track in artist_tracks]
            # embed_links.pop(8)
            # embed_links.pop(8)
            print(f"Embed link: {embed_links}")
            if user_active:
                history_insert(name,embed_links)
            return render_template("rec.html",recommendation=top_tracks,names=artist_name)
        else:
            return render_template("error.html",message="Artist not found")

@app.route('/track')
def track(name):
        track_name=name

        seed_track=sp.search(q=track_name,type="track",limit=1)
        if seed_track['tracks']['items']:
            track_uri = seed_track['tracks']['items'][0]['uri']
        else:
            return render_template("error.html",message="Track not found")
        print(track_uri)
        recommendations = sp.recommendations(seed_tracks=[track_uri], limit=8)
        embed_links = [f"{track['id']}" for track in recommendations['tracks']]
        print(recommendations)
        if embed_links:
            if user_active:
                history_insert(name,embed_links)
            return render_template("rec.html",recommendation=recommendations,urls=embed_links,names=track_name)
        else:
            return render_template("error.html",message="No similar tracks found")

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form["aname"]
        options = request.form.get('dropdown')
        if options == "artist":
            return artist(name) 
        elif options == "track":
            return track(name) 
        elif options == "genre":
            return genre(name)
        else:
            return render_template("ioption.html")
    else:
        return "Method not allowed" 

@app.route('/genre', methods =["GET", "POST"])
def genre(name):
        genre_name=name
        recommendations=sp.recommendations(seed_genres=[genre_name], limit=8)
        print(recommendations)
        if recommendations['tracks']:
            embed_links = [f"https://open.spotify.com/embed/track/{track['id']}" for track in recommendations['tracks']]
            print(f"Embed link: {embed_links}")
            if embed_links:
                if user_active:
                    history_insert(name,embed_links)
                return render_template("rec.html", recommendation=recommendations, urls=embed_links,names=genre_name)
            else:
                return render_template("error.html",message="No similar tracks found")
        else:
            return render_template("error.html",message="Genre not found")
        
        
def history_insert(name,embed_links):
    db.execute("USE spotify")
    result=','.join(embed_links)
    query="INSERT INTO history (email,search,suggested) VALUES (%s,%s,%s)"
    data=(email_id,name,result)
    db.execute(query,data)
    myconn.commit()
        
@app.route('/creds')
def creds():
    if user_active:
        return render_template("user.html")
    else:
        return render_template("LoginPg.html")
    

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        x=request.form.get("email")
        y=request.form.get("password")
        db.execute("USE spotify")
        query="SELECT name from creds where email=%s and password=%s"
        data=(x,y)
        db.execute(query,data)
        result=db.fetchall()
        if result:
            global user_active,email_id
            user_active=str(result[0][0])
            email_id=x
            return redirect(url_for("home"))
        else:
            return "failed"
    else:
        return "<h1>try another way</h1>"

@app.route('/condition_log')
def condition_log():
    return render_template("signup.html")

@app.route('/condition_sign')
def condition_sign():
    return render_template("LoginPg.html")

def new_user(a,b,c):
    db.execute("USE spotify")
    x=a
    y=b
    z=c
    query="SELECT name from creds where email=%s"
    data=(x,)
    db.execute(query,data)
    result=db.fetchall()
    if result :
        return render_template("signup.html")
    else:
        insert_query = "INSERT INTO creds ( email,name, password) VALUES ( %s, %s, %s)"
        data = (x, y, z)
        db.execute(insert_query, data)
        myconn.commit()
        return None

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        x=request.form.get("email")
        y=request.form.get("name")
        z=request.form.get("password")
        new_user(x,y,z)
        return render_template("LoginPg.html")
    else:
        return "<h1>try another way</h1>"


@app.route('/user_menu',methods=['GET','POST'])
def user_menu():
    if request.method=='POST':
        x=request.form.get('button')
        print(x)
        if x=="history":
            db.execute("USE spotify")
            query="SELECT search from history where email=%s"
            data=(email_id,)
            db.execute(query,data)
            result=db.fetchall()
            print(data)
            print(result)
            return render_template("history.html",history=result)
        else:
            return f"{x}"
    else:
        return "wrong method"
    

@app.route('/suggested',methods=['GET','POST'])
def suggested():
    if request.method=='POST':
        name=request.form.get('button')
        db.execute("USE spotify")
        query="SELECT suggested from history where email=%s and search=%s"
        data=(email_id,name)
        db.execute(query,data)
        result=db.fetchall()
        print(result)
        if result:
            embed_links = result[0][0].split(',')
            return render_template("history_songs.html",songs=embed_links)
    else:
        return "wrong method"


if __name__=="__main__":
    app.run(debug=True)

        
# @app.route('/year', methods =["GET", "POST"])
# def year(name):
#         year_release={'from': '2010', 'to': '2020'}
#         print(type(year_release))
#         recommendations=sp.recommendations(release_date_range=year_release,limit=12)
#         print(recommendations)
#         if recommendations['tracks']:
#             embed_links = [f"https://open.spotify.com/embed/track/{track['id']}" for track in recommendations['tracks']]
#             print(f"Embed link: {embed_links}")
#             if embed_links:
#                 return render_template("rec.html", recommendation=recommendations, urls=embed_links,names=name)
#             else:
#                 return render_template("error.html",message="No tracks found")
#         else:
#             return render_template("error.html",message="Date issue")

# @app.route('/year', methods =["GET", "POST"])
# def year(name):
#         year_release=name
#         print(type(year_release))
#         recommendations=sp.recommendations(target_tempo=year_release)
#         print(recommendations)
#         if recommendations['tracks']:
#             embed_links = [f"https://open.spotify.com/embed/track/{track['id']}" for track in recommendations['tracks']]
#             print(f"Embed link: {embed_links}")
#             if embed_links:
#                 return render_template("rec.html", recommendation=recommendations, urls=embed_links,names=name)
#             else:
#                 return render_template("error.html",message="No tracks found")
#         else:
#             return render_template("error.html",message="Date issue")










# from matplotlib import artist
# import spotipy
# from flask import Flask,render_template,request

# # Create a Spotipy object
# sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id='a24c797e8e9a487a8c6f9aaceadd3eab', client_secret='87183cc80b114379b637810a397c3f60', redirect_uri='http://127.0.0.1:5000/'))

# # Get the user's access token
# access_token = sp.auth_manager.get_access_token()['access_token']


# app=Flask(__name__)

# @app.route('/')
# def home():
#    return render_template("songrec.html")


# @app.route('/artist', methods =["GET", "POST"])
# def artist():
#     if request.method == "POST":
#         artist_name=request.form["aname"]
#         find_artist = sp.search(q=f'artist:"{artist_name}"', type='artist',limit=1)

#         if find_artist['artists']['items']:
#             artist_uri = find_artist['artists']['items'][0]['uri']
#         else:
#             print(f"No artist found for '{artist_name}'")
#         if artist_uri:
#             top_tracks = sp.artist_top_tracks(artist_uri)
#             artist_tracks = top_tracks['tracks']
#             embed_links = [f"{track['id']}" for track in artist_tracks]
#             print(f"Embed link: {embed_links}")

#             return render_template("rec.html",recommendation=top_tracks,urls=embed_links)
#         else:
#             return "No artist found"
#     else:
#         return "GO BACK AND SEARCH IN SEARCH BAR!"

# @app.route('/track', methods =["GET", "POST"])
# def track():
#     if request.method=="POST":
#         track_name=request.form["aname"]
#         seed_track=sp.search(q=track_name,type="track",limit=1)
#         if seed_track['tracks']['items']:
#             track_uri = seed_track['tracks']['items'][0]['uri']
#         else:
#             print( "Invalid Track Name")
#         print(track_uri)
#         recommendation = sp.recommendations(seed_tracks=[track_uri], limit=8)
#         embed_links = [f"{track['id']}" for track in recommendation['tracks']]
#         print(f"Embed link: {embed_links}")
#         if embed_links:
#             return render_template("rec.html",recommendation=recommendation,urls=embed_links)
#         else:
#             return "Track not found 404"
#     else:
#         return "GO BACK AND SEARCH IN SEARCH BAR!"


# if __name__=="__main__":
#     app.run(debug=True)

# @app.route('/genre', methods =["GET", "POST"])
# def genre():
#     if request.method=="POST":
#         genre_name=request.form["aname"]
#         recommendations=sp.recommendations(seed_genres=genre_name, limit=12)
#         print(recommendations)
#         if recommendations['tracks']:
#             embed_links = [f"https://open.spotify.com/embed/track/{track['id']}" for track in recommendations['tracks']]
#             print(f"Embed link: {embed_links}")
#             if embed_links:
#                 return render_template("rec.html", recommendation=recommendations, urls=embed_links)
#             else:
#                 return "No embed links found."
#         else:
#             return "No recommendations found for the selected genre."
#     else:
#         return "GO BACK AND SEARCH IN SEARCH BAR!"






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
