import streamlit as st
import numpy as np
import pickle
from pathlib import Path
import base64


# --- GENERAL SETTINGS ---
PAGE_TITLE = "Laptop Price Predictor"
PAGE_ICON = "💻"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

def add_bg_from_local(image_files):
    with open(image_files[0], "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    with open(image_files[1], "rb") as image_file:
        encoded_string1 = base64.b64encode(image_file.read())
    with open(image_files[2], "rb") as image_file:
        encoded_string2 = base64.b64encode(image_file.read())
    st.markdown(
    """
    <style>
      .stApp {
          background-image: url(data:image/png;base64,"""+encoded_string.decode()+""");
          background-size: cover;
      }
      .css-6qob1r.e1fqkh3o3 {
        background-image: url(data:image/png;base64,"""+encoded_string1.decode()+""");
        background-size: cover;
        background-repeat: no-repeat;
      }
      .css-1avcm0n.e8zbici2 {
        background-image: url(data:image/png;base64,"""+encoded_string2.decode()+""");
        background-size: cover;
        background-repeat: no-repeat;
      }
    </style>"""
    ,
    unsafe_allow_html=True
    )
add_bg_from_local([r'Purple_hexagonal.jpg', r'Purple_hexagonal.jpg',r'Purple_hexagonal.jpg'])



# import the model
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

# --- LOAD CSS---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.title("Laptop Predictor")

# brand
company = st.selectbox('Brand',df['Company'].unique())

# type of laptop
type = st.selectbox('Type',df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

# weight
weight = st.number_input('Weight of the Laptop')

# Touchscreen
touchscreen = st.selectbox('Touchscreen',['No','Yes'])

# IPS
ips = st.selectbox('IPS',['No','Yes'])

# screen size
screen_size = st.number_input('Screen Size')

# resolution
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

#cpu
cpu = st.selectbox('CPU',df['Cpu brand'].unique())

hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])

gpu = st.selectbox('GPU',df['Gpu brand'].unique())

os = st.selectbox('OS',df['os'].unique())

if st.button('Predict Price'):
    # query
    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'Yes':
        ips = 1
    else:
        ips = 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    try:
        ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
        query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,os],dtype='object')

        query = query.reshape(1,12)
        st.title("The predicted price of this configuration is " + str(int(np.exp(pipe.predict(query)[0]))))
    except Exception as e:
        st.write("Please don't enter 0 mention some value!")

