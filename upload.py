import streamlit as st
import streamlit.components.v1 as stc
import base64

# File Processing Pkgs
import pandas as pd







def download_link(object_to_download, download_filename, download_link_text):
	if isinstance(object_to_download,pd.DataFrame):
		object_to_download = object_to_download.to_csv(index=False)
		b64 = base64.b64encode(object_to_download.encode()).decode()
	return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'



def main():
	st.title("Customer Segmentation App")

	menu = ["Home","Dataset","About"]
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
				# Examples

				if st.button('Download Dataframe as CSV'):
					tmp_download_link = download_link(df, data_file, 'Click here to download your data!')
					st.markdown(tmp_download_link, unsafe_allow_html=True)
	if choice == "About":
		st.text("Mariyam Nazaa Zuhair")


		
				

 


	else:
		st.subheader("About")
		st.info("Built by: Mariyam Nazaa Zuhair")
		st.text("Mariyam Nazaa Zuhair")







if __name__ == '__main__':
	main()