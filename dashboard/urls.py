from django.conf.urls import url
from dashboard import views


urlpatterns = [
    url(r'^$', views.get_patients),
    url(r'^(?P<my_id>\w+)',views.get_patient_info),
]