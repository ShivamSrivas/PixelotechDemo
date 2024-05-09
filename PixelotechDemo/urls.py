"""PixelotechDemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from UserAuth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verification', views.UserVerification, name='Verification'),
    path('getAllUser', views.GetAllUser, name='GetAllUser'),
    path('getUserById/<int:user_id>', views.GetUserById, name='GetUserById'),
    path('getAllProduct', views.GetAllProduct, name='GetAllProduct'),
    path('getProductById/<int:product_id>', views.GetProductById, name='GetProductById'),
    path('userRegistration', views.UserRegistration, name='UserRegistration'),
    path('otpGeneration', views.OtpGeneration, name='OtpGeneration'),
    path('addProduct', views.AddProduct, name='AddProduct'),
    path('deleteProductById/<int:product_id>', views.DeleteProductById, name='DeleteProductById'),
    path('updateUser/<int:user_id>', views.UpdateUser, name='UpdateUser'),
    path('deleteUserById/<int:user_id>', views.DeleteUserById, name='DeleteUserById'),
]

urlpatterns+=staticfiles_urlpatterns()