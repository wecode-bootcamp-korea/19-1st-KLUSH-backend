from django.urls     import path

from products.views  import MenuView, MainProductView

urlpatterns = [
    path('/menu-bar', MenuView.as_view()),
    path('/main', MainProductView.as_view())
]
