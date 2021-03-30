from flask import Flask,Blueprint,request,render_template,redirect,make_response,jsonify,url_for

blog_abtest=Blueprint('blog_bp',__name__)

@blog_abtest.route('/engA')
def engA():
    return render_template("blog_engA.html")

@blog_abtest.route('/engB')
def engB():
    return render_template("blog_engB.html")


@blog_abtest.route('/set_email',methods=["GET","POST"])
def set_email():
    if request.method=='GET':
        print("set_email()",request.args.get('user_email'))
        #return make_response(jsonify(success=True),200) 
        #->vue와 같은 js를 사용하지 않아서 서버단에서 풀스택을 구현하는 거라 전체페이지를 리로딩하는 식으로한다.
        #return redirect(url_for('blog_bp.engA'))
        return redirect('/blueprint/engA')
    else:
        print('set_email',request.get_json())
        #post방식으로 데이터를 가져올 수 있다. vue에서 했었음
        return redirect(url_for('blog_bp.engA'))
