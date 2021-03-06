from flask import Flask,Blueprint,request,render_template,redirect,make_response,jsonify,url_for,session
from blog_control.user_mgmt import User
from flask_login import login_user,current_user,logout_user
import datetime
from blog_control.session_mgmt import BlogSession
#login_user:서버단에서 세션 쿠키셋관련 임포트
#current_user: 세션확인 할 때 사용
#main코드에 app에 최초 before request함수를 정의해둬서 블루프린트로 정의된 라우팅으로 들어와도 자동으로 before requset가 실행됨.
blog_abtest=Blueprint('blog_bp',__name__)

@blog_abtest.route('/engA')
def engA():
    if current_user.is_authenticated:#세션확인 후 구독이력 확인
        return render_template("blog_engA.html",user_email=current_user.user_email)#여기에 jinja2에 들어갈 변수를 같이 넣어준다.
    else:
        return render_template('blog_engA.html')
@blog_abtest.route('/engB')
def engB():
    return render_template("blog_engB.html")


@blog_abtest.route('/fullstack')
def fullstack():    
    if current_user.is_authenticated:#세션확인 후 구독이력 확인
        web_page=BlogSession.get_blog_page(current_user.blog_id)#구독시 페이지정보  
        BlogSession.save_session_info(session['client_id'],current_user.user_email,web_page)
        #로그인한 방문자의 IP등을 세션라이브러리로부터 받아와서 넣는다.      
        return render_template(web_page,user_email=current_user.user_email)#여기에 jinja2에 들어갈 변수를 같이 넣어준다.
    else:
        web_page=BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'],'anonymous',web_page)
        #로그인하지않은 방문자의 IP등을 세션라이브러리로부터 받아와서 넣는다.
        return render_template(web_page)


@blog_abtest.route('/logout')
def logout():
    User.delete(user_id=current_user.id)
    logout_user() #어차피 라우팅 리퀘스트시 세션에 로그인 정보가 있다.
    return redirect(url_for('blog_bp.fullstack'))


@blog_abtest.route('/set_email',methods=['GET','POST'])
def set_email():
    if request.method=='GET':
        #print('http check',request.headers)
        print("set_email()",request.args.get('user_email'))
        #return make_response(jsonify(success=True),200) 
        #->vue와 같은 js를 사용하지 않고 서버단에서 풀스택을 구현하는 거라 전체페이지를 리로딩하는 식으로한다.
        #return redirect(url_for('blog_bp.engA'))
        return redirect(url_for(request.form['blog_id']))
    else:
        #print('http check',request.headers)
        #http request의 헤더부분을 가져올 수 있다. 이후 content type를 확인하고 데이터를 어떻게 가져와야하는지 고민하자.
        #content type이 application/json인 경우에는 request.get_json()
        #->print('set_email',request.get_json())
        #print('blog_id',request.form['blog_id'])
        #print('only user_email',request.form['user_email'])
        #post방식으로 데이터를 가져올 수 있다. vue에서 했었음
        user=User.create(request.form['user_email'],request.form['blog_id'])
        login_user(user,remember=True, duration=datetime.timedelta(days=30))
        #로그인 기록유지 시킴 remember me,flask_login google검색
        #세션정보가 플라스크에서 만들어져 셋쿠키로 웹브라우저에 전송, 웹브라우저는 서버주소와 쿠키를 저장,관리를 하면서 다음에 해당서버에 request를 할 때 사용한다. 
        #return redirect(url_for(request.form['blog_id']))
        return redirect('/blueprint/fullstack')

    

