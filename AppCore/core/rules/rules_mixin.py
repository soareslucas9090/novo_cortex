class ModelRulesMixin:
    _rules = None
    rules_class = None

    @property
    def rules(self):
        if not self._rules:
            self._rules = self.get_model_rules_class()

        return self._rules

    def get_model_rules_class(self):
        if not self.rules_class:
            raise ValueError('rules_class não foi definido no model')
        return self.rules_class(object_instance=self)