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


st.header('Workshop')

selected = option_menu(

    menu_title = None,

    options = ["Materials","Produce"],

    icons = ["list-check","database","hammer"],

    orientation = 'horizontal',

) 


if selected == "Materials":

    toggle = st.toggle(label = "View Available Materials")

    if toggle:
         
        items = db.child("Materials").order_by_child("Name").get()
        
        st.write(items.val())

    else:
         
        with st.form("Order Materials ",clear_on_submit = True):
    
            Name = st.text_input("Enter the name of the material")
    
            Quantity = st.number_input("Enter quantity",min_value=1,max_value=100,step=1)

            submit = st.form_submit_button(label = "Submit")

            if submit:

                d = {"Name" : Name, "Quantity" : Quantity}

                if Name != '':

                    products = db.child("Materials").order_by_child("Name").equal_to(Name).get()

                    if products == '' or products == None:

                        db.child("Materials").child(Name).set(d)

                    else:

                        q = db.child("Materials").child(Name).get()

                        q1 = q.val()

                        if q1 == None:

                            db.child("Materials").child(Name).set(d)

                        else:
    
                            q2 = q1['Quantity']
    
                            q2 += Quantity
    
                            d = {"Name" : Name, "Quantity" : q2}
    
                            db.child("Materials").child(Name).set(d)

                    st.toast("Successfully Ordered!")

                else:

                    st.warning("Name cannot be empty")

if 'clicked' not in st.session_state:

    st.session_state['clicked'] = False

if 'clicked' not in st.session_state:

    st.session_state.clicked = False

def click_button():

    st.session_state.clicked = True



if selected == "Produce":
    
    products = db.child("Products").order_by_child("Name").get()

    option = list(products.val())

    with st.form("Select Item to Produce", clear_on_submit = True):
     
        item = st.selectbox(label = "Select an item to produce", options = option)
    
        if item == 'Kit':
    
            pen1 = db.child("Materials").child("Pen").child("Quantity").get()
    
            pen = pen1.val()
    
            pencil1 = db.child("Materials").child("Pencil").child("Quantity").get()
    
            pencil = pencil1.val()
    
            scale1 = db.child("Materials").child("Scale").child("Quantity").get()
    
            scale = scale1.val()
    
            maxi = max(pen,pencil,scale)
    
            amount = st.number_input("Enter Number of Items to Produce",min_value = 1,max_value = maxi, step = 1)
    
        submitted = st.form_submit_button("Submit",on_click = click_button())

        if submitted:
            
            if pen < amount or pencil < amount or scale < amount:
    
                st.error("Insufficient Materials. Order more to produce.")
    

            else:

               pen -= amount

               pencil -= amount

               scale -= amount

               data = {"Name" : "Pen", "Quantity" : pen}

               db.child("Materials").child("Pen").set(data)

               data = {"Name" : "Pencil", "Quantity" : pencil}

               db.child("Materials").child("Pencil").set(data)

               data = {"Name" : "Scale", "Quantity" : scale}

               db.child("Materials").child("Scale").set(data)

               st.toast("Order Success")

        itemQuantity = db.child("Products").child(item).child("Quantity").get()

        itemq = itemQuantity.val()

        q = itemq + amount

        g = {"Name" : item, "Quantity" : q}

        db.child("Products").child(item).set(g)