from codewatch.assertion import assertion
from codewatch.helpers.visitor import count_calls_on_django_model


USAGE_FILE = 'django_usage.py'


def file_filter(file_name):
    return file_name == USAGE_FILE


def directory_filter(dir_name):
    return True


STATS_NAMESPACE = 'DjangoConfigDangerousMethod'
count_calls_on_django_model(
    STATS_NAMESPACE,
    'django_usage.py.DjangoUser',
    'dangerous_method',
)


@assertion(stats_namespaces=[STATS_NAMESPACE])
def correctly_infers_dangerous_method_call(_stats):
    assert _stats.get(USAGE_FILE, 0) == 5, 'Django inference failed'
