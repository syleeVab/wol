from flask import Flask, redirect, render_template, request, url_for
import os, sys, login, requests as api_req
from datetime import timedelta

# 블루프린트로 연결
app = Flask(__name__)
app.secret_key = os.urandom(24) # 사용자 세션 관리를 할 때 필요한 정보
# login session timeout 시간 조정
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# # 웹에 한글 출력 시 글짜 깨지는 현상 방지용 : 웹에서는 기본적으로 기존 utf-8 인코딩이 아닌, ascii 인코딩으로 출력됨.
app.config['JSON_AS_ASCII'] = False

# app.register_blueprint(login.bp_login)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/control', methods=['GET', 'POST'])
def controlPC():
    if request.method == 'GET':
        return render_template('control.html')


@app.route('/login', methods=['POST'])
def loginCheck():
    if request.method =='POST':
        # print(dir(request))
        login_info = request.form
        # print(login_info['id'], login_info['pw'])

        # api에 전송
        data = {'LoginID': login_info['id'], 'LoginPass': login_info['pw']}
        res = api_req.post('https://carstat.co.kr/api/user/cs/auth', data=data)

        if res.status_code == 200: # 200일 경우 정상
            print('kk')
            return redirect(url_for('controlPC'), 'user:')
        print('hh')
        return render_template('home.html', loginFail=True)
    else:
        print('dd')
        return render_template('home.html', connectFail=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
    