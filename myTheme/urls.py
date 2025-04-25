from django.contrib import admin
from django.urls import path
from myApp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.renderPage),
    path('signIn',views.signIn),
    path('signUp',views.signUp),
    path('saveRegister',views.saveRegister),
    path('checkLogin',views.checkLogin),
    path('renderExpense',views.renderExpense),
    path('saveExpense',views.saveExpense),

    path('renderIncome',views.renderIncome),
    path('saveIncome',views.saveIncome),
    path('viewExpense',views.viewExpense),
    path('viewIncome',views.viewIncome),
    path('logout',views.logout),
    path('dashBoard',views.dashBoard),
    path('searchExp',views.searchExp),
    path('updateExp',views.updateExp),
    path('deleteExp',views.deleteExp),
    path('adminViewUser',views.adminViewUser),
    path('deActiveUser',views.deActiveUser),
    path('deactiveUser',views.deactiveUser),
    path('activeUser',views.activeUser),
    path('adminHome',views.adminHome),
    path('openMessage',views.openMessage),
    path('saveMessage',views.saveMessage),
    path('requestedUser',views.requestedUser),
    path('requestActiveUser',views.requestActiveUser),
    
  
#     path('createAdmin',views.createAdmin),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
