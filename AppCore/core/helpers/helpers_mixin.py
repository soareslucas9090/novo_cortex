class ModelHelperMixin:
    _helper = None
    helper_class = None

    @property
    def helper(self):
        if not self._helper:
            self._helper = self.get_model_helper_class()

        return self._helper

    def get_model_helper_class(self):
        if not self.helper_class:
            raise ValueError('helper_class não foi definido no model')
        return self.helper_class(object_instance=self)