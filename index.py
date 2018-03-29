import os
import MySQLdb
import datetime
now = datetime.datetime.now()
from flask import Flask,request,render_template,session,redirect
from werkzeug import secure_filename
from database import insert,select,update,delete,encrypt
con=MySQLdb.connect("localhost","root","root","media")
obj=con.cursor()
select=select()
insert=insert()
update=update()
delete=delete()
encrypt=encrypt()
video_list=[".mp4",".ogg",".mkv",".avi",".swf"]
album=""
profile=""
cover_pic=""
app=Flask(__name__)
app.secret_key = "suresh"
app.config['activity'] = "static/img/uploads/activities"
app.config['Dp'] = "static/img/uploads/Dp"
app.config['cover'] = "static/img/uploads/cover_picture"

#testing

@app.route("/test" , methods=['POST','GET'])
# def test():
# 	data=select.test(32)
# 	return render_template("test.html",data=data)
def test():
	data=encrypt.encrypt("suresh")
	return data
@app.route("/")
def login():
	return render_template("login.html")

#Login validated Function
@app.route("/login_validate",methods=['POST','GET'])
def login_validate():
	user_id=request.form['user_id'] 
	password=request.form['password'] 
	if user_id=="" or password=="":
		return render_template("login.html",data="Please Enter the vaild User name or password")	
	else:
		password=encrypt.encrypt(password)
		print password
		data=select.login(user_id,password)
		if (data):
			session['id']=data[0]
			session['user_id']=data[1]
			session['user_name']=data[4]
			session['photo']=data[8]
			now = datetime.datetime.now()
			insert.session(data[0],data[4],data[8],now)
			return redirect("/dashboard")
		else:
			return render_template("login.html",data="Please Enter the vaild User name or password")


#SIGN UP PAGE
@app.route("/sign_up")
def sign_up():
	success=0
	return render_template("sign_up.html",success=success)

@app.route("/validate_signup",methods=['POST','GET'])
def validate():
	success=0
	user_id=request.form['user_id']
	mail_id=request.form['mail_id']
	if(mail_id=="" or user_id==""):
		return render_template("sign_up.html",success=success,data="enter both the UserId and email id")
	else:
		data=select.exit_users(user_id,mail_id)
		if(data):
			success=0
			return render_template("sign_up.html",success=success,data="userID or email id already exits")
		else:
			success=1
			return render_template("sign_up.html",success=success,user_id=user_id,mail_id=mail_id)

@app.route("/tem_signup",methods=['POST','GET'])
def tem_signup():
	user_id=request.form['user_id']
	mail_id=request.form['mail_id']
	user_name=request.form['user_name']
	dob=request.form['dob']
	gender=request.form['gender']
	phone=request.form['phone']
	files=request.files['file']
	password=request.form['password']
	repeat_pass=request.form['rep_pass']
	if(password== repeat_pass):
		password=encrypt.encrypt(password)
		if (files):
			filename = secure_filename(files.filename)
			filename1=filename
			files.save(os.path.join(app.config['Dp'], filename))
			now = datetime.datetime.now()
			os.rename("static/img/uploads/Dp/"+str(filename),"static/img/uploads/Dp/"+"media_"+user_id+"_"+str(now)+filename1)
			file="media_"+user_id+"_"+str(now)+filename1
		else:
			if(gender=="Male"):
				files=user_name[0].lower()
				file="alphabets/"+files+".jpg"
			else:
				files=user_name[0].lower()
				file="alphabets/"+files+"f.jpg"
		insert.signups(user_id,mail_id,user_name,password,phone,dob,gender,file)
		return redirect("/")
	else:
		success=1
		return render_template("sign_up.html",success=success,user_id=user_id,mail_id=mail_id,user_name=user_name,dob=dob,gender=gender,phone=phone,file=files)
	



@app.route("/dashboard")
def index():
	id=session['id']
	user_id=session['user_id']
	user_name=session['user_name']
	profile=session['photo']
	theme=select.theme(id)
	user_profile=select.user_profile(id)
	#friend_request
	frnd_req_id=select.friend_request(id)
	if frnd_req_id==None:
		frnd_req_count=0
	else:
		frnd_req_count=len(frnd_req_id)
		frnd_req_details=[]
		for x in frnd_req_id:
			frnd_req_details.append(select.frnd_req_details(x))
	#select Activities and timelines
	data=[]
	data1=select.select_connections(id)
	data.append(data1)
	data2=select.select_connections2(id)
	data.append(data2)
	# print data
	fid=[]
	fid.append(id)
	for x in data:
		if(x!=None):
			for y in x:
				fid.append(y)
	# print fid
	profile_pic=[]
	for x in fid:
		profile_pic.append(select.select_profile_data(x))
	activity=[]
	for x in fid:
		data=select.activities(x)
		activity.append(data)
	activities=[]
	for x in activity:
		for y in x:
			activities.append(y)
	like_list=[]
	for y in activities: 
		data=select.select_likes(y[0])
		for x in data:
			like_list.append(select.select_profile_data(x[0]))

	#online session 
	online_frnd=select.select_session(id)

	activity=reversed(activities)
	return render_template("index.html",video_list=video_list,theme=theme,my_profile=user_profile,frnd_req_count=frnd_req_count,activities=activity,frnd_req_details=frnd_req_details,profile_pic=profile_pic,sessions=online_frnd,likes=like_list,data=data)

@app.route("/edit" , methods=['POST','GET'])
def edit():
	user_id=session['id']
	mail_id=request.form['mail_id']
	user_name=request.form['user_name']
	dob=request.form['dob']
	gender=request.form['gender']
	phone=request.form['phone']
	files=request.files['file']
	cover=request.files['cover_pic']
	password=request.form['password']
	data=select.select_pass(user_id);
	password=encrypt.encrypt(password)
	if(data[0]==password):
		if(files):
			filename = secure_filename(files.filename)
			filename1=filename
			files.save(os.path.join(app.config['Dp'], filename))
			now = datetime.datetime.now()
			os.rename("static/img/uploads/Dp/"+str(filename),"static/img/uploads/Dp/"+"media_"+str(user_id)+"_"+str(now)+filename1)
			file="media_"+str(user_id)+"_"+str(now)+filename1
		else:
			file=session['photo']
		if(cover):
			filename = secure_filename(cover.filename)
			filename1=filename
			cover.save(os.path.join(app.config['cover'], filename))
			now = datetime.datetime.now()
			os.rename("static/img/uploads/cover_picture/"+str(filename),"static/img/uploads/cover_picture/"+str(user_id)+"_"+"media_"+"cover_pic"+str(now)+filename1)
			cover=str(user_id)+"_"+"media_"+"cover_pic"+str(now)+filename1
		else:
			cover=select.select_cover(user_id)
			cover=cover[0]
		update.edit_profile(user_name,mail_id,phone,dob,gender,file,cover,user_id)
		return redirect("/dashboard")
	else:
		return "incorret password";

@app.route("/like/<post_id>",methods=['POST','GET'])
def likes(post_id):
	user_id=session['id']
	update.update_likes(post_id,user_id)
	return redirect("/dashboard")

@app.route("/view_likes/<post_id>",methods=['POST','GET'])
def veiw_likes(post_id):
	data=select.select_likes(post_id)
	# print data
	post=select.select_post(post_id)
	posted_user=select.select_post_user(post[1])
	like_list=[]
	for x in data:
		like_list.append(select.select_profile_data(x[0]))
	print like_list
	data_list=[]
	for x in data:
		for y in like_list:
			if(y[0]==x[0]):
				a=(y[0],y[1],y[2],x[1])
				data_list.append(a)
				break;
	return render_template("like_comment.html",liked_list=data_list,post=post,posted_user=posted_user,s=1)
@app.route("/post_comment/<post_id>",methods=['POST','GET'])
def comment(post_id):
	user_id=session['id']
	comment=request.form['comment']
	files=request.files['attachment']
	if(comment or files):
		if(files):
				filename = secure_filename(files.filename)
				filename1=filename
				files.save(os.path.join(app.config['activity'], filename))
				now = datetime.datetime.now()
				os.rename("static/img/uploads/activities/"+str(filename),"static/img/uploads/activities/"+str(user_id)+"comment"+"_"+"media_"+str(now)+filename1)
				file=str(user_id)+"comment"+"_"+"media_"+str(now)+filename1
		else:
			file=0
		update.update_comment(post_id,user_id)
		insert.insert_comment(post_id,user_id,comment,file)
	return redirect("/dashboard")

@app.route("/view_comments/<post_id>",methods=['POST','GET'])
def veiw_comments(post_id):
	data=select.select_comments(post_id)
	post=select.select_post(post_id)
	# print post
	posted_user=select.select_post_user(post[1])
	# print posted_user
	comment_list=[]
	for x in data:
		comment_list.append(select.select_profile_data(x[0]))
	data_list=[]
	for x in data:
		for y in comment_list:
			if(y[0]==x[0]):
				time=str(x[4])
				t="\t"+time[10:16]+ " " +time[0:10]
				a=(y[0],y[1],y[2],x[2],x[3],t)
				data_list.append(a)
				break;
	return render_template("like_comment.html",data=data,commented_list=data_list,post=post,posted_user=posted_user,s=0)


@app.route("/profile_setting/<id>",methods=['POST','GET'])
def settings(id):
	return  "sss"
@app.route("/delete_post/<id>",methods=['POST','GET'])
def delete_post(id):
	obj.execute("SELECT `post_attachement` FROM m_post WHERE id='%s'" %(id))
	data=obj.fetchone()
	for x in data:
		data=x
	if(data!=str(0)):
		os.remove("static/img/uploads/activities/"+data)
	delete.delete_post(id)

	return  redirect("/dashboard")


@app.route("/confirm_request/<frnd_id>",methods=['POST','GET'])
def confirm_request(frnd_id):
	id=session['id']
	update.confirm_request(id,frnd_id)
	return redirect("/dashboard")

@app.route("/ignore_request/<req_id>",methods=['POST','GET'])
def ignore_request(req_id):
	id=session['id']
	delete.ignore_request(req_id,id)
	return redirect("/dashboard")


@app.route("/upload_post",methods=['POST','GET'])
def upload():
	files=request.files['attachment']
	content=request.form['content']
	if(content or files):
		id=session['id']
		user_name=session['user_name']
		user_id=session['user_id']
		if(files):
			filename = secure_filename(files.filename)
			filename1=filename
			files.save(os.path.join(app.config['activity'], filename))
			now = datetime.datetime.now()
			os.rename("static/img/uploads/activities/"+str(filename),"static/img/uploads/activities/"+str(user_id)+"_"+"media_"+str(now)+filename1)
			file=str(user_id)+"_"+"media_"+str(now)+filename1
			insert.upload_post(id,content,file,0)
		else:
			file=0
			insert.upload_post(id,content,file,0)
	return redirect("/dashboard")

@app.route("/create_group/<id>",methods=['POST','GET'])
def create_group(id):


	return render_template("create_group.html")




@app.route("/theme",methods=['POST','GET'])
def theme():
	theme=request.form['theme']
	user_id=session['id']
	update.update_theme(theme,user_id)
	return redirect("/dashboard")


@app.route("/search",methods=['POST','GET'])
def search():
	q=request.form['q']

	user_id=session['user_id']
	id=session['id']
	user_name=session['user_name']
	profile=session['photo']
	if('@' in q):
		q=q[1:]
		result=select.search(q)
	# else:
	# 	result=select.search_frnd(q)
	# 	print result
	data=select.select_con(id,result[0])
	obj.execute("SELECT * FROM m_bp_friends WHERE  friend_user_id='%s' AND initiator_user_id='%s' " %(id,result[0]))
	data1=obj.fetchone()
	print data,data1
	if(data==None and data1==None ):
		s=1
	else:
		s=0
	return render_template("friends.html",result=result,user_id=id,user_name=user_name,profile=profile,s=s)


@app.route("/request/<req_id>")
def request_frnd(req_id):
	friend_id=req_id
	user_id=session['id']
	insert.request(user_id,friend_id)
	return redirect("/dashboard")


@app.route("/profile/<id>")
def profile(id):
	user_id=session['id']
	theme=select.theme(user_id)
	my_profile_data=select.user_profile(user_id)
	user_profile=select.user_profile(id)
	data=[]
	data1=select.select_connections(id)
	data.append(data1)
	data2=select.select_connections2(id)
	data.append(data2)
	fid=[]
	fid.append(id)
	for x in data:
		if(x!=None):
			for y in x:
				fid.append(y)
	profile_pic=[]
	for x in fid:
		profile_pic.append(select.select_profile_data(x))
	activity=[]
	for x in fid:
		data=select.activities(x)
		activity.append(data)
	activities=[]
	for x in activity:
		for y in x:
			activities.append(y)
	activity=reversed(activities)
	return render_template("profile.html",theme=theme,my_profile_data=my_profile_data,user_id=user_id,my_profile=user_profile,activities=activity,profile_pic=profile_pic)




@app.route("/mailn")
def mail():
	user_id=session['user_id']
	user_name=session['user_name']
	profile=session['photo']
	return render_template("mailbox.html",user_id=user_id,user_name=user_name,profile=profile)
@app.route("/compose")
def compose():
	user_id=session['user_id']
	user_name=session['user_name']
	profile=session['photo']
	return render_template("compose.html",user_id=user_id,user_name=user_name,profile=profile)

@app.route("/lockscreen")
def lockscreen():
	user_id=session['id']
	user_name=session['user_name']
	delete.pop_session(user_id)
	return render_template("lockscreen.html",user_name=user_name)
@app.route("/locklogin",methods=['POST','GET'])
def login1():
	password=request.form['password']
	user_id=session['user_id']
	user_name=session['user_name']

	if user_id=="" or password=="":
			return render_template("lockscreen.html",user_name=user_name,data="Please Enter the vaild password")	
	else:
		data=select.login(user_id,password)
		if (data):
			session['user_id']=data[1]
			session['user_name']=data[4]
			session['photo']=data[8]

			return redirect("/dashboard")
		else:
			return render_template("lockscreen.html",user_name=user_name,data="Please Enter the vaild password")



@app.route("/logout/<user_id>")
def logout(user_id):
	# theme=request.form['theme']
	user_id=user_id
	# update.update_theme(theme,user_id)
	delete.pop_session(user_id)
	session.pop('user_id',None)
	session.pop('user_name',None)
	session.pop('photo',None)
	return redirect("/")

if __name__=="__main__":
	app.run("127.0.0.1",8000,debug=True)
