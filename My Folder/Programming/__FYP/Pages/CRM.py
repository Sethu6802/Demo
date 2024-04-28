import streamlit as st 

from streamlit_option_menu import option_menu

from urllib3 import disable_warnings

from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

import pyrebase

from firebase_admin import db

firebaseConfig = {

    'apiKey': " AIzaSyCwdhswGJY5QMANM4bVO8XQmd1TJ08pM7Y ",

    'authDomain': "app001-97f05.firebaseapp.com",

    'projectId': "app001-97f05",

    'storageBucket': "app001-97f05.appspot.com",

    'messagingSenderId': "461483901137",

    'appId': "1:461483901137:web:df034f8dccc390a20c45f0",

    'measurementId': "G-RE5B8WK68Z",

    'databaseURL' : 'https://app002-f6090-default-rtdb.firebaseio.com/'

}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

db = firebase.database()



def signup(email,password):
    try:
        auth.create_user_with_email_and_password(email,password)

        st.toast("Registered New User Successfully")

        return 1
    
    except:

        login(e,p)

        return 0
    
    
def login(e,p):

    try:

        auth.sign_in_with_email_and_password(e,p)

        st.toast("Logged in Successfully")
    
    except:

        st.error('Invalid Credentials')

    
    
if 'clicked' not in st.session_state:

    st.session_state['clicked'] = False

if 'clicked' not in st.session_state:

    st.session_state.clicked = False

def click_button():

    st.session_state.clicked = True




st.header('Real-time Data Dashboard')

selected = option_menu(

    menu_title = None,

    options = ["Data Entry","Data Overview","Product DB"],

    icons = ["pencil-fill","database-fill-check","database-lock"],

    orientation = 'horizontal',

) 

if selected == 'Data Overview':

    st.write("Toggle to switch between Cutomers and Dealers ")

    x = st.toggle("Toggle Button")

    if x:

        users = db.child("users").order_by_child("Type").equal_to("Dealer").get()

        st.write(users.val())

    else:

        users = db.child("users").order_by_child("Type").equal_to("Customer").get()

        st.write(users.val())


if selected == 'Data Entry':
    
    with st.form("Enter Details here:",clear_on_submit = True):
        
        d = st.selectbox(label='Are you a Customer or a Dealer',options=['Customer','Dealer'])
    
        a = st.text_input(label='Enter Name')

        e = st.text_input(label='Enter Email')

        p = st.text_input(label='Enter Password')
    
        submit = st.form_submit_button(label = "Submit")
    
        if submit:

            if a != '':

                data = { "Name" : a, "Type" : d, "Email" : e, "Password" : p }

                y = signup(e,p)

                if y == 1:
                    
                    db.child("users").child(a).set(data)

                    st.toast("Submitted Details Successfully!")


if selected == 'Product DB':

    select = st.selectbox(label = '', options = ["Enter Product Details","Product Overview"])
    
    if select == 'Enter Product Details':

        with st.form("Product Details",clear_on_submit = True):
    
            prodName = st.text_input("Enter the name of the Product")
    
            prodQuantity = st.number_input("Enter Product quantity",min_value=1,max_value=100,step=1)

            submit = st.form_submit_button(label = "Submit")

            if submit:

                d = {"Name" : prodName, "Quantity" : prodQuantity}

                if prodName != '':

                    products = db.child("Products").order_by_child("Name").equal_to(prodName).get()

                    if products == '' :

                        db.child("Products").child(prodName).set(d)

                    else:

                        q = db.child("Products").child(prodName).get()

                        q1 = q.val()

                        q2 = q1['Quantity']

                        q2 -= prodQuantity

                        d = {"Name" : prodName, "Quantity" : q2}

                        db.child("Products").child(prodName).set(d)

                st.toast("Product Details Saved!")

    if select == 'Product Overview':

        products = db.child("Products").order_by_child("Name").get()

        st.write(products.val())

