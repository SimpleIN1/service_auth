import secrets
from typing import Tuple

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import status, exceptions
from rest_framework.response import Response

from AccountsApp.services.token.jwt_token import Jwt
from .mail.mail_send import EmailResetPassword, EmailVerify, RecoveryAccount, RegisteredProfile, InfoCreatedProfile, \
    SuccessOpeningAccessClient, LoginDetails, ChangePassword, OpeningAccessToApp
from .token.mail_token import create_token
from ..models import upload_to

User = get_user_model()


class UserUpdateDestroyRetrieve:
    '''# RUD(read, update, delete) операции над пользователем #'''

    def __check_email(self, user, new_email):
        '''# Сравнение нового и старого почтового адресса #'''

        if user.email != new_email:
            # token = create_token(id, new_email, uuid, settings.SECRET_KEY, 'confirm_verify_email') #Jwt.create_tmp_access_token(new_email)
            token = create_token(user, True)
            EmailVerify(email=[new_email], context={
                'protocol': settings.PROTOCOL,
                'site_name': settings.HOST,
                'url': f'{settings.URL_PAGE["email_verify"]}?email={new_email}&'
                       f'token={token}&'
                       f'uuid={user.uuid}',
            }).send()
            return '9'
        return '11'

    def __update_user(
            self,
            request,
            partial=False
    ) -> Response:
        '''# Функция обновления пользователься. Если пользователь изменил почту,
         то отправляется письмо на почту с подтверждением #'''

        data = request.data
        user = request.user

        serializer = self.serializer_class(data=data, instance=user, partial=partial)
        serializer.is_valid(raise_exception=True)

        code = self.__check_email(
            user,
            data.get('email')
        )

        serializer.save()

        return Response({'user_info': code,#settings.ERRORS['user_info'][code]
                         'user_data': serializer.data},
                        status=status.HTTP_200_OK)

    def put_user(self, request, *args, **kwargs) -> Response:
        '''# Обновление пользователя. Полная передачала данных #'''

        return self.__update_user(
            request=request
        )

    def destroy_user(self, request, *args, **kwargs) -> Response:
        '''# Удаление пользователя #'''

        instance = request.user
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_user(self, request, *args, **kwargs) -> Response:
        '''# Получение данных о пользователе #'''

        data = self.serializer_class(request.user).data
        return Response(data, status=status.HTTP_200_OK)

    def patch_user(self, request, *args, **kwargs) -> Response:
        '''# Обноление пользователя. не полная передача данных #'''

        return self.__update_user(
            request=request,
            partial=True
        )


class UserBase:
    pass


def find_or_get_user_model(code='4',raise_exception=True,**kwargs) -> User:
    '''# Проверка пользователя на то, что пользователь существует #'''
    #raise_exception = True
    #if kwargs.get('raise_exception'):
    #    raise_exception = kwargs.pop('raise_exception')
                                      
    print('%-'*10)
    print(kwargs)
    print('%-'*10)
    
    try:
        user = User.objects.get(**kwargs)
    except User.DoesNotExist:
        if raise_exception == False:
            return code
        else:
            raise exceptions.AuthenticationFailed(
                {'user_error': code}, #settings.ERRORS['user_error']['1']
                code=status.HTTP_401_UNAUTHORIZED
            )
    return user


def filter_user_model(code='4', **kwargs) -> User:
    '''# Проверка пользователя на то, что пользователь существует #'''

    try:
        user = User.objects.filter(**kwargs)
    except User.DoesNotExist:
        return None
    return user


def logout(user: User):
    user.update_last_login()
    user.save()


def is_not_verify_user(user: User) -> None:
    '''# Проверка на непройденную верификацию пользователя #'''

    if not user.is_verify:

        token = create_token(user)
        EmailVerify(email=[user.email], context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
            'url': f'{settings.URL_PAGE["email_verify"]}?email={user.email}&'
                   f'token={token}&'
                   f'uuid={user.uuid}',
        }).send()

        raise exceptions.AuthenticationFailed(
            {'user_error': '3'}, #settings.ERRORS['user_error']['3']
            code=status.HTTP_401_UNAUTHORIZED
        )


def is_not_active_user(user: User) -> None:
    '''# Проверка на то, что является ли пользователь неактивным #'''

    if not user.is_active:
        raise exceptions.AuthenticationFailed(
            {'user_error': '4'},#settings.ERRORS['user_error']['4']
            code=status.HTTP_401_UNAUTHORIZED
        )


def check_password_user(
    user: User,
    password: str,
    code: str = '1',
) -> None:
    '''# Проверка на соответствие пароля #'''

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed(
            {'user_error': code}, #settings.ERRORS['user_error']['2']
            code=status.HTTP_400_BAD_REQUEST
        )


def perform_confirm_verify_user(**kwargs):
    '''# Верификация почты пользователя по email и uuid #'''

    email = kwargs.pop('email')
    user = find_or_get_user_model(**kwargs)

    if not user.email == email:
        user.email = email

    if user.is_verify:
        return ('user_info', '6', status.HTTP_200_OK)
    if not user.is_verify:
        user.is_verify = True
    if not user.is_active:
        user.is_active = True

    user.save()

    return ('user_info', '8', status.HTTP_200_OK)


def perform_additional_to_reset_password(**kwargs) -> Tuple[str, str, int]:
    '''# Функция, выполняющая дополниетельные действия к сбросу пароля #'''

    user = find_or_get_user_model(**kwargs)

    if not user.is_reset_password:
        user.is_reset_password = True
        user.save()

    email = user.email
    uuid = user.uuid
    token = create_token(user) #.id, email, uuid, settings.SECRET_KEY, 'confirm_reset_password')#Jwt.create_tmp_access_token(email)

    EmailResetPassword([kwargs.get('email')], context={
        'protocol': settings.PROTOCOL,
        'site_name': settings.HOST,
        'port': settings.PORT,
        'url': f'{settings.URL_PAGE["reset_password"]}?email={email}&'
               f'token={token}&'
               f'uuid={uuid}',
    }).send()

    return ('user_info', '10', status.HTTP_200_OK)


def perform_reset_password(**kwargs) -> Tuple[str, str, int]:
    '''# Функция, выполняющая сброс пароля #'''

    password = kwargs.pop('password')
    user = find_or_get_user_model(**kwargs)

    if not user.is_reset_password:
        return ('user_info', '5', status.HTTP_200_OK)

    is_not_active_user(user)
    is_not_verify_user(user)

    user.set_password(password)
    user.is_reset_password = False
    user.save()

    return ('user_info', '7', status.HTTP_200_OK)


def perform_additional_to_recovery_user(**kwargs) -> Tuple[str, str, int]:
    '''# Функция, выполняющая дополнительные действия для восстановления учетной записи #'''

    user = find_or_get_user_model(**kwargs)
    is_not_verify_user(user)
    if user.is_active:
        return ('user_info', '12', status.HTTP_200_OK)

    email = user.email
    uuid = user.uuid
    token = create_token(user)#.id, email, uuid, settings.SECRET_KEY, 'confirm_recovery_user')#Jwt.create_tmp_access_token(email)

    RecoveryAccount([kwargs.get('email')], context={
        'protocol': settings.PROTOCOL,
        'site_name': settings.HOST,
        'port': settings.PORT,
        'url': f'{settings.URL_PAGE["recovery_account"]}?email={email}&'
               f'token={token}&'
               f'uuid={uuid}',
    }).send()

    return ('user_info', '13', status.HTTP_200_OK)


def perform_recovery_user(**kwargs) -> Tuple[str, str, int]:
    '''# Функция, выполняющая дополнительные действия для восстановления учетной записи #'''

    user = find_or_get_user_model(**kwargs)

    user.is_active = True
    user.save()

    return ('user_info', '12', status.HTTP_200_OK)


def is_token_transferred(refresh_token) -> None:
    '''# Функция, выполняющая проверку на передачу refresh_token #'''
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            {'fields_error': '18'},#settings.ERRORS['18']},#{'error_token': 'Refresh field is required'},
            code=status.HTTP_400_BAD_REQUEST
        )


def get_couple_tokens(**kwargs) -> dict:
    '''# Функция, выполняющая получние access_token и refresh_token #'''
    password = kwargs.pop('password')

    user = find_or_get_user_model('1',**kwargs)

    is_not_verify_user(user)
    is_not_active_user(user)
    check_password_user(user, password)

    token = {
        'refresh': Jwt.create_refresh_token(user_id=user.id),
        'access': Jwt.create_access_token(user_id=user.id),
    }

    return token


def get_access_token(**kwargs) -> dict:
    '''# Фунция, выпоняющая получение и пересоздание access_token из refresh_token #'''

    user = find_or_get_user_model(**kwargs)

    is_not_verify_user(user)

    access_token = {
        'access': Jwt.create_access_token(user_id=kwargs.get('id'))
    }

    return access_token


def perform_resend_email_letter(**kwargs) -> Tuple[str, str, int]:
    '''# Фунция, выпоняющая отправку письма #'''

    #password = kwargs.pop('password')
    user = find_or_get_user_model(**kwargs)

    if not user.is_verify: #and user.check_password(password):

        # token = create_token(user)

        RegisteredProfile(email=[user.email], context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
            'port': settings.PORT,
        }).send()

        return ('user_info', '9', status.HTTP_200_OK)

    return ('user_info', '9', status.HTTP_204_NO_CONTENT)


def perform_change_password(user: User, **kwargs) -> Tuple[str, str, int]:
    old_password = kwargs.get('old_password')
    password = kwargs.get('password')

    check_password_user(user, old_password, '2')

    user.set_password(password)
    user.save()

    return ('user_info', '7', status.HTTP_204_NO_CONTENT)


def send_email_directors(instance):
    directors = filter_user_model(type_user=1, is_getter_email=True)

    if directors:
        # Отправка письма директору(рам)
        try:
            #if not instance.is_added_admin_panel:
            filename = instance.file.name
            #else:
            #    filename = upload_to(instance, '')

            for director in directors:
                token = create_token(director, is_password=True)
                InfoCreatedProfile(email=[director.email], context={
                    'protocol': settings.PROTOCOL,
                    'site_name': settings.HOST,
                    'port': settings.PORT,
                    'last_name': instance.last_name,
                    'first_name': instance.first_name,
                    'middle_name': instance.middle_name,
                    'email': instance.email,
                    'org_name': instance.organization_name,
                    'url': f'{settings.URL_PAGE["url_for_access_client"]}?email={director.email}&'
                           f'token={token}&uuid={director.uuid}&email_access={instance.email}',
                }).send(filename)
        except Exception as e:
            print(e)


def generate_password(length: int = 11) -> str:
    return secrets.token_urlsafe(length)


def open_access_user(instance):
    #password = generate_password()
    #instance.set_password(password)

    if not (instance.is_active and instance.is_verify) and not instance.is_email_getted:
        password = generate_password()
        instance.set_password(password)
        instance.is_active = True
        instance.is_verify = True
        instance.is_email_getted = True
        instance.is_open_app = True
        instance.save()

        SuccessOpeningAccessClient(
            email=[instance.email],
            context={
                'protocol': settings.PROTOCOL,
                'site_name': settings.HOST,
                'port': settings.PORT,
                'email': instance.email,
                'password': password,
            }
        ).send()
        return True
    elif not (instance.is_active and instance.is_verify) and instance.is_email_getted:
        instance.is_active = True
        instance.is_verify = True
        instance.is_open_app = True
        instance.save()
        OpeningAccessToApp(
            email=[instance.email],
            context={
                'protocol': settings.PROTOCOL,
                'site_name': settings.HOST,
                'port': settings.PORT,
            }
        ).send()
        return True
    return False


def send_login_detail(email, password):
    LoginDetails(
        email=[email],
        context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
            'port': settings.PORT,
            'email': email,
            'password': password,
        }
    ).send()


def change_password_details(email, password):
    ChangePassword(
        email=[email],
        context={
            'protocol': settings.PROTOCOL,
            'site_name': settings.HOST,
            'port': settings.PORT,
            'email': email,
            'password': password,
        }
    ).send()
