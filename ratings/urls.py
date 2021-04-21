from django.urls import path
from .views      import RateView, CommentView

urlpatterns = [
        path('/comment/<int:product_id>', CommentView.as_view()),
        path('/comment', CommentView.as_view()),
        path('', RateView.as_view()),
]
