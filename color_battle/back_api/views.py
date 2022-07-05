from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import status
from back_api import serializer as ser
from back_api import models
from threading import Thread
import requests
import json


"""MICROSERVICE REQUESTS"""
def micro_set_color(data):
  data.pop('user', None)
  data.pop('date_time', None)
  requests.post(
    f'{settings.MAP_URL}/set_color',
    headers={
      'Content-Type': 'application/json'
    },
    data=json.dumps(data)
  )

def micro_save():
  res = requests.post(
    f'{settings.MAP_URL}/save',
    headers={
      'Content-Type': 'application/json'
    }
  )
  if res.status_code == 201:
    models.MapBackUp.objects.create(file=res.json()['file_path'])

"""Permisions"""
class IsBot(BasePermission):
  """
    FO: add field 'group' in JWT token to reduce
        number of request to DB
    FO: use 'group' from JWT token for permissions'
        check
  """
  def has_permission(self, request, view):
    t = request.user.has_perm('back_api.bot')
    return t

class IsTg(BasePermission):
  """Unnecessary validator"""
  def has_permission(self, request, view):
    t = request.user.has_perm('back_api.tg')
    return t

class IsWorker(BasePermission):
  """
    FO: add field 'group' in JWT token to reduce
        number of request to DB
    FO: use 'group' from JWT token for permissions'
        check
  """
  def has_permission(self, request, view):
    t = request.user.has_perm('back_api.worker')
    return t


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsWorker])
def set_color(request):
  """
    FO: add field 'group' in JWT token to reduce
        number of request to DB
    FO: use stateless authentification for workers
        because only id is needed
    FO: make bulk_create for batches of MapActions
  """
  rdata = dict(request.data)
  rdata.pop('date_time', None)
  rdata.pop('user', None)
  rdata['user'] = request.user.id
  sr = ser.MapActionSerializer(data=rdata)
  if sr.is_valid():
    Thread(target=micro_set_color, args=(sr.validated_data.copy(),)).start()
    inst = sr.save()
    
    if not (inst.id % settings.BACKUP_STEP):
      Thread(target=micro_save).start()
    return Response(status=status.HTTP_201_CREATED)
  return Response(data={'error':sr.errors},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsBot])
def tg_new_player(request):
  """
    FO: add field 'group' in JWT token to reduce
        number of request to DB
    FO: use stateless authentification for bots
        because only id is needed
  """
  creator_workers = models.Creators.objects.filter(owner=request.data['owner'])
  rsr = ser.CreatorsRequestSerializer(many=True)
  if len(creator_workers):
    rsr.instance = creator_workers
    return Response(data=rsr.data, status=status.HTTP_200_OK)

  worker, username, password = models.create_worker()
  data = {
    'owner': request.data['owner'],
    'worker': worker.id,
    'bot': request.user.id,
    'w_username': username,
    'w_password': password
  }
  sr = ser.CreatorsSerializer(data=data)
  if sr.is_valid():
    sr.save()
    rsr.initial_data = [{
      'w_username': username,
      'w_password': password
    }]
    rsr.is_valid(True)
    return Response(data=rsr.validated_data, status=status.HTTP_201_CREATED)
  return Response(data={'errors':sr.errors},status=status.HTTP_400_BAD_REQUEST)
