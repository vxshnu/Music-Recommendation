# importing Flask and other modules
from flask import Flask, request, render_template 
 
# Flask constructor
app = Flask(__name__)   
 
# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def home():
   return render_template("forms.html")


@app.route('/login', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form["fname"]
       # getting input with name = lname in HTML form 
       last_name = request.form["lname"]
       num=request.form["Drop"]
       return ("Your name is "+first_name + last_name)
       
    return "HEy"
 
if __name__=='__main__':
   app.run()