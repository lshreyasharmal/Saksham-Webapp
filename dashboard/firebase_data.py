def get_db():
    import pyrebase
    import os
    import firebase_admin
    from firebase_admin import credentials, firestore

    if (not len(firebase_admin._apps)):
        cred = credentials.Certificate(os.getcwd() + "\serviceAccountCredentials.json")
        default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db