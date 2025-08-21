# /whatsnews/models/User.py


import peewee as pw
from playhouse.signals import pre_save
from werkzeug.security import check_password_hash, generate_password_hash
from whatsnews.models import BaseModel


class User(BaseModel):
    id = pw.AutoField()
    username = pw.CharField(unique=True)
    password = pw.CharField()
    is_admin = pw.BooleanField(default=False)

    class Meta:
        table_name = 'users'


    @classmethod
    def login(cls, username, pw_guess):
        try:
            user = User.get(User.username == username)
        except User.DoesNotExist:
            return None
        if not check_password_hash(user.password, pw_guess):
            return None
        # FIX ME: I should remove/mask the password here...

        return user
    

    def __repr__(self):
        return f'<User {self.id} | {self.username}>'
    

#
# Signals
#


@pre_save(sender=User)
def pre_save_handler(model_class, instance, created):
    ''' If the password was modified, hash it '''
    
    if User.password in instance.dirty_fields:
        instance.password = generate_password_hash(instance.password)