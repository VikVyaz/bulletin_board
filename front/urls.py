from django.urls import path

from front.apps import FrontConfig
from front.views import MainPageView, get_ad_list, user_login, ad_create, ad_detail, user_logout, reset_request

app_name = FrontConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),

    path('ads/list/', get_ad_list, name='ad_list'),
    path('ads/new/', ad_create, name='ad_new'),
    path('ads/<int:pk>/details/', ad_detail, name='ad_details'),
    # path('ads/<int:pk>/update/',, name = 'ad_update'),
    # path('ads/<int:pk>/delete/',, name = 'ad_delete'),
    #
    # path('feedback/list',, name = 'ad_list'),
    # path('feedback/new',, name = 'ad_new'),
    # path('feedback/<int:pk>/details/',, name = 'ad_details'),
    # path('feedback/<int:pk>/update/',, name = 'ad_update'),
    # path('feedback/<int:pk>/delete/',, name = 'ad_delete'),
    #
    path('user/login/', user_login, name='user_login'),
    path('user/logout/', user_logout, name='user_logout'),
    # path('user/register/', , name='user_register'),
    path('reset_request/', reset_request, name='user_password_reset_request'),
    # path('user/reset_confirm/', , name='user_password_reset_confirm'),
]
