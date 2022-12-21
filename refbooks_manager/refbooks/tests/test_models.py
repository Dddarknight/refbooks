from django.test import TestCase

from refbooks_manager.refbooks.models import (
    RefBook, Version, Element
)
from refbooks_manager.test_container import TestContainer
from refbooks_manager.utils import get_test_data


test_container = TestContainer()


class RefBookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.refbook_data = get_test_data(
            'refbooks.json')['refbooks']['refbook1']
        cls.refbook = test_container.create_refbook('refbook1')

    def test_refbook_creation(self):
        self.assertTrue(isinstance(self.refbook, RefBook))
        self.assertEqual(
            self.refbook.code, self.refbook_data['code'])
        self.assertEqual(
            self.refbook.name, self.refbook_data['name'])
        self.assertEqual(
            self.refbook.description, self.refbook_data['description'])


class VersionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.refbook = test_container.create_refbook('refbook1')
        cls.version_data = get_test_data(
            'versions.json')['versions']['version1-1']
        cls.version = test_container.create_version('version1-1', cls.refbook)

    def test_refbook_creation(self):
        self.assertTrue(isinstance(self.version, Version))
        self.assertEqual(
            self.version.refbook, self.refbook)
        self.assertEqual(
            self.version.version, self.version_data['version'])
        self.assertEqual(
            self.version.start_date, self.version_data['start_date'])


class ElementModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.refbook = test_container.create_refbook('refbook1')
        cls.version = test_container.create_version('version1-1', cls.refbook)
        cls.element = test_container.create_element('element1', cls.version)
        cls.element_data = get_test_data(
            'elements.json')['elements']['element1']

    def test_refbook_creation(self):
        self.assertTrue(isinstance(self.element, Element))
        self.assertEqual(
            self.element.version, self.version)
        self.assertEqual(
            self.element.code, self.element_data['code'])
        self.assertEqual(
            self.element.value, self.element_data['value'])
