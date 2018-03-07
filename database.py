import MySQLdb
con=MySQLdb.connect("localhost","root","root","media")
obj=con.cursor()
class insert:
  def signups(*data):

    obj.execute("INSERT INTO m_signups (`user_login`, `user_email`,`user_pass`) VALUES('%s','%s','%s')" %(data[1],data[2],data[4]))
    con.commit()
    obj.execute("INSERT INTO m_users (`user_login`, `user_email`,`display_name`,`user_pass`,`phone`,`dob`,`gender`,`photo`) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')" %(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]))
    con.commit()    
    return 1
  def upload_post(*data):
  	obj.execute("INSERT INTO m_post(`user_id`,`post_content`,`post_attachement`,`post_likes`) VALUES('%s','%s','%s','%s')" %(data[1],data[2],data[3],data[4]))
  	con.commit()
  def request(*data):

    obj.execute("INSERT INTO m_bp_friends (`initiator_user_id`, `friend_user_id`, `is_confirmed`) VALUES('%s','%s','%s')" %(data[1],data[2],0))
    con.commit()   
    return 1
  def session(*data):
  	obj.execute("SELECT * FROM  m_sessions WHERE user_id='%s'" %(data[1]))
	x=obj.fetchone()
	print x
	if(x):
	    # obj.execute("INSERT INTO m_sessions(`user_id`, `user_name`, `profile_pic`,`time`) VALUES('%s','%s','%s','%s')" %(data[1],data[2],data[3],data[4]))
	    # con.commit()   
	    print x
	else:
		obj.execute("INSERT INTO m_sessions(`user_id`, `user_name`, `profile_pic`,`time`) VALUES('%s','%s','%s','%s')" %(data[1],data[2],data[3],data[4]))
		con.commit() 
	

class update:
	def user_edit(*data):
		obj.execute("UPDATE temp_login SET password='%s',authority='%s',time_stamp=now(),user_name='%s',access='%s',dept='%s' WHERE user_id='%s';" %(data[3],data[6],data[2],data[4],data[5],data[1]))
		con.commit()
	def confirm_request(*data):
		obj.execute("UPDATE m_bp_friends SET is_confirmed='%s' WHERE initiator_user_id='%s' AND friend_user_id='%s';" %(1,data[2],data[1]))
		con.commit()
	def update_likes(*data):
		obj.execute("SELECT `post_likes` FROM m_post WHERE id='%s' ;" %(data[1]))
		like=obj.fetchone()
		likes=like[0]+1
		obj.execute("UPDATE m_post SET post_likes='%s' WHERE id='%s';" %(likes,data[1]))
		con.commit()
		#likes details
		obj.execute("SELECT `count` FROM m_likes WHERE post_id='%s' AND user_id='%s' ;" %(data[1],data[2]))
		count=obj.fetchone()
		if(count):
			count=count[0]+1
			obj.execute("UPDATE m_likes SET count='%s' WHERE post_id='%s' AND user_id='%s';" %(count,data[1],data[2]))
			con.commit()
		else:
			obj.execute("INSERT INTO m_likes(`post_id`,`user_id`,`count`) VALUES('%s','%s','%s')" %(data[1],data[2],1))
			con.commit()
	def edit_profile(*data):
		obj.execute("UPDATE m_users SET display_name='%s',user_email='%s',phone='%s',dob='%s',gender='%s',photo='%s',cover_pic='%s' WHERE ID='%s';" %(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]))
		con.commit()

class delete:

	def user_delete(*data):
		obj.execute("DELETE FROM temp_login WHERE user_id='%s'" %(data[1]))
		obj.execute("DELETE FROM staff WHERE user_id='%s'" %(data[1]))
		con.commit()

	def pop_session(*data):
		obj.execute("DELETE FROM m_sessions WHERE user_id='%s'" %(data[1]))
		con.commit()	

	def ignore_request(*data):
		obj.execute("DELETE FROM m_bp_friends WHERE initiator_user_id='%s' AND friend_user_id='%s'" %(data[1],data[2]))
		con.commit()	

	def delete_post(*data):
		obj.execute("DELETE FROM m_post WHERE id='%s'" %(data[1]))
		con.commit()	
	

class select:
	def login(*data):

		obj.execute("SELECT * FROM m_users WHERE user_login='%s' AND user_pass='%s'" %(data[1],data[2]))
		data=obj.fetchone();
		return data
	def select_cover(*data):
		obj.execute("SELECT `cover_pic` FROM m_users WHERE ID ='%s' " %(data[1]))
		data1=obj.fetchone()
		return data1

	def exit_users(*data):
		obj.execute("SELECT * FROM m_signups WHERE user_login='%s' OR user_email='%s'" %(data[1],data[2]))
		data=obj.fetchone();
		return data
	def select_user(*data):
		obj.execute("SELECT * FROM m_users WHERE ID='%s'" %(data[1]))
		data=obj.fetchone()
		return data		

	def search(*data):
		obj.execute("SELECT * FROM m_users WHERE user_login='%s'" %(data[1]))
		data=obj.fetchone()
		return data
	def friend_request(*data):
		obj.execute("SELECT `initiator_user_id` FROM m_bp_friends WHERE friend_user_id='%s' AND is_confirmed='%s'" %(data[1],0))
		data=obj.fetchall()
		return data
	def frnd_req_details(*data):
		obj.execute("SELECT * FROM m_users WHERE ID='%s' " %(data[1]))
		data=obj.fetchone()
		return data
	def select_connections(*data):
		obj.execute("SELECT `friend_user_id` FROM m_bp_friends WHERE initiator_user_id='%s' AND is_confirmed='1' " %(data[1]))
		data=obj.fetchall()
		return data
	def select_connections2(*data):
		obj.execute("SELECT `initiator_user_id` FROM m_bp_friends WHERE friend_user_id='%s' AND is_confirmed='1' " %(data[1]))
		data=obj.fetchall()
		return data
	def activities(*data):
		obj.execute("SELECT * FROM m_post WHERE user_id='%s'" %(data[1]))
		data=obj.fetchall()
		return data
	def user_profile(*data):
		obj.execute("SELECT *FROM m_users WHERE ID='%s'" %(data[1]))
		data=obj.fetchone()
		return data
	def select_profile_data(*data):
		obj.execute("SELECT `ID`,`photo`,`display_name` FROM m_users WHERE ID='%s'" %(data[1]))
		data=obj.fetchone()
		return data
	def select_session(*data):
		obj.execute("SELECT * FROM m_sessions")
		data=obj.fetchall()
		return data		
	def select_likes(*data):
		obj.execute("SELECT `user_id`,`count`,`post_id` FROM m_likes WHERE post_id='%s'" %(data[1]))
		data=obj.fetchall()
		return data			
	def test(*data):
		obj.execute("SELECT m_likes.user_id,m_users.ID,m_users.display_name,m_users.photo,m_post.post_attachement,m_likes.count ,m_post.time FROM m_likes,m_post ,m_users WHERE m_likes.user_id =m_post.user_id ")
		# obj.execute("SELECT `ID` FROM m_users WHERE ID='%s'" %(data[1]))
		
		data=obj.fetchone()
		return data
	def select_pass(*data):
		obj.execute("SELECT `user_pass` FROM m_users WHERE  ID='%s' " %(data[1]))
		data=obj.fetchone()
		return data


if __name__=="__main__":
	update=update()
	select=select()
	insert=insert()
	delete=delete()