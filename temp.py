
import os

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage, exceptions


cred = credentials.Certificate(os.getcwd() + "\serviceAccountCredentials.json")
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# d = db.collection(u'patients').get()
# for  f in d:
#     f_dict = f.to_dict()
#     print f_dict[u'id']
#     print f.to_dict()

# d = db.collection(u'patient_med_logs').document(u'PT00001').collection(u'20180729').get()
# for f in d:
#     print f.to_dict()

# d = db.collection(u'patient_med_logs').document('PT00001')

# try:
#     doc = d.get()
#     print(u'Document data: {}'.format(doc.to_dict()))
# except google.cloud.exceptions.NotFound:
#     print(u'No such document!')

# .document(u'PT00001').get()
# print d
# for f in d:
#     print f.to_dict()

# d = db.collection(u'patient_daily_rout_logs').document('PT2001').collection('08-31-18').get()
# for f in d:
#     print f.to_dict()


# d = db.collection(u'user_profile').document('PT2001').collection('patient').get()
# for f in d:
#     print f.to_dict()




# print d.get().to_dict()
# collection('08-31-18').document('Walk').collection('details').

# try:

#     doc = d.get()
#     print(u'Document data: {}'.format(doc.to_dict()))
# except google.cloud.exceptions.NotFound:
#     print(u'No such document!')



# d = db.collection("patient_dr_dates").document("PT2001").collection("dates")
# dd = d.get()
# dicts = []
# for f in dd:
#      dicts.append(f.to_dict())
# dates = dicts[0].keys()
# tasks = dicts[1].keys()
# print dates, tasks
# d = db.collection("patient_daily_rout_logs").document("PT2001")

# for date in dates:
#     for task in tasks:
#         dr_collection = d.collection(date).document(task).collection('details').get()
#         if dr_collection:
#             for drf in dr_collection:
#                 print drf.to_dict()
#         else:
#             print "ha"

my_id = "PT2001"
patient_info_doc = db.collection("user_profile").document(my_id).collection("patient").document("info").get()
patient_info = {}
print patient_info_doc.to_dict()

