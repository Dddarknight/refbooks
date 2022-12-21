from rest_framework import serializers

from refbooks_manager.refbooks.models import RefBook, Element


class RefBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = RefBook
        root_name = 'refbooks'
        fields = [
            'id', 'code', 'name'
        ]


class ElementSerializer(serializers.ModelSerializer):
    version = serializers.SerializerMethodField('get_version')

    class Meta:
        model = Element
        root_name = 'elements'
        fields = [
            'code', 'value', 'version'
        ]

    def get_version(self, obj):
        return obj.version.version
