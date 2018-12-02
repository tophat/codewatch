class DjangoUser(object):
    def dangerous_method(self):
        pass


def get_user():
    # without an inference tip, this will be un-inferrable
    return DjangoUser.objects.get(id=1337)


user = get_user()
# to infer that this is made on a DjangoUser, the above needs an inference tip
user.dangerous_method()
