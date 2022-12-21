from rest_framework.renderers import JSONRenderer


class AppJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        root_name = getattr(renderer_context.get('view').get_serializer().Meta,
                            'root_name',
                            'objects')
        data_with_root = {root_name: data}
        return super().render(
            data_with_root, accepted_media_type, renderer_context)
