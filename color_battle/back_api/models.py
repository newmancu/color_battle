from django.db import models
from django.core.validators import RegexValidator, BaseValidator
from django.core.exceptions import ValidationError
from django.utils.regex_helper import _lazy_re_compile
from django.contrib.auth.models import User, Group
from django.conf import settings 
from django.contrib.auth.validators import UnicodeUsernameValidator
import random


"""Validators"""

class BaseUserGroupValidator(BaseValidator):
  message = "Ensure user group is %(limit_value)s (it is %(show_value)s)."
  code = "invalid"

  def __init__(self, limit_value, message=...):
    super().__init__(limit_value, message)

  
  def __call__(self, value):
    cleaned = self.clean(value)
    limit_value = (
      self.limit_value() if callable(self.limit_value) else self.limit_value
    )
    params = {"limit_value": limit_value, "show_value": cleaned, "value": value}
    if self.compare(cleaned, limit_value):
      raise ValidationError(self.message, code=self.code, params=params)

  def __eq__(self, other):
      if not isinstance(other, self.__class__):
          return NotImplemented
      return (
          self.limit_value == other.limit_value
          and self.message == other.message
          and self.code == other.code
      )

  def compare(self, a, b):
    print(a, type(a))
    return a.groups.filter(name=b).exists()


class TgUserValidator(BaseUserGroupValidator):
  """Unnecessary validator"""
  def __init__(self, message=...):
    super().__init__('TG', message)
  

class WorkerUserValidator(BaseUserGroupValidator):
  def __init__(self, message=...):
    super().__init__('Worker', message)


class BotUserValidator(BaseUserGroupValidator):
  def __init__(self, message=...):
    super().__init__('Bot', message)


color_validator = RegexValidator(
    # _lazy_re_compile(r"^#([0-9a-f]{3}|[0-9a-f]{6})\Z"),
    _lazy_re_compile(r"^#([0-9a-f]{6})\Z"),
    message="Enter a valid color.",
    code="invalid",
)

def validate_colro(value):
    return color_validator(value)


"""Fields"""
class ColorField(models.CharField):
  def __init__(self, *args, **kwargs):
    kwargs['max_length'] = 7
    super().__init__(*args,**kwargs)
    self.validators.append(validate_colro)


"""Models"""
class MapAction(models.Model):

  user = models.ForeignKey(
    'auth.User',
    null=False,
    validators=[WorkerUserValidator],
    on_delete=models.DO_NOTHING
  )

  date_time = models.DateTimeField(
    auto_now=True
  )

  px = models.PositiveIntegerField(
    null=False
  )

  py = models.PositiveIntegerField(
    null=False
  )

  color = ColorField(
    null=False,
  )


class Creators(models.Model):
  username_validator = UnicodeUsernameValidator()
  owner = models.BigIntegerField(
  )

  """dublication information in db..."""
  w_username = models.CharField(
    max_length=150,
    unique=True,
    validators=[username_validator],
  )

  """dublication information in db..."""
  w_password = models.CharField(
    max_length=128
  )

  worker = models.ForeignKey(
    'auth.User',
    related_name='worker',
    validators=[WorkerUserValidator],
    on_delete=models.DO_NOTHING
  )


  bot = models.ForeignKey(
    'auth.User',
    related_name='bot',
    validators=[BotUserValidator],
    on_delete=models.DO_NOTHING
  )


"""EXTRA FUNCTIONS"""

def __gen_account():
  if settings.ACCOUNT_ID is None:
    settings.WORKER_GROUP = Group.objects.get(name='Worker')
    settings.ACCOUNT_ID = User.objects.all().order_by('-id')[0].id
  fruit = random.choice(settings.ACCOUNT_NAMES)
  adj = random.choice(settings.ACCOUNT_ADJ)
  settings.ACCOUNT_ID += 1
  password = ''.join(random.choices("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM", k=32))
  return f"{adj}_{fruit}_{settings.ACCOUNT_ID}", password

def create_worker(*args, **kwargs):
  username, password = __gen_account()

  worker = User.objects.create_user(
    username=username, password=password, *args, **kwargs
  )

  settings.WORKER_GROUP.user_set.add(worker)
  return worker, username, password