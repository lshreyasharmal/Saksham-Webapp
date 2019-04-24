from django.shortcuts import render
from django.views.generic import TemplateView
from .firebase_data import get_db
from google.cloud import storage, exceptions


def get_date(ts, type):
    if(type == 'inj'):
        from datetime import datetime
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        return date
    from datetime import datetime, timedelta
    ts /= 1000
    date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
    return date


def get_time(ts, type):
    if(type == 'inj'):
        from datetime import datetime
        date = datetime.utcfromtimestamp(ts).strftime('%H:%M:%S')
        return date
    from datetime import datetime, timedelta
    ts /= 1000
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
        "patients": patients_info,
    }

    return render(request, 'main.html', context)


def get_medication(db, my_id):
    patient_dates = db.collection(u'patient_med_dates').document(
        my_id).collection(u'dates').get()
    dates = {}
    # print(patient_dates)
    for items in patient_dates:
        dates = items.to_dict()
    if(dates == []):
        return None

    medication = {}
    j = 1
    patient_document = db.collection(u'patient_med_logs').document(my_id)

    for d in dates:
        med_collection = patient_document.collection(d).get()

        for med in med_collection:
            medication[j] = {
                'index': j,
                'med_name': med.to_dict()['name'],
                'time': get_time(med.to_dict()['timestamp'], "med"),
                'date': get_date(med.to_dict()['timestamp'], "med"),
                'status': med.to_dict()['taken']
            }
            j = j+1
    return medication


def get_daily_routine(db, my_id):
    patient_dates = db.collection(u'patient_dr_dates').document(
        my_id).collection("dates").get()
    dicts = []
    for items in patient_dates:
        dicts.append(items.to_dict())
    if(dicts == []):
        return None
    # print(dicts)
    dates = dicts[0].keys()
    tasks = dicts[1].keys()
    dr_database = db.collection(u'patient_daily_rout_logs').document(my_id)
    daily_routine = {}
    j = 1
    for date in dates:
        for task in tasks:
            dr_collection = dr_database.collection(
                date).document(task).collection("details").get()
            if dr_collection:
                for item in dr_collection:
                    daily_routine[j] = {
                        'index': j,
                        "task_name": item.to_dict()['name'],
                        "time": get_time(item.to_dict()['timestamp'], "dr"),
                        "date": get_date(item.to_dict()['timestamp'], "dr"),
                        "status": True if item.to_dict()['done'] == 1 else False
                    }
                    j += 1

    return daily_routine


def get_diet(db, my_id):
    patient_dates = db.collection(u'patient_dietr_dates').document(
        my_id).collection("dates").get()
    dicts = []
    for items in patient_dates:
        dicts.append(items.to_dict())
    if(dicts == []):
        return None
    # print(dicts)
    dates = dicts[0].keys()
    meals = dicts[1].keys()
    diet_database = db.collection(u'patient_diet_logs').document(my_id)
    diet_collection = {}
    j = 1
    for date in dates:
        # print(date)
        for meal in meals:
            # print(meal)
            diet = diet_database.collection(date).document(meal).get()
            # print(diet.to_dict())
            if diet.to_dict() != {}:
                for item in diet.to_dict():
                    # print("hhhhh")
                    # print(item)
                    # print(diet.to_dict())
                    diet_collection[j] = {
                        'index': j,
                        "meal_name": meal,
                        "items": diet.to_dict()[item],
                        "date": date

                    }
                    j += 1
    # print(diet_collection)

    return diet_collection


def get_injection_schedule(db, my_id):
    patient_dates = db.collection(u'patient_injr_dates').document(
        my_id).collection(u'dates').get()
    dates = {}
    # print(patient_dates)
    for items in patient_dates:
        dates = items.to_dict()
    if(dates == []):
        return None

    injection = {}
    j = 1
    patient_document = db.collection(u'patient_inj_logs').document(my_id)

    for d in dates:
        inj_collection = patient_document.collection(d).get()

        for inj in inj_collection:
            injection[j] = {
                'index': j,
                'inj_name': inj.to_dict()['name'],
                'time': get_time(int(inj.to_dict()['timeStamp']), "inj"),
                'date': get_date(int(inj.to_dict()['timeStamp']), "inj"),
                'status': inj.to_dict()['status']
            }
            j = j+1
    return injection


def get_phm(db, my_id):
    patient_dates = db.collection(u'patient_records_dates').document(
        my_id).collection(u'dates').get()
    dates = {}

    for items in patient_dates:
        dates = items.to_dict()
    if(dates == []):
        return None

    phm_dict = {}
    j = 1
    patient_collection = db.collection(
        u'records').document(my_id).collection("patient")

    for d in dates:
        phm_document = patient_collection.document(d).get()

        for key, value in phm_document.to_dict().items():
            phm_dict[j] = {
                'index': j,
                'date': d,
                'measurement': key,
                'value': str(value)
            }
            j = j+1
    return phm_dict


def get_activity_usage(db, my_id):
    print(my_id)
    patient_dates = db.collection(u'time_dates').document(my_id).collection("dates").get()
    
    dicts = []
    for items in patient_dates:
        dicts.append(items.to_dict())
        print(items.to_dict())
    if(dicts == []):
        return None

    dates = dicts[0].keys()
    module = dicts[1].keys()
    print(len(module))
    au_database = db.collection(u'time_spent').document(my_id)
    activity_usage = {}
    j = 1
    for date in dates:
        for name in module:
            print(name)
            au_document = au_database.collection(date).document(name).get()
            if(au_document.to_dict()):
                print(au_document.to_dict())
                activity_usage[j] = {
                    'index': j,
                    "module_name": au_document.to_dict()['activity_name'],
                    "date" : date,
                    "time": au_document.to_dict()['timeSpent']
                }
                print(j)
                j += 1
            else:
                print("oops")
                print(name)

    return(activity_usage)

def get_patient_info(request, my_id):
    db = get_db()

    patient_info = db.collection("user_profile").document(
        my_id).collection("patient").document("info").get().to_dict()
    medication = get_medication(db, my_id)
    daily_routine = get_daily_routine(db, my_id)
    injection = get_injection_schedule(db, my_id)
    diet = get_diet(db, my_id)
    physical_health = get_phm(db, my_id)
    activity_usage = get_activity_usage(db,my_id)
    print(activity_usage)

    context = {
        "id": my_id,
        'medication': medication,
        'daily_routine': daily_routine,
        'injection': injection,
        'physical_health' : physical_health,
        'diet': diet,
        'activity_usage' : activity_usage,
        'patient_info': patient_info
    }
    return render(request, 'patient_profile.html', context)
