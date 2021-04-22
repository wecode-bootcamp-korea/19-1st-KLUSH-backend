from django.urls     import path

from products.views  import MenuView, MainProductView, ProductView, CategoryView

urlpatterns = [
    path('/<int:product_id>', ProductView.as_view()),
    path('/menu-bar', MenuView.as_view()),
    path('/main', MainProductView.as_view()),
    path('/category', CategoryView.as_view()),
]
