from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import status
from back_api import serializer as ser


"""Permisions"""
class IsBot(BasePermission):
  def has_permission(self, request, view):
    t = request.user.has_perm('back_api.bot')
    return t

class IsTg(BasePermission):
  def has_permission(self, request, view):
    t = request.user.has_perm('back_api.tg')
    return t

class IsWorker(BasePermission):
  def has_permission(self, request, view):
    t = request.user.has_perm('back_api.worker')
    return t


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsWorker])
def set_color(request):
  return Response(data={'request':'from func'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsTg])
def tg_new_user(request):
  return Response(data={'request':'from func'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsBot])
def tg_bot_connect(request):
  return Response(data={'request':'from func'},status=status.HTTP_400_BAD_REQUEST)