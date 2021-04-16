from django.urls import path

from products.views  import MenuView

urlpatterns = [
    path('/menu-bar', MenuView.as_view())
]
