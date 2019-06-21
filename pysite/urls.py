"""pysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

import guestbook.views as guestbook_views
import main.views as main_views
import user.views as user_view

urlpatterns = [
    path('', main_views.index),

    path('user/joinform', user_view.joinform),
    path('user/join', user_view.join),
    path('user/joinsuccess', user_view.joinsuccess),
    path('user/login', user_view.login),
    path('user/loginform', user_view.loginform),
    path('user/logout', user_view.logout),
    path('user/updateform', user_view.updateform),
    path('user/update', user_view.update),
    path('user/api/checkemail', user_view.checkemail),

    path('guestbook/deleteform/<int:id>', guestbook_views.deleteform),
    path('guestbook/', guestbook_views.list),
    path('guestbook/add', guestbook_views.add),
    path('guestbook/delete', guestbook_views.delete),


    path('admin/', admin.site.urls),
]
