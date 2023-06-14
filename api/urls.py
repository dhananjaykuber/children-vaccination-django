from django.urls import path
from . import views

urlpatterns = [
    path("hospital-register/", views.hospital_register, name="hospital_register"),
    path("hospital-login/", views.hospital_login, name="hospital_login"),
    path("children-register/", views.children_register, name="children_register"),
    path("children-detail/<id>", views.children_detail, name="children_detail"),
    path("children-update/<id>", views.children_update, name="children_update"),
    path("children-list/", views.children_list, name="children_list"),
    path("children-delete/<id>", views.children_delete, name="children_delete"),
    path("vaccination-date/<date>", views.vaccination_date, name="vaccination_date"),
    path(
        "vaccination-update/<id>", views.vaccination_update, name="vaccination_update"
    ),
]
