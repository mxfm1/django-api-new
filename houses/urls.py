from django.urls import path
from .views import CreateResidence,ResidenceDetailView

urlpatterns = [
    path("create/",CreateResidence.as_view(),name="create_residence"),
    path("<str:identifier>/", ResidenceDetailView.as_view(),name="residence_detail_view")
]
