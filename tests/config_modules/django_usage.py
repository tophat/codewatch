class DjangoUser(object):
    class object(object):
        @staticmethod
        def get():
            pass

    def dangerous_method(self):
        pass


def get_user():
    return DjangoUser.objects.get(id=1337)


user = get_user()
user.dangerous_method()
