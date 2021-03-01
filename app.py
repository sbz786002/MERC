from flask import Flask, request,render_template,abort,send_from_directory
import json
import pyodbc
import re
import decimal
import secrets
#import os,inspect
import time
import os
from os.path import abspath
import base64
from pathlib import Path
from decimal import Decimal
from PIL import Image
from flask_cors import CORS
from GETExcel import New,listVal
import blurDetect as Blur
import login as lg
import GSTcheck as gst
import requests
from os.path import abspath
import os


app = Flask(__name__)
CORS(app)

def setConn(db):
	srIp = "192.168.5.178"
	userid = "ankur"
	pswrd = "cipl1234"
	if db=="IMAGEDB":
		db="ImageIdentification"
		srIp = "FS3"
		userid = "Merc"
		pswrd = "Ultimate@@9898"
	if db == "V21":
		db = "VirolaMarch21"
	if db=="VI":
		db="virola"
	if db=="VS":
		db="VirolaDomestic"
	if db=="TESTVI":
		db="Virola"
		srIp="192.168.5.157"
	if db=="TESTVS":
		db="VirolaDomestic"
		srIp="192.168.5.157"
	return 'Driver={SQL Server};''Server='+srIp+';''Database='+db+';''UID='+userid+';''PWD='+pswrd+';'

def dec_serializer(o):
    if isinstance(o, decimal.Decimal):
        return float(o)

@app.route('/',methods=['POST','GET'])
def newfile():
	return "Welcome to Virola"


@app.route('/api/v1/Payment/GetPaymentData',methods=['POST','GET'])
def Payments():
	token = request.headers.get('Authorization')
	#print(token)
	if token != 'c53fdd2cebc0552dbf994034ac9f4cca774c4ee609418a5a50954202acbf5e99366635c75518e8afb4a8c3432b79a13e4f5c6166bd7d836f0fad767edd3d1472':
		data = {"data":'Invalid Token',"status":400}
		return json.dumps(data,default=dec_serializer)
	Que = request.args.get('query')
	request_json = request.get_json()
	if not Que:
		data = {"data":'Query Not Inserted',"status":400}
		return json.dumps(data,default=dec_serializer)
	sts = setConn("IMAGEDB")
	if Que == 'CHANGE_PASSWORD' and not request_json:
		data = {"data":'request JSON Not Inserted',"status":400}
		return json.dumps(data,default=dec_serializer)

	if Que == 'CHANGE_PASSWORD':
		eoldpass = str(request_json['oldpassword'])
		enewpass = lg.encrpyt(str(request_json['newpassword']))
		ID = str(request_json['ID'])
		Que1 = 'select userid,username,pswrd from users where userid = ? and Active = 1'
		conn1 = pyodbc.connect(sts,autocommit=True)
		cur1 = conn1.cursor()
		cur1.execute(Que1,(ID))
		rv = cur1.fetchall()
		if len(rv) > 0:
			st = lg.dcrypt(rv[0][2])
			if st == eoldpass:
				Que = Que + " @ID = "+ID+", @newpassword='"+enewpass+"'"
			else:
				data = {"data":'Invalid userid and password',"Status":1000}
				return json.dumps(data,default=dec_serializer)
	exque = 'EXEC USP_FILL_COMMON_QUERY ?'
	try:
		conn = pyodbc.connect(sts,autocommit=True)
		cur = conn.cursor()
		cur.execute(exque,('EXEC '+Que))
		row_headers=[x[0] for x in cur.description]
		rv = cur.fetchall()
		json_data=[]
		if len(rv) == 0:
			data = {"data":json_data,"status":1000}
			return json.dumps(data,default=dec_serializer)
		conn.close()
		for result in rv:
			json_data.append(dict(zip(row_headers,result)))
		data = {"data":json_data,"status":1000}
		return json.dumps(data,default=dec_serializer)
	except Exception as e:
		x = str(e)
		data = {"data":x,"Status":500}
		return json.dumps(data,default=dec_serializer)
	

 
@app.route('/SaveFile', methods=['POST'])
def SaveFile():
	if request.method == 'POST':
		img = request.files['file']
		st = img.save('ExcelShare/'+img.filename)
		full_path = abspath('ExcelShare/'+img.filename)
		return str(full_path)
	else:
		abort(401)


@app.route('/SaveTemplateFile', methods=['POST'])
def SaveTemplateFile():
	if request.method == 'POST':
		img = request.files['file']
		portalName = request.args.get('portal')
		block = request.args.get('templateid')
		Path('Catalogue/'+portalName+'/'+block).mkdir(parents=True, exist_ok=True)
		st = img.save('Catalogue/'+portalName+'/'+block+'/'+img.filename)
		full_path = abspath('Catalogue/'+portalName+'/'+block+'/'+img.filename)
		return str(full_path)
	else:
		abort(401)


@app.route('/SaveImageVS', methods=['POST'])
def getImg():
    db = request.args.get('db')
    artid = request.args.get('artid')
    angle = request.args.get('angle')
    loginid = request.args.get('loginid')
    tp = request.args.get('tp')
    img = request.files['file']
    name = img.filename
    sts = setConn(db)
    my_string = base64.b64encode(img.read())
    Que = 'exec PSP_ImportImage ?,?,?,?,?'
    conn = pyodbc.connect(sts,autocommit=True)
    cur = conn.cursor()
    rv = cur.execute(Que,(my_string,artid,angle,tp,loginid))
    row_headers=[x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data=[]
    conn.close()
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data,default=dec_serializer)

@app.route('/api/v1/Common/GetDynamicQuery', methods=['GET','POST'])
def CommonQuery():

    Que = request.args.get('query')
    if not Que:
    	return "Query Not Inserted"
    db = request.args.get('db')
    if not db:
    	return "Database Not Selected"
    sts = setConn(db)
    exque = 'EXEC USP_FILL_COMMON_QUERY ?'
    try:
    	conn = pyodbc.connect(sts,autocommit=True)
    	cur = conn.cursor()
    	cur.execute(exque,(Que))
    	row_headers=[x[0] for x in cur.description]
    	rv = cur.fetchall()
    	json_data=[]
    	if len(rv) == 0:
    		data = {"data":json_data,"status":1000}
    		return json.dumps(data,default=dec_serializer)
    	conn.close()
    	for result in rv:
    		json_data.append(dict(zip(row_headers,result)))
    	data = {"data":json_data,"status":1000}
    	return json.dumps(data,default=dec_serializer)
    except Exception as e:
    	x = str(e)
    	data = {"data":x,"Que":Que}
    	return json.dumps(data,default=dec_serializer)


@app.route('/api/v1/Common/GetDynamicQueryNew', methods=['GET','POST'])
def CommonQueryNew():

    Que = request.headers.get('query')
    db = request.headers.get('db')
    if not Que:
    	return "Query Not Inserted"
    if not db:
    	return "Database Not Selected"
    sts = setConn(db)
    exque = 'EXEC USP_FILL_COMMON_QUERY ?'
    try:
    	conn = pyodbc.connect(sts,autocommit=True)
    	cur = conn.cursor()
    	cur.execute(exque,(Que))
    	row_headers=[x[0] for x in cur.description]
    	rv = cur.fetchall()
    	json_data=[]
    	if len(rv) == 0:
    		data = {"data":json_data,"status":1000}
    		return json.dumps(data,default=dec_serializer)
    	conn.close()
    	for result in rv:
    		json_data.append(dict(zip(row_headers,result)))
    	data = {"data":json_data,"status":1000}
    	return json.dumps(data,default=dec_serializer)
    except Exception as e:
    	x = str(e)
    	data = {"data":x,"Que":Que}
    	return json.dumps(data,default=dec_serializer)


@app.route('/login', methods=['GET','POST'])
def loginCheck():
	username = request.args.get('user')
	password = request.args.get('password')
	db = request.args.get('db')
	sts = setConn(db)
	if db=="IMAGEDB":
		Que = 'select userid,username,pswrd from users where Username = ? and Active = 1'
	else:
		Que = 'select userid,LoginName,pswrd from users where LoginName = ?'
	conn = pyodbc.connect(sts,autocommit=True)
	cur = conn.cursor()
	cur.execute(Que,(username))
	rv = cur.fetchall()
	if len(rv) > 0:
		st = lg.dcrypt(rv[0][2])
		userid = str(rv[0][0])
		if st == password:
			res = secrets.token_hex(64)
			cur1 = conn.cursor()
			Que1 = "EXEC USP_LOGIN_VARIFICATION ?,?"
			cur1.execute(Que1,(res,userid))
			rv1 = cur1.fetchall()
			ret = {"token":rv1[0][0],"userid":userid}
			return json.dumps(ret)
		else:
			ret = {"result":"Incorrect password"}
			return json.dumps(ret)
	else:
		ret = {"result":"User Not found"}
		return json.dumps(ret)


@app.route('/TokenVarification', methods=['GET','POST'])
def tokenCheck():
	token = request.headers.get('token')
	db = request.args.get('db')
	sts = setConn(db)
	Que = 'select userid from TokenAuth where token = ? and auth = 1'
	conn = pyodbc.connect(sts,autocommit=True)
	cur = conn.cursor()
	cur.execute(Que,(token))
	rv = cur.fetchall()
	if len(rv) > 0:
		ret = {"data":{"Valid":True}}
		return json.dumps(ret,default=dec_serializer)
	else:
		ret = {"data":{"Valid":False}}
		return json.dumps(ret,default=dec_serializer)


@app.route('/api/v1/Common/GetFillComboQuery', methods=['GET','POST'])
def fillcmbQuery():

    frmname = request.args.get('formname')
    quename = request.args.get('queryname')
    cnt = request.args.get('count')
    srchtext = request.args.get('searchtext')
    filters = request.args.get('filter')
    if not quename:
    	return "Query Not Inserted"
    db = request.args.get('db')
    if not db:
    	return "Database Not Selected"
    sts = setConn(db)
    exque = 'EXEC USP_FILL_COMBO_QUERY ?,?,?,?,?'
    try:
    	conn = pyodbc.connect(sts,autocommit=True)
    	cur = conn.cursor()
    	cur.execute(exque,(frmname,quename,cnt,srchtext,filters))
    	row_headers=[x[0] for x in cur.description]
    	rv = cur.fetchall()
    	json_data=[]
    	conn.close()
    	for result in rv:
    		json_data.append(dict(zip(row_headers,result)))
    	data = {"data":json_data,"status":1000}
    	return json.dumps(data,default=dec_serializer)
    except Exception as e:
    	return str(e)


@app.route('/Defects', methods=['POST'])
def Defects():
	if request.method == 'POST':
		img = request.files['file']
		st = img.save('outward/'+os.path.basename(img.filename))
		full_path = abspath('outward/'+os.path.basename(img.filename) )
		my_string = base64.b64encode(img.read())
		url = "http://192.168.5.2:7172/defects"
		payload={}
		files=[('file', open(full_path,'rb'))]
		headers = {'Authorization': 'Basic YWRtaW46c3Q='}
		response = requests.request("POST", url, headers=headers, data=payload, files=files)
		data = json.loads(response.text)
		sts = {"data":data,"status":1000}
		return sts
	else:
		abort(401)

@app.route('/SaveImg', methods=['POST','GET'])
def SaveImage():
	img = request.files['file']
	clmn = request.args.get('column')
	tbl = request.args.get('table')
	db = request.args.get('db')
	fld = request.args.get('Ufield')
	val = request.args.get('UValue')
	name = img.filename
	my_string = base64.b64encode(img.read())
	my_string = base64.b64decode(my_string)
	if not db:
		return "Database Not Selected"
	sts = setConn(db)
	Que = "Update "+tbl+" set "+clmn+" = ? output Inserted."+fld+" where "+fld+" = ?"
	try:
		conn = pyodbc.connect(sts,autocommit=True)
		cur = conn.cursor()
		cur.execute(Que,(my_string,val))
		row_headers=[x[0] for x in cur.description]
		rv = cur.fetchall()
		json_data=[]
		if len(rv) == 0:
			data = {"data":json_data,"status":1000}
			return json.dumps(data,default=dec_serializer)
		conn.close()
		for result in rv:
			json_data.append(dict(zip(row_headers,result)))
			data = {"data":json_data,"status":1000}
			return json.dumps(data,default=dec_serializer)
	except Exception as e:
		x = {}
		data = {"data":str(e)}
		return json.dumps(data,default=dec_serializer)


@app.route('/encrypt', methods=['POST','GET'])
def encrypt():
	val = request.args.get('password')
	st = lg.encrpyt(val)
	return st


@app.route('/dcrypt', methods=['POST','GET'])
def dcrypt():
	val = request.args.get('password')
	st = lg.dcrypt(val)
	return st

@app.route('/GetJSON2Excel',methods=['POST','GET'])
def GETExcel():
	request_json = request.get_json()
	st = New.getExcel(request_json)
	with open(st, "rb") as img_file:
		return (base64.b64encode(img_file.read()).decode('utf-8'))
	#return send_from_directory('GETExcel/','New.xlsx', as_attachment=True)

@app.route('/GetPortalExcel',methods=['GET','POST'])
def GetPortalExcel():
	rsj = request.get_json()
	template = request.headers.get('tempid')
	Portal = request.headers.get('portal')
	celladdress = request.headers.get('Range')
	Sheet = request.headers.get('SheetName')
	st = New.getPortalExcel(rsj,Portal,template,Sheet,celladdress)
	fl = ''
	with open(st[0],"rb") as img_file:
		fl = base64.b64encode(img_file.read()).decode('utf-8')
	dt = {"FileStr":fl,"FileName":st[1],"status":1000}
	return json.dumps(dt,default=dec_serializer)

@app.route('/GetdrpExcel',methods=['GET','POST'])
def GetdrpExcel():
	Que = request.args.get('que')
	st = New.getdrpExcel(Que)
	with open(st, "rb") as img_file:
		return (base64.b64encode(img_file.read()).decode('utf-8'))

@app.route('/GSTCheck',methods=['POST','GET'])
def checkGST():
	val = request.args.get('gstno')
	st = gst.check(val)
	return st

@app.route('/BlurDetect',methods=['POST'])
def blurdetect():
	img = request.files['file']
	st = img.save('outward/'+os.path.basename(img.filename))
	full_path = abspath('outward/'+os.path.basename(img.filename))
	st = Blur.main(full_path)
	return st

@app.route('/GetSheetAttribute',methods=['POST'])
def GetSheetAttribute():
	img = request.files['file']
	S_index = request.args.get('sindex')
	R_index = request.args.get('rindex')
	st = img.save('ExcelShare/'+img.filename)
	full_path = abspath('ExcelShare/'+img.filename)
	dt = New.getAttribute(full_path,R_index,S_index)
	data = {"data":dt,"status":1000}
	return json.dumps(data,default=dec_serializer)



if __name__ == "__main__":
	#app.run(host="192.168.5.179",port=7071)
	from waitress import serve
	serve(app)
    #from werkzeug.serving import run_simple
    #run_simple("0.0.0.0", 7071, app)
    #app.run(host="192.168.5.179",port=8071, ssl_context=context)