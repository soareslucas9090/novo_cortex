class ModelBusinessMixin:
    _business = None
    business_class = None

    @property
    def business(self):
        if not self._business:
            self._business = self.get_model_business_class()

        return self._business
    
    def get_model_business_class(self):
        if not self.business_class:
            raise ValueError('business_class não foi definido no model')
        return self.business_class(instance=self)