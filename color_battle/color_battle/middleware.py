
from typing import ByteString
from channels.auth import SessionMiddleware, CookieMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

"""VAR 2"""
class AsyncQueryJWTAuth(JWTAuthentication):

  async def authenticate(self, token):
    validated_token = await self.get_validated_token(token)

    return await self.get_user(validated_token)

  @database_sync_to_async
  def get_validated_token(self, raw_token):
    return super().get_validated_token(raw_token)

  @database_sync_to_async
  def get_user(self, validated_token):
    return super().get_user(validated_token)

"""VAR 1"""
@database_sync_to_async
def get_user(token):
  try:
    vtoken = AccessToken(token=token)
    return User.objects.get(id=vtoken['user_id'])
  except TokenError:
    return AnonymousUser()

def parse_query(query_string: ByteString):
  parsed = query_string.decode('utf-8').split('&')
  tokens = {}
  for item in parsed:
    token = item.split('=')
    tokens[token[0]] = '='.join(token[1:])
  return tokens


class QueryAuthMiddlewaer:

  def __init__(self, inner, *args, **kwargs):
    self.inner = inner

  # async def __call__(self, scope, recive, send):
  #   print(scope['headers'])
  #   tokens = parse_query(scope['query_string'])
  #   try:
  #     token = tokens['token']
  #     user = await get_user(token)
  #   except:
  #     user = AnonymousUser()
  #   scope['user'] = user
  #   return await self.inner(scope, recive, send)

  jwt_auth = AsyncQueryJWTAuth()
  async def __call__(self, scope, recive, send):
    tokens = parse_query(scope['query_string'])
    try:
      token = tokens['token']
      user = await self.jwt_auth.authenticate(token)
    except:
      # user = AnonymousUser()
      raise ValueError(
       "No user JWT token was sent"             
      )
    scope['user'] = user
    return await self.inner(scope, recive, send)

def QueryAuthStack(inner):
  return CookieMiddleware(SessionMiddleware(QueryAuthMiddlewaer(inner)))
  