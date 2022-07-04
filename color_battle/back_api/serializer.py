from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers as sr
from back_api import models

"""Serializers"""


class MapActionSerializer(ModelSerializer):
  """
    FO: add field 'group' in JWT token to reduce
        number of request to DB
    FO: don't need extra validation on user
        because it was checked in view
  """
  class Meta:
    model = models.MapAction
    fields = '__all__'


class CreatorsSerializer(ModelSerializer):

  class Meta:
    model = models.Creators
    fields = '__all__'


class CreatorsRequestSerializer(Serializer):
  w_username = sr.CharField()
  w_password = sr.CharField()