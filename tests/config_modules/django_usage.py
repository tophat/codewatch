class DjangoUser(object):
    def dangerous_method(self):
        pass

    def safe_method(self):
        pass


def get_user():
    # without an inference tip, this will be un-inferrable
    return DjangoUser.objects.get(id=1337)


user = get_user()
# dangerous_method call #1
user.dangerous_method()


def get_users():
    return DjangoUser.objects.bulk_create()


# dangerous_method call #2
users = get_users()
for user in users:
    user.dangerous_method()


# dangerous_method call #3
# Chained call
all_users = DjangoUser.objects.all()
all_users.latest().dangerous_method()


# dangerous_method call #4
all_users.filter().order_by().all().first().dangerous_method()


# dangerous_method call #5
# vanilla python method call
DjangoUser().dangerous_method()


# not a call
DjangoUser.dangerous_method


def dangerous_method():
    pass


# not a call on DjangoUser
dangerous_method()


DjangoUser().safe_method()
