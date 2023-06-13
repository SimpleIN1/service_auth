from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


UserModel = get_user_model()

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print('--')
        print(request)
        print(username)
        print(password)
        print('--')
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        print('Its OK')
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            print(user)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
            print('No ok')
        else:
            print('Its ok 2')
            print('check pass', user.check_password(password))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            #else:
             #   user.set_password(password)
              #  user.save()
               # print('check pass', user.check_password(password))
