from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='welcome'),
    url(r'^welcome/(?P<user_id>[0-9a-z\-]*)/$', views.welcome, name='welcome_with_id'),
#    url(r'^sign_in/$', views.sign_in, name='sign_in'),]

    url(r'^sign_in/$', views.SignInFormView.as_view() , name='sign_in'),


    url(r'^brainstorm/', views.brainstorm, name='brainstorm'),

    url(r'^logout/$', views.logout, name='logout'),

    url(r'^group/$', views.group_statements, name='group_statements'),
    url(r'^rate/$', views.rate_statements, name='rate_statements'),
    url(r'^thanks/$', views.thanks, name='thanks'),
]
