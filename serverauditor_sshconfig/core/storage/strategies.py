import six


class Strategy(object):

    def __init__(self, storage):
        self.storage = storage


class SaveStrategy(Strategy):

    def save_submodel(self, submodel, mapping):
        if isinstance(submodel, six.integer_types):
            return submodel
        assert submodel.id
        return submodel.id

    def save_field(self, field, mapping):
        return field and self.save_submodel(field, mapping)

    def save(self, model):
        model_copy = model.copy()
        for field, mapping in model.mapping.items():
            saved_submodel = self.save_field(getattr(model, field), mapping)
            setattr(model_copy, field, saved_submodel)
        return model_copy


class RelatedSaveStrategy(SaveStrategy):

    def save_submodel(self, submodel, mapping):
        return self.storage.save(submodel).id


class GetStrategy(Strategy):

    def get(self, model):
        return model


class RelatedGetStrategy(GetStrategy):

    def get(self, model):
        result = super(RelatedGetStrategy, self).get(model)
        for field, mapping in result.mapping.items():
            submodel_id = getattr(result, field)
            if submodel_id:
                submodel = self.storage.get(mapping.model, id=submodel_id)
                setattr(result, field, submodel)
        return result
