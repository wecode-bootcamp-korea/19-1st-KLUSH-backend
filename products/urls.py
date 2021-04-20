from django.urls     import path

from products.views  import MenuView, MainProductView, ProductView

urlpatterns = [
    path('/menu-bar', MenuView.as_view()),
    path('/main', MainProductView.as_view()),
    path('/category', ProductView.as_view()),
]
