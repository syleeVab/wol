from flask import Flask, redirect, render_template, request, url_for, session
import os, sys, login, requests as api_req, json
from datetime import timedelta
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from classes.user import user_info, name_list, adrs_dict, isUser, User # 사용자 그룹 정보 dict
from classes.wakeonlan import wakeOnLan

# 블루프린트로 연결
app = Flask(__name__)
app.secret_key = os.urandom(24) # 사용자 세션 관리를 할 때 필요한 정보
# login session timeout 시간 조정
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# # 웹에 한글 출력 시 글짜 깨지는 현상 방지용 : 웹에서는 기본적으로 기존 utf-8 인코딩이 아닌, ascii 인코딩으로 출력됨.
app.config['JSON_AS_ASCII'] = False

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    user = User(user_id=user_id)
    if user_info[user_id]['group'] == 'admin':
        user.isAdmin = True
    
    return user

# 현재 사용자가 로그인되어있지 않은 경우
@login_manager.unauthorized_handler
def unauthorzed():
    return redirect('/')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/personalPC', methods=['POST'])
@login_required
def personalControl():

    user_id = current_user.get_id().strip()
    user = user_info[user_id]    
    # user = json.loads(session['user']) # client에서 받는 데이터 쓸 거면 필요없음
    ID = user.get('id')
    GROUP = user.get('group')
    NAME = user.get('name')
    ADR = user.get('mac_adr')
    

    # if ID == request.json['id'] : # client의 id와 session의 id가 같으면 wol 실행
    if NAME == request.json['name']:
        wakeOnLan(ADR)
        return json.dumps({'ownIsSuccess': True})
    
    return json.dumps({'ownIsSuccess' : False})



@app.route('/collectLeft', methods=['POST'])
@login_required
def cltLeft():
    user_id = current_user.get_id().strip()
    user = user_info[user_id]
    ID = user.get('id')
    GROUP = user.get('group')
    NAME = user.get('name')
    ADR = '0C-54-A5-08-AA-D1' # 왼쪽 수집 PC mac 주소
    
    # client에서 name 정보를 맘대로 고칠 수 있나? 그런 거 방지용으로 만들고 싶은데

    # if ID == request.json['id'] and (GROUP == 'admin' or GROUP == 'multiGroup'): # client와 session id가 같고 특정 group일 때 wol 실행
    if NAME == request.json['name'] and (GROUP == 'admin' or GROUP == 'multiGroup'): # client와 session id가 같고 특정 group일 때 wol 실행
        wakeOnLan(ADR)
        return json.dumps({'leftIsSuccess': True})
    
    return json.dumps({'leftIsSuccess': False})



@app.route('/collectRight', methods=['POST'])
@login_required
def cltRight():
    user_id = current_user.get_id().strip()
    user = user_info[user_id]    
    ID = user.get('id')
    GROUP = user.get('group')
    NAME = user.get('name')
    ADR = 'B8-97-5A-B3-4F-93' # 오른쪽 수집 PC mac 주소

    # if ID == request.json['id'] and (GROUP == 'admin' or GROUP == 'multiGroup'):
    if NAME == request.json['name'] and (GROUP == 'admin' or GROUP == 'multiGroup'):
        wakeOnLan(ADR)
        return json.dumps({'rightIsSuccess': True})
    
    return json.dumps({'rightIsSuccess': False})



@app.route('/adminControl', methods=['POST'])
@login_required
def adminControl():
    user_id = current_user.get_id().strip()
    user = user_info[user_id]

    NAME = user.get('name')

    if NAME == request.json['name']:
        selectedName = request.json['control_name']
        ADR = adrs_dict[selectedName]
        wakeOnLan(ADR)
        print(ADR, 'success')

        return json.dumps({f'{selectedName}_wol_success': True})
    else :
        return json.dumps({f'{selectedName}_wol_success': False})
        


@app.route('/control/', methods=['GET', 'POST'])
@login_required
def controlPC():
    if request.method == 'GET':
        
        # flask_login current_user 이용
        user_id = current_user.get_id().strip()
        user = user_info[user_id]

        # session 1 : json으로 전송 시 
        # user = json.loads(session['user']) # json 문자열 parsing(json.loads) 후 'id'key값 얻기(user.get('id')) or user['id'] 마지막건 오류가 좀 나는 거 같음.

        # session 2 : id data만 전송 시
        # user_id = session['user'] # counterpart for session / json 말고 일반 data 전송 시

        # url_for 로 얻을 때
        # user_id = request.args['user'] #counterpart for url_for()
        # return render_template('control.html', userName = user.get('name'), userGroup = user.get('group'), userID = user.get('id'))

        # 관리자라면 사용자 이름 전부 가져오기
        userNameList = None
        # if user.get('group') == 'admin':
        if user['group'] == 'admin':
            userNameList = name_list
            print("\nuserNameList => \n", userNameList)

        return render_template('control.html', userName = user.get('name'), userGroup = user.get('group'), userNameList=userNameList)
        # return render_template('control.html', userName = '변진환', userGroup = user.get('group'), userNameList=userNameList)




@app.route('/login/', methods=['POST'])
def loginCheck():
    if request.method =='POST':
        
        # print(login_info['id'], login_info['pw'])
        login_info = request.form

        userCheck = isUser(login_info['id'], login_info['pw'])
        # data = {'LoginID': login_info['id'], 'LoginPass': login_info['pw']}
        # # api에 전송
        # res = api_req.post('https://carstat.co.kr/api/user/cs/auth', data=data)

        if userCheck['success'] == True: # 200일 경우 정상
            # session 1 : json으로 전송 시 
            # idCheck = json.dumps(user_info[login_info['id']]) 
            # session['user'] = idCheck # 배포용
            # session['user'] = json.dumps(user_info['LEEHANEUL'])

            # session 2 : id data 만 전송 시 
            # 이렇게 보내도 되는지?(실행은 됨) web 상에서 데이터 전송 시에는 데이터 타입 json으로 보내야된다고 들었는디,,
            # session['user'] = login_info['id'] 

            # url_for 로 id data 전송 시 : 문제점 : url에 id값이 그대로 표기됨. id만 변경하면 다른 유저pc로 이동가능할 듯.
            # return redirect(url_for('controlPC', user=login_info['id']))

            # 로그인 아이디로 앞으로 전송 예정
            login_ob = User(login_info['id'], login_info['pw']) # 배포용

            login_user(login_ob)

            print('\nlogin complete by : ', login_info['id'], '\n')      
            return redirect(url_for('controlPC'))

        print('\nlogin failed')
        return render_template('home.html', loginFail=True)
    
# @app.route()



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=18888, debug=True)
    