from django.db import models
from django.core.validators import RegexValidator, BaseValidator
from django.core.exceptions import ValidationError
from django.utils.regex_helper import _lazy_re_compile


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
  def __init__(self, message=...):
    super().__init__('TG', message)
  

class WorkerUserValidator(BaseUserGroupValidator):
  def __init__(self, message=...):
    super().__init__('Worker', message)


class BotUserValidator(BaseUserGroupValidator):
  def __init__(self, message=...):
    super().__init__('Bot', message)


color_validator = RegexValidator(
    _lazy_re_compile(r"^#([0-9a-f]{3}|[0-9a-f]{6})\Z"),
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

  user_id = models.ForeignKey(
    'auth.User',
    null=False,
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
  owner = models.ForeignKey(
    'auth.User',
    related_name='owner',
    validators=[TgUserValidator],
    on_delete=models.DO_NOTHING
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
