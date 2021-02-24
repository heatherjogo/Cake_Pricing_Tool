import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import Sequential, load_model

# Load models:
tiers = load_model('../models/tiers.h5')
type = load_model('../models/type.h5')

# Load Price Lookup Table as DataFrame:
price_df = pd.read_csv('price_lookup.csv', index_col=False)

# Setting up page as wide, and adding graphic at top.
st.set_page_config(layout="wide")
img = Image.open('Cake_Tool_Header.png')
st.image(img, use_column_width=True, caption="")

st.title('Custom Cake Pricing Tool')
st.write("Welcome! If you're a home baker and ever wondered if you are charging a fair price for your cakes, this is the place for you! This easy-to-use tool will help you determine a fair price range to consider for a given cake. Simply upload an image, select the width of the bottom layer of your cake, and the tool does the rest!")

#
st.header("Step 1: Upload Cake Image:")
st.write("Please try to upload images with minimal background clutter, and take the photo straight on, or from slightly above your cake. Birdseye images may not work.")
uploaded_file = st.file_uploader(label = '', type=['jpg', 'jpeg', 'png', 'bmp'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
#    st.image(image, caption='Uploaded Cake Image', width=100)
    resized = image.resize((400,400))
#    st.image(resized, caption='Resized and Reshaped Cake Image', use_column_width=300)
    row_1, row_2 = st.beta_columns((1,1))

    with row_1:
        st.write("**Original Uploaded Cake Image**")
        st.image(image, width=300)

    with row_2:
        st.write("**Resized & Reshaped Cake Image**")
        st.image(resized, width=300)
        st.write("*Ready to input to pricing model...*")
st.write("")

# Create Step 2 section:
st.header("Step 2: Input Cake Size")

col_1, col_2, col_3 = st.beta_columns(3)

size = col_1.selectbox('Select the base width of the bottom tier of your cake (in inches):',
    (4, 6, 7, 8, 9, 10, 12, 14, 16))
col_2.write(" ")
col_3.write(" ")

# Create Step 3 section:
st.header("Step 3: Get Recommended Price")
if st.button("Let's Go! >>"):
    image_to_model = Image.open(uploaded_file)
    resized_image = image_to_model.resize((400,400))
    input_arr = img_to_array(resized_image)
    input_arr = np.array([input_arr])
#    tier_preds = tiers.predict(input_arr)
#    tier_class = tiers.predict_classes(input_arr)
#    type_class = type.predict_classes(input_arr)
    tier_class = np.argmax(tiers.predict(input_arr), axis=-1)
    type_class = np.argmax(type.predict(input_arr), axis=-1)
    range = price_df.loc[(price_df['tiers'] == tier_class[0]) & (price_df['type'] == type_class[0]) & (price_df['base_size'] == size), ['low_range', 'high_range']]
#   st.write(range)
    st.subheader("The recommended price for your cake is: ")
    st.header(range['low_range'].values[0] + " to " + range['high_range'].values[0])




# if uploaded_file is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_file.getvalue()
#     st.write(bytes_data)
#
#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#     st.write(stringio)
#
#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)
#
#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)

# img = Image.open('giants.jpg')
# st.image(img, width=400, caption="Your Submitted Cake")
