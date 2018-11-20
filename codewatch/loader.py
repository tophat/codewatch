import importlib

from codewatch.assertion import Assertion


class ModuleLoader(object):
    def __init__(
        self,
        codewatch_config_module,
    ):
        self.assertions = self._load_assertions(codewatch_config_module)
        self.filters = self._load_file_filters(codewatch_config_module)

    def _load_assertions(self, assertion_module_name):
        assertion_module = importlib.import_module(assertion_module_name)
        return Assertion.load_assertion_fns(assertion_module)

    def _load_file_filters(self, filter_module_name):
        filter_module = importlib.import_module(filter_module_name)
        if not hasattr(filter_module, 'directory_filter'):
            raise NotImplementedError(
                'need directory_filter method in filter_module',
            )
        if not hasattr(filter_module, 'file_filter'):
            raise NotImplementedError(
                'need file_filter method in filter_module',
            )
        directory_filter = getattr(filter_module, 'directory_filter')
        file_filter = getattr(filter_module, 'file_filter')

        return directory_filter, file_filter
