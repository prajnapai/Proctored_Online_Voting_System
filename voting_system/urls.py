"""voting_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from voting_system import views

# from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('election', views.election, name='election'),
    path('login_user/<int:eid>/', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('contactus', views.contactus, name='contactus'),
    path('authentication', views.authentication, name='authentication'),
    path('verify_user', views.verify_user, name='verify_user'),  #face
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('voting', views.voting, name='voting'),
    path('result/<int:eid>/', views.result, name='result'),
    path('cast_vote', views.cast_vote, name='cast_vote'),
    path('vote_success', views.vote_success, name='vote_success'),
    # path('face_proctoring', views.face_proctoring, name='face_proctoring'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)