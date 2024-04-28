import streamlit as st

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_squared_error, r2_score


st.title('Stock Market Prediction')

uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])


if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.subheader('Raw data')

    st.write(data)

    st.subheader('Data preprocessing')


    data['Date'] = pd.to_datetime(data['Date'])

    data['Year'] = data['Date'].dt.year

    data['Month'] = data['Date'].dt.month

    data['Day'] = data['Date'].dt.day



    X = data[['Year', 'Month', 'Day']]

    y = data['Close']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    st.subheader('Model training')

    model = LinearRegression()

    model.fit(X_train, y_train)


    st.subheader('Model evaluation')

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)

    r2 = r2_score(y_test, y_pred)

    st.write('Mean Squared Error:', mse)

    st.write('R^2 Score:', r2)


    st.subheader('Make a prediction')


    year = st.slider('Year', min_value=2010, max_value=2030, value=2022)

    month = st.slider('Month', min_value=1, max_value=12, value=1)

    day = st.slider('Day', min_value=1, max_value=31, value=1)

    prediction = model.predict([[year, month, day]])

    st.write('Predicted Closing Price:', prediction[0])
