class ModelStateMixin:
    _state = None
    state_class = None

    @property
    def state(self):
        if not self._state:
            self._state = self.get_model_state_class()

        return self._state

    def get_model_state_class(self):
        if not self.state_class:
            raise ValueError('state_class não foi definido no model')

        return self.dispatcher_state_class.get(self.status)(object_instance=self)
    
    def set_state(self, new_state):
        if not self.state:
            raise ValueError('state_class não foi definido no model')
        
        self.status = new_state
        self.save()
        self.state
