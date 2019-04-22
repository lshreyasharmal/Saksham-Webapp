from django.shortcuts import render
from django.views.generic import TemplateView
from .firebase_data import get_db
from google.cloud import storage, exceptions


def get_date(ts,type):
    if(type=='inj'):
        from datetime import datetime
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        return date
    from datetime import datetime,timedelta
    ts /= 1000
    date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
    return date
def get_time(ts,type):
    if(type=='inj'):
        from datetime import datetime
        date = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')
        return date
    from datetime import datetime,timedelta
    ts/=1000
    time = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')
    return time


def get_patients(request):
    db = get_db()
    patients = db.collection(u'patients').get()
    patients_info = {}
    for p in patients:
        p_dict = p.to_dict()
        patients_info[p_dict[u'id']] = p_dict[u'name']

    context = {
        "patients" : patients_info,
    }

    return render(request,'main.html',context)
def get_medication(db, my_id):
    patient_dates = db.collection(u'patient_med_dates').document(my_id).collection(u'dates').get()
    dates = {}
    print(patient_dates)
    for items in patient_dates:
        dates = items.to_dict()
    if(dates==[]):
        return None
    
    medication = {}
    j=1
    patient_document = db.collection(u'patient_med_logs').document(my_id)

    for d in dates:
        med_collection = patient_document.collection(d).get()

        for med in med_collection:
            medication[j]={
                'index' : j,
                'med_name' : med.to_dict()['name'],
                'time' : get_time(med.to_dict()['timestamp'],"med"),
                'date' : get_date(med.to_dict()['timestamp'],"med"),
                'status' : med.to_dict()['taken']
            }
            j=j+1
    return medication

def get_daily_routine(db,my_id):
    patient_dates = db.collection(u'patient_dr_dates').document(my_id).collection("dates").get()
    dicts = []
    for items in patient_dates:
        dicts.append(items.to_dict())
    if(dicts==[]):
        return None
    dates = dicts[0].keys()
    tasks = dicts[1].keys()
    dr_database = db.collection(u'patient_daily_rout_logs').document(my_id)
    daily_routine = {}
    j = 1
    for date in dates:
        for task in tasks:
            dr_collection = dr_database.collection(date).document(task).collection("details").get()
            if dr_collection:
                for item in dr_collection:
                    daily_routine[j] = {
                        'index' : j,
                        "task_name" : item.to_dict()['name'],
                        "time" : get_time(item.to_dict()['timestamp'],"dr"),
                        "date" : get_date(item.to_dict()['timestamp'],"dr"),
                        "status" : True if item.to_dict()['done']==1 else False
                    }
                    j+=1
                
    return daily_routine

def get_injection_schedule(db,my_id):
    patient_dates = db.collection(u'patient_injr_dates').document(my_id).collection(u'dates').get()
    dates = {}
    print(patient_dates)
    for items in patient_dates:
        dates = items.to_dict()
    if(dates==[]):
        return None
    
    injection = {}
    j=1
    patient_document = db.collection(u'patient_inj_logs').document(my_id)

    for d in dates:
        inj_collection = patient_document.collection(d).get()

        for inj in inj_collection:
            injection[j]={
                'index' : j,
                'inj_name' : inj.to_dict()['name'],
                'time' : get_time(int(inj.to_dict()['timeStamp']),"inj"),
                'date' : get_date(int(inj.to_dict()['timeStamp']),"inj"),
                'status' : inj.to_dict()['status']
            }
            j=j+1
    return injection


def get_patient_info(request,my_id):
    db = get_db()

    patient_info = db.collection("user_profile").document(my_id).collection("patient").document("info").get().to_dict()
    medication = get_medication(db, my_id)
    daily_routine = get_daily_routine(db, my_id) 
    injection = get_injection_schedule(db,my_id)      
  
    context = {
        "id" : my_id,
        'medication' : medication,
        'daily_routine' : daily_routine,
        'injection' : injection,
        'patient_info' : patient_info
    }
    return render(request,'patient_profile.html',context)