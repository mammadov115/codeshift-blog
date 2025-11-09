from drf_yasg.inspectors import SwaggerAutoSchema

class DynamicTaggingAutoSchema(SwaggerAutoSchema):

    def get_tags(self, operation_keys=None):
        
        tags = getattr(self.view, 'swagger_tag', None)
        if tags:
            return tags

        if hasattr(self.view, 'queryset') and self.view.queryset is not None:
            model_name = self.view.queryset.model.__name__
            return [f"{model_name} Management"]
            
        elif hasattr(self.view, 'serializer_class'):
            try:
                model_name = self.view.serializer_class.Meta.model.__name__
                return [f"{model_name} Management"]
            except AttributeError:
                pass 
        

        return super().get_tags(operation_keys)