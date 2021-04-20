from django.urls import path
from .views      import RateView

urlpatterns = [
        path('', RateView.as_view()),
]