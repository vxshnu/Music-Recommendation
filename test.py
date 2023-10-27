import spotipy
import mysql.connector  
from flask import Flask,render_template,request,url_for,redirect
import random

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
        return render_template("firstpg.html",n=user_active[0].capitalize(),set="50px",radius="50px")
    else:
        return render_template("firstpg.html",n="LOGIN",set="100px" ,radius="3px")
    

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
            if user_active:
                history_insert(name,embed_links,"Artist")
            artist_info = sp.artist(artist_uri)
            artist_name = artist_info['name']
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
        recommendations = sp.recommendations(seed_tracks=[track_uri], limit=8)
        embed_links = [f"{track['id']}" for track in recommendations['tracks']]
        if embed_links:
            if user_active:
                history_insert(name,embed_links,"Track")
            return render_template("rec.html",recommendation=recommendations,names=seed_track['tracks']['items'][0]['name'])
        else:
            return render_template("error.html",message="No similar tracks found")


@app.route('/genre', methods =["GET", "POST"])
def genre(name):
        genre_name=name
        recommendations=sp.recommendations(seed_genres=[genre_name], limit=8)
        if recommendations['tracks']:
            embed_links = [f"{track['id']}" for track in recommendations['tracks']]
            if embed_links:
                if user_active:
                    history_insert(name,embed_links,"Genre")
                return render_template("rec.html", recommendation=recommendations,names=genre_name)
            else:
                return render_template("error.html",message="No similar tracks found")
        else:
            return render_template("error.html",message="Genre not found")

@app.route('/randomized', methods =["GET", "POST"]) 
def randomize():
    if request.method=="POST":
        genres=['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
        random_genres=random.sample(genres,2)
        selected_genres=",".join(random_genres)
        genre_name=selected_genres
        recommendations=sp.recommendations(seed_genres=[genre_name], limit=8)
        if recommendations['tracks']:
            embed_links = [f"{track['id']}" for track in recommendations['tracks']]
            if embed_links:
                if user_active:
                    history_insert("Randomized",embed_links,"Genre")
                return render_template("rec.html", recommendation=recommendations, names="RANDOM GEN 😊")
            else:
                return render_template("error.html",message="No similar tracks found")
        else:
            return render_template("error.html",message="Genre not found")


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
        
def history_insert(name,embed_links,filter):
    db.execute("USE spotify")
    result=','.join(embed_links)
    query="INSERT INTO history (email,search,suggested,filter) VALUES (%s,%s,%s,%s)"
    data=(email_id,name,result,filter)
    db.execute(query,data)
    myconn.commit()
        
@app.route('/creds')
def creds():
    if user_active:
        return render_template("user.html",n=user_active)
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
        global user_active, email_id
        if user_active:
            x=request.form.get('button')
            if x=="history":
                db.execute("USE spotify")
                query="SELECT search,filter from history where email=%s"
                data=(email_id,)
                db.execute(query,data)
                result=db.fetchall()
                return render_template("history.html",name=user_active,history=result)
            
            elif x=="logout":  
                user_active = email_id = None
                return redirect(url_for('home'))
            elif x=="confirm":
                return render_template("change_pass.html",text="")
            else:
                return f"{x}"
        else:
            return redirect(url_for('condition_sign'))
    else:
        return "wrong method"
    

@app.route('/suggested',methods=['GET','POST'])
def suggested():
    if request.method=='POST':
        name=request.form.get('button1')
        name2=request.form.get('button2')
        db.execute("USE spotify")
        if name:
            query="SELECT suggested from history where email=%s and search=%s"
            data=(email_id,name)
            db.execute(query,data)
            result=db.fetchall()
            if result:
                embed_links=[]
                for item in result:
                    string_value = item[0]
                    value_list = string_value.split(',')
                    embed_links.extend(value_list)
                return render_template("history_songs.html",songs=embed_links)
            else:
                return "error!"
        elif name2:
            query="DELETE from history where email=%s and search=%s"
            data=(email_id,name2)
            db.execute(query,data)
            myconn.commit()
            query="SELECT search,filter from history where email=%s"
            data=(email_id,)
            db.execute(query,data)
            result=db.fetchall()
            return render_template("history.html",name=user_active,history=result)
    else:
        return "wrong method"

@app.route('/current_password',methods=['GET','POST'])
def change_password():
    if request.method=="POST":
        x=request.form.get("password")
        db.execute("USE spotify")
        query="SELECT password from creds where email=%s"
        data=(email_id,)
        db.execute(query,data)
        result=db.fetchall()
        data=list(result[0])
        result=str(data[0])
        if result==x:
            y=request.form.get("new_password")
            db.execute("USE spotify")
            query="UPDATE creds set password=%s where email=%s"
            data=(y,email_id)
            db.execute(query,data)
            myconn.commit()
            return redirect(url_for('home'))
        else:
            
            return render_template("change_pass.html",text="Wrong Password")


# @app.after_request
# def add_header(response):
#     response.headers['Cache-Control'] = 'no-store, no-cache'
#     return response

if __name__=="__main__":
    app.run(debug=True)

