from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'coffeapp'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name= 'home'),
    path('new-product/', views.createProduct, name='new-product'),
    path('products-page.', views.productsPage, name='products-page'),
    path('manage-product/',views.manageProduct, name='manage-product')
]



urlpatterns+= static(settings.MEDIA_URL, documnet_root= settings.MEDIA_ROOT)