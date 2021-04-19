from django.urls     import path

from products.views  import MenuView, ProductView

urlpatterns = [
    path('/detail/<int:product_id>', ProductView.as_view()),
    path('/menu-bar', MenuView.as_view()),
]
