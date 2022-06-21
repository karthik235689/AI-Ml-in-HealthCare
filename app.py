from flask import Flask ,render_template

app=Flask(__name__)


'''
Common Pages
'''
@app.route("/")
@app.route("/home")
def home():
    return render_template("/Commonpages/index.html")

@app.route("/about")
def about():
    return render_template("/Commonpages/aboutus.html")


'''
Patients
'''
@app.route("/Login_Patients")
def Login_Patients():
    return render_template("/P_Pages/P_Login.html")

@app.route("/Register_Patients")
def Register_Patients():
    return render_template("/P_Pages/P_Register.html")





'''
Doctors
'''
@app.route("/Login_Doctors")
def Login_Doctors():
    return render_template("/D_Pages/D_Login.html")

@app.route("/Register_Doctors")
def Register_Doctors():
    return render_template("/D_Pages/D_Register.html")




'''
Lab
'''
@app.route("/Login_Lab")
def Login_Lab():
    return render_template("/L_Pages/L_Register.html")

@app.route("/Register_Lab")
def Register_Lab():
    return render_template("/D_Pages/D_Login.html")

@app.route("/lab/home")
def Home_Lab():
    return render_template("/L_Pages/index.html",title="Dashboard")

@app.route("/lab/profile")
def Profile_Lab():
    return render_template("/L_Pages/profile.html",title="Profile")

@app.route("/lab/upload")
def Upload_Lab():
    return render_template("/L_Pages/upload.html",title="Upload")

@app.route("/lab/history")
def Uploadhistory_Lab():
    return render_template("/L_Pages/uploadhistory.html",title="Upload History")

if __name__ == "__main__":
    app.run(debug=True)