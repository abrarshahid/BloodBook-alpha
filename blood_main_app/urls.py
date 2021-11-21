
from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="startpage"),
    path('home/',views.index,name="home"),
    path('msg/',views.msg,name="message"),
    path('signup/',views.signup,name="signup"),
    path('login/',views.handlelogin,name="login"),
    path('chart/',views.chart,name="chart"),
    path('edit-profile/',views.edit,name="edit"),
    path('user-profile/<str:name>',views.profile,name="profile"),
    path('logout/',views.handlelogout,name="logout"),
    path('request/<str:donor>/',views.request_donor,name="request"),
    path('accept/<str:receiver>/',views.accept,name="accept"),
    path('emergency/',views.emergency,name="emergency"),
    path('received/',views.received,name="received"),
    path('p2p-accept/',views.p2p_accept,name="p2p-accept"),
    path('p2p-received/',views.p2p_received,name="p2p-received"),
    path('search/',views.search,name="search")

]

