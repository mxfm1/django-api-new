from django.urls import path
from .views import CreateResidence,ResidenceDetailView,ListResidence,AddResidentView

urlpatterns = [
    path("create/",CreateResidence.as_view(),name="create_residence"),
    path("<str:identifier>/", ResidenceDetailView.as_view(),name="residence_detail_view"),
    path("",ListResidence.as_view(),name="residence_list_view"),
    path("<str:identifier>/add-resident",AddResidentView.as_view(),name="add_resident_view")
]
