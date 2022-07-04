from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers as sr
from back_api import models

"""Serializers"""


class MapActionSerializer(ModelSerializer):

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