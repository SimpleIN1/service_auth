from django.contrib.auth import get_user_model


User = get_user_model()


class Verify:

    @staticmethod
    def verify_email(uuid):
        try:
            user = User.objects.get(
                uuid=uuid,
                is_verify=False,
            )
        except User.DoesNotExist:
            return False

        user.is_verify = True
        user.save()

        return True
