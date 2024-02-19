from marshmallow import fields, ValidationError

class ClassField(fields.Field):
    '''A custom Field to be used in Marshmallow Schemas where a class constructing correctly is the only required validation.
    The class can only have one constructor parameter.
    '''

    def __init__(self, class_type, **kwargs):
        '''Constructor.
        
        Args:
            class_type: the type of the class that needs to be validated.
        '''
        self.class_type = class_type
        super().__init__(**kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        return self.class_type.serialize(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            obj = self.class_type(value)
        except ValueError as err:
            raise ValidationError(err.args)
        
        return obj