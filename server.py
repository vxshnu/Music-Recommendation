
from flask import Flask, request, render_template ,redirect,request

app = Flask(__name__)   
 

@app.route('/')
def home():
   return render_template("artist.html")


@app.route('/get')
def get():
   return render_template("forms.html")

@app.route('/artist', methods =["GET", "POST"])
def artist():
    if request.method == "POST":
       
       name = request.form["aname"]
       
     
       return name
       
    return "Error"
 
if __name__=='__main__':
   app.run()
