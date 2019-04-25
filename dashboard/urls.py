from django.conf.urls import url
from dashboard import views


urlpatterns = [
    url(r'^$', views.get_patients),
    url(r'^(?P<my_id>\w+@\w+.\w+.\w+)',views.get_patient_info),
    url(r'^(?P<my_id>\w+)',views.get_patient_info),
]
