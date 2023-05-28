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
add_bg_from_local([r'10340256_13077.jpg', r'10340256_13077.jpg',r'10340256_13077.jpg'])



# import the model
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

# --- LOAD CSS---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Heading of the Page
st.markdown("<h1 style='text-align: center; text-decoration: underline;'>Laptop Predictor</h1>", unsafe_allow_html=True)

# All inputs:
# brand
brand_options = df['Company'].unique().tolist()
brand_options.insert(0, 'Select an option')
company = st.selectbox('Brand', brand_options)

# type of laptop
type_options = df['TypeName'].unique().tolist()
type_options.insert(0, 'Select an option')
laptop_type = st.selectbox('Type', type_options)

# Ram
ram_options = [2, 4, 6, 8, 12, 16, 24, 32, 64]
ram_options.insert(0, 'Select an option')
ram = st.selectbox('RAM(in GB)', ram_options)

# weight
weight = st.number_input('Weight of the Laptop')

# Touchscreen
touchscreen_options = ['No', 'Yes']
touchscreen_options.insert(0, 'Select an option')
touchscreen = st.selectbox('Touchscreen', touchscreen_options)

# IPS
ips_options = ['No', 'Yes']
ips_options.insert(0, 'Select an option')
ips = st.selectbox('IPS', ips_options)

# screen size
screen_size = st.number_input('Screen Size (in inch)')

# resolution
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

#cpu
cpu_options = df['Cpu brand'].unique().tolist()
cpu_options.insert(0, 'Select an option')
cpu = st.selectbox('CPU', cpu_options)

# HDD
hdd_options = [0, 128, 256, 512, 1024, 2048, 4096]
hdd_options.insert(0, 'Select an option')
hdd = st.selectbox('HDD(in GB)', hdd_options)

# SSD
ssd_options = [0, 128, 256, 512, 1024, 2048]
ssd_options.insert(0, 'Select an option')
ssd = st.selectbox('SSD(in GB)', ssd_options)

# GPU
gpu_options = df['Gpu brand'].unique().tolist()
gpu_options.insert(0, 'Select an option')
gpu = st.selectbox('GPU', gpu_options)

# OS
if company == 'Apple':
    os_options = ['Mac']
else:
    os_options = [option for option in df['os'].unique() if option != 'Mac']
os = st.selectbox('OS', ['Select an OS'] + os_options)

# Prediction
if st.button('Predict Price'):
    # query
    if company == 'Select an option' or laptop_type == 'Select an option' or ram == 'Select an option' or \
            weight < 0.5 or touchscreen == 'Select an option' or ips == 'Select an option' or \
            screen_size == 0 or resolution == 'Select a resolution' or cpu == 'Select a CPU' or \
            (hdd == 'Select an option' and ssd == 'Select an option') or (hdd == 0 and ssd == 0) or gpu == 'Select a GPU' or os == 'Select an OS':
        st.error('Please select all specifications.')
    else:
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
            query = np.array([company,laptop_type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,os],dtype='object')

            query = query.reshape(1,12)
            st.title("The predicted price of this configuration is " + str(int(np.exp(pipe.predict(query)[0]))))
        except Exception as e:
            if hdd == 'Select an option':
                st.write("Please select 0 if your laptop doesn't contain any HDD")
            elif ssd == 'Select an option':
                st.write("Please select 0 if your laptop doesn't contain any SSD")
            else:
                st.write("Please don't enter 0, mention some value!")

