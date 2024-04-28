from textblob import TextBlob

import pandas as pd

import streamlit as st

import cleantext

from PIL import Image


st.title('Product Management')

with st.expander('Analyze Text'):

    text = st.text_input('Enter Text:')

    if text:

        blob = TextBlob(text)

        st.write('Polarity: ',round(blob.sentiment.polarity),2)

        st.write('Subjectivity: ',round(blob.sentiment.subjectivity),2)
    
with st.expander('Process Text '):

    pre = st.text_input('Clean Text:')

    if pre:

        st.write(cleantext.clean(pre,clean_all=False,extra_spaces=True,stopwords=True,lowercase=True,numbers=True,punct=True))

with st.expander('Dataset Analysis'):

    upl = st.file_uploader('Upload File')
 
    
    if st.checkbox("Preview:"):

        df = pd.read_csv(upl,encoding='utf-8',encoding_errors='ignore')

        df['Review'] = df['selected_text']

        df['Analysis'] = df['sentiment']

        st.dataframe(df[['Review','Analysis']])

        @st.cache_data
        def convert_df(df):

            return df.to_csv().encode('utf-8')
        
        csv = convert_df(df)
        
        st.download_button(
            label="Download Data as CSV",

            data=csv,

            file_name = 'sentiment.csv',
            
            mime='text/csv',
        )

st.write('\n\n\n\n\n')

st.title('Product Analysis from Image Input')

uploaded_file = st.file_uploader('Choose Image to upload…', type = (["jpg", "jpeg"]))

if uploaded_file is not None:

    img = Image.open(uploaded_file)
    
    st.image(img, caption = 'Uploaded image') 
        