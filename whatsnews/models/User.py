import peewee as pw
from playhouse.signals import pre_save
from werkzeug.security import generate_password_hash
from whatsnews.models import BaseModel


class User(BaseModel):
    id = pw.AutoField()
    username = pw.CharField(unique=True)
    password = pw.CharField()
    is_admin = pw.BooleanField(default=False)

    class Meta:
        table_name = 'users'


#
# Signals
#


@pre_save(sender=User)
def pre_save_handler(model_class, instance, created):
    ''' If the password was modified, hash it '''
    if User.password in instance.dirty_fields:
        instance.password = generate_password_hash(instance.password)