from flask import Flask, render_template, request
from img_recognition import main

app = Flask(__name__)

@app.route("/")
# "/" = home page; runs main at home page (in the broswer url, it's what comes after it)
# eg. 127.0.0.1:5000/ (this is main)

def main_page():
    a = [1, 3, "h", 4] # printing out an example list
    
    return render_template("base.html", a=a, test=True)
    # converts jinja page to html, passing variable into jinja (jinja just contains the python code within html
    # a=a is passing the variable into the html, while test=True is for the "Hello world !!" to show if test=True

@app.route("/2")
# this would be from 127.0.0.1:5000/2 instead of just the "/"
def secondpage():
    return render_template("secondpage.html")

@app.route("/3")
def thirdpage():
    return render_template("filename.html")

@app.route("/get_json")
def get_json():
    my_file = request.files["adasd"]
    my_file.save("temp.png")

    notes = main("temp.png")

    return {
        "notes": [[["C4"],["C5", "A4","B5"],["F5"]], [["C4"],["C5", "A4","B5"],["F5"]]]
    }

# just an ending thing 
if __name__ == "__main__":
    app.run(debug=True)
