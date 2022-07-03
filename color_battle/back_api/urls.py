from django.urls import path, include
from back_api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
  path('setcolor', views.set_color, name='setcolor'),
  path('tg/', include([
    path('new_user', views.tg_new_user, name='tg_new_user'),
    path('bot_connect', views.tg_bot_connect, name='bot_connect'),
  ])),

  path('token/', include([
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  ])),
]
