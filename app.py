import streamlit as st
import Preprocessor
# from scrapper import raw_scrapper as rs, miscellaneous as mse

st.set_page_config(page_title="My Streamlit App", layout="wide")
st.title("Welcome to Sourcx Agency Research Tool")
st.subheader("Get all the information of an agency in just a few clicks")

# Define session state to store raw_data
if "raw_data" not in st.session_state:
    st.session_state.raw_data = None

Cookie = "AQEDASzx2XoCr5_IAAABldukTA0AAAGV_7DQDVYA0h-P6PVFJNrD4K3O-G-Z96D5r_W5EzW9xUozMI4ogRFvLXIF_QmdQTjCOHmg12W66gvkJJkp8kmgeHbQZYNmV_dgTXuuAGVFOKwHCHDUBAMH8Bnd"
linkedin_profile_data = None
with st.sidebar:
    st.header("Inputs")
    # website = st.text_input("Enter Website Homepage")
    linkedin_profile_url = st.text_input("Enter LinkedIn Profile")
    
    if linkedin_profile_url:
        if st.button("Scrape"):
            st.write("Fetching the Linkedin data...")
            linkedin_profile_data = Preprocessor.scrape_linkden_profile(Cookie, linkedin_profile_url)

if linkedin_profile_data:
    st.write("Linkedin Fetched successfully")
    st.title("Linkedin Data")
    st.json(linkedin_profile_data)

            
#             raw_data = 
#             st.session_state.raw_data = rs.website_node_profile_scrapper(website, Cookie, linkedin)
#             # mse.save_json(st.session_state.raw_data, "test.json")
#             st.write("Data fetched successfully")
#             # st.session_state.raw_data = str(rs.website_node_profile_scrapper(website, Cookie, linkedin))

# # # Display raw_data only if available
# if st.session_state.raw_data:
#     st.write(st.session_state.raw_data)

# if isinstance(st.session_state.raw_data, bytes):
#     try:
#         decoded_data = st.session_state.raw_data.decode('utf-8')
#         st.write(decoded_data)
#     except UnicodeDecodeError:
#         st.write("Error: Data is not in UTF-8 format.")



st.sidebar.write("---")
st.sidebar.write("Powered by SourX")
