from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
import os

class Command(BaseCommand):
  help = "startup command"

  def handle(self, *args, **options):
    
    names = ['TG', 'Worker', 'Bot']
    ex_groups = Group.objects.filter(name__in=names)
    gotNames = list(map(lambda x: x.name, ex_groups))
    groups = []
    ct = ContentType.objects.get_or_create(
      app_label='back_api',
      model='auth.User'
    )[0]
    for name in names:
      if name not in gotNames:
        g = Group(name=name)
        p = Permission.objects.create(
          codename=name.lower(),
          name=name, 
          content_type=ct
        )
        groups.append((g,p))

    if groups:
      Group.objects.bulk_create(list(map(lambda x: x[0], groups)))
      gp = [
        Group.permissions.through(group_id=igp[0].id, permission_id=igp[1].id)
        for igp in groups
      ]
      Group.permissions.through.objects.bulk_create(gp)
      self.stdout.write(self.style.SUCCESS(f'adding default groups {groups}'))

    if not User.objects.filter(username='admin').exists():
      User.objects.create_superuser('admin', 'admin@jam.as', 'admin')
      self.stdout.write(self.style.SUCCESS(f'adding default superuser'))


    bot_group = Group.objects.get(name='Bot')
    try:
      bot = User.objects.get(username=os.environ.get('BOT_USERNAME', 'bot_1'))
    except:
      bot = User.objects.create_user(
        username=os.environ.get('BOT_USERNAME', 'bot_1'),
        password=os.environ.get('BOT_PASSWORD', 'bot_1')
      )
    bot.groups.add(bot_group)
    self.stdout.write('Bot added: ' + str(bot))