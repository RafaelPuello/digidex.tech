from django.urls import path

from .views import NameSuggestView, NameBackboneView, NameLookupView, NameUsageView

urlpatterns = [
    path('name_suggest/', NameSuggestView.as_view(), name='name_suggest'),
    path('name_backbone/', NameBackboneView.as_view(), name='name_backbone'),
    path('name_lookup/', NameLookupView.as_view(), name='name_lookup'),
    path('name_usage/', NameUsageView.as_view(), name='name_usage'),
]
