from django.urls import path, include
from back_api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
  path('setcolor', views.set_color, name='setcolor'),
  path('tg/', include([
    path('new_player', views.tg_new_player, name='tg_new_player'),
  ])),

  path('token/', include([
    path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  ])),
  path('internal', views.internal_msg, name='internal')

]
