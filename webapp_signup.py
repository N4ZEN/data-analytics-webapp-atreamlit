import streamlit as st
import pandas as pd
import base64


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def download_link(object_to_download, download_filename, download_link_text):
	if isinstance(object_to_download,pd.DataFrame):
		object_to_download = object_to_download.to_csv(index=False)
		b64 = base64.b64encode(object_to_download.encode()).decode()
	return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'



def main():
	"""Simple Login App"""

	st.title("Simple Login App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Data","Analytics","Profiles"])
				if task == "Add Data":
					st.subheader("Upload dataset")

					menu = ["Home","Dataset","DocumentFiles","About"]
					choice = st.sidebar.selectbox("Menu",menu)

					if choice == "Dataset":
						st.subheader("Dataset")
						data_file = st.file_uploader("Upload CSV",type=['csv'])
						if st.button("Process"):
							if data_file is not None:
								file_details = {"Filename":data_file.name,"FileType":data_file.type,"FileSize":data_file.size}
								st.write(file_details)
								df = pd.read_csv(data_file, encoding = "ISO-8859-1")
								st.dataframe(df)
				

								if st.button('Download Dataframe as CSV'):
									tmp_download_link = download_link(df, 'YOUR_DF.csv', 'Click here to download your data!')
									st.markdown(tmp_download_link, unsafe_allow_html=True)
					else:
						st.subheader("About")
						st.info("Built by: Mariyam Nazaa Zuhair")
						st.text("Mariyam Nazaa Zuhair")


				elif task == "Analytics":
					st.subheader("Analytics")
				elif task == "Profiles":
					st.subheader("User Profiles")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")


	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()

