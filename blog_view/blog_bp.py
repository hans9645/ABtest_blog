from flask import Flask,Blueprint,request,render_template

blog_abtest=Blueprint('blog',__name__)

@blog_abtest.route('/eng')
def eng():
    return render_template("blog_eng.html")

@blog_abtest.route('/kor')
def kor():
    return render_template("blog_kor.html")