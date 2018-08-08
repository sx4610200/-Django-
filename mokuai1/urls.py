from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
    url(r'^novel/$', views.novel),
    url(r'^usershome/$', views.userhome),
    url(r'^adminhome/$', views.adminhome),
    url(r'^loginpanel/$', views.loginpanel),
    url(r'^zhucepanel/$', views.zhucepanel),
    url(r'^login/$', views.login),
    url(r'^zhuce/$', views.zhuce),
    url(r'^loginout/$', views.loginout),
    url(r'^reg/$', views.reg),
    url(r'^createQR/$', views.createQR),
    url(r'^SubmitMessages/$', views.submitmessage),
    url(r'^messagespanel/$', views.messagespanel),
    url(r'^applysuccess/$', views.applysuccess),
    url(r'^applyrefuse/$', views.applyrefuse),
    url(r'^showImg/$', views.showImg),
    url(r'^allocation/$', views.allocation),
    url(r'^task/$', views.task),
    url(r'^money/$', views.money),
    url(r'^doctorhome/$', views.doctorhome),
    url(r'^writeapply/$', views.writeapply),
    url(r'^writeapplypannel/$', views.writeapplypannel),
    url(r'^delectusers/$', views.delectusers),
    url(r'^seemessagespanel/$',views.seemessagespanel),
    url(r'^seemessagesiomppanel/$',views.seemessagesiomppanel),

]
