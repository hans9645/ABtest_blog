from flask import Flask,Blueprint,request,render_template

blog_abtest=Blueprint('blog',__name__)

@blog_abtest.route('/engA')
def eng():
    return render_template("blog_engA.html")

@blog_abtest.route('/engB')
def kor():
    return render_template("blog_engB.html")