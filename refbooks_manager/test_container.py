from django.test import TestCase

from refbooks_manager.refbooks.models import (
    RefBook, Version, Element
)
from refbooks_manager.utils import get_test_data


class TestContainer(TestCase):
    test_data_refbooks = get_test_data('refbooks.json')
    test_data_versions = get_test_data('versions.json')
    test_data_elements = get_test_data('elements.json')

    def create_refbook(self, refbook):
        return RefBook.objects.create(
            code=self.test_data_refbooks['refbooks'][refbook]['code'],
            name=self.test_data_refbooks['refbooks'][refbook]['name'],
            description=(
                self.test_data_refbooks['refbooks'][refbook]['description']))

    def create_version(self, version, refbook):
        version = Version.objects.create(
            refbook=refbook,
            version=self.test_data_versions['versions'][version]['version'],
            start_date=(
                self.test_data_versions['versions'][version]['start_date']))
        return version

    def create_element(self, element, version):
        element = Element.objects.create(
            version=version,
            code=self.test_data_elements['elements'][element]['code'],
            value=self.test_data_elements['elements'][element]['value'])
        return element
