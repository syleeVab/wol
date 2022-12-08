from ctypes import sizeof
from flask import Blueprint, render_template, request as fk_req, jsonify, url_for, redirect
import sys, hashlib, datetime, json
import requests as api_req


bp_login = Blueprint('login', __name__, url_prefix='/login')

@bp_login.route('/', methods=['POST'])
def loginCheck():
    if fk_req.method =='POST':
        # print(dir(fk_req))
        login_info = fk_req.form
        # print(login_info['id'], login_info['pw'])

        # api에 전송
        data = {'LoginID': login_info['id'], 'LoginPass': login_info['pw']}
        res = api_req.post('https://carstat.co.kr/api/user/cs/auth', data=data)

        if res.status_code == 200: # 200일 경우 정상
            return render_template('control.html')

        return render_template('home.html', loginFail=True)
    else:
        return render_template('home.html', connectFail=True)