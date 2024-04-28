from urllib3 import disable_warnings

from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyASdAH5zl3EmwYq7t-lq0ClnYp9faqq0gs",

    'authDomain': "app001-97f05.firebaseapp.com",

    'projectId': "app001-97f05",

    'storageBucket': "app001-97f05.appspot.com",

    'messagingSenderId': "461483901137",

    'appId': "1:461483901137:web:df034f8dccc390a20c45f0",

    'measurementId': "G-RE5B8WK68Z",

    'databaseURL' : 'https://console.firebase.google.com/project/app001-97f05/overview'

}

firebase = pyrebase.initialize_app(firebaseConfig)

'''auth = firebase.auth()

def signup():

    email = input("Enter Email: ")

    password = input("Enter Password: ")

    user = auth.create_user_with_email_and_password(email,password)

    print("Successfully created account!")

signup()'''