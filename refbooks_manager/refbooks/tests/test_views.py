from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy

from refbooks_manager.refbooks.models import RefBook
from refbooks_manager.test_container import TestContainer


test_container = TestContainer()


class RefbooksViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.refbook1 = test_container.create_refbook('refbook1')
        cls.refbook2 = test_container.create_refbook('refbook2')
        cls.refbook3 = test_container.create_refbook('refbook3')
        cls.version1_1 = test_container.create_version(
            'version1-1', cls.refbook1)
        cls.version1_2 = test_container.create_version(
            'version1-2', cls.refbook1)
        cls.version1_3 = test_container.create_version(
            'version1-3', cls.refbook1)
        cls.version2_1 = test_container.create_version(
            'version2-1', cls.refbook2)
        cls.version2_2 = test_container.create_version(
            'version2-2', cls.refbook2)
        cls.version3_1 = test_container.create_version(
            'version3-1', cls.refbook3)

    def test_all_refbooks(self):
        c = Client()
        response = c.get(reverse_lazy('refbooks'))
        refbooks = RefBook.objects.all()
        for refbook in refbooks:
            self.assertContains(response, refbook.id)
            self.assertContains(response, refbook.code)
            self.assertContains(response, refbook.name)

    def test_refbooks_with_date(self):
        c = Client()
        url = reverse_lazy('refbooks')
        response = c.get(f'{url}?date=2022-12-01')
        expected_codes = ["RB1", "RB3"]
        expected_names = ["refbook1", "refbook3"]
        for code in expected_codes:
            self.assertContains(response, code)
        for name in expected_names:
            self.assertContains(response, name)
        not_expected_code = ["RB2"]
        self.assertNotContains(response, not_expected_code)
        not_expected_name = ["refbook2"]
        self.assertNotContains(response, not_expected_name)


class ElementsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.refbook1 = test_container.create_refbook('refbook1')
        cls.version1_1 = test_container.create_version(
            'version1-1', cls.refbook1)
        cls.version1_2 = test_container.create_version(
            'version1-2', cls.refbook1)
        cls.version1_3 = test_container.create_version(
            'version1-3', cls.refbook1)
        test_container.create_element('element1', cls.version1_1)
        test_container.create_element('element2', cls.version1_1)
        test_container.create_element('element2', cls.version1_2)
        test_container.create_element('element3', cls.version1_2)
        test_container.create_element('element1', cls.version1_3)
        test_container.create_element('element3', cls.version1_3)

    def test_elements_latest_version(self):
        c = Client()
        response = c.get(reverse_lazy('elements', args=['1']))
        expected_codes = ["D1", "D3"]
        expected_values = ["doctor1", "doctor3"]
        for code in expected_codes:
            self.assertContains(response, code)
        for value in expected_values:
            self.assertContains(response, value)
        not_expected_code = ["D2"]
        self.assertNotContains(response, not_expected_code)
        not_expected_value = ["doctor2"]
        self.assertNotContains(response, not_expected_value)

    def test_elements_specific_version(self):
        c = Client()
        url = reverse_lazy('elements', args=['1'])
        response = c.get(f'{url}?version=2.0')
        expected_codes = ["D2", "D3"]
        expected_values = ["doctor2", "doctor3"]
        for code in expected_codes:
            self.assertContains(response, code)
        for value in expected_values:
            self.assertContains(response, value)
        not_expected_code = ["D1"]
        self.assertNotContains(response, not_expected_code)
        not_expected_value = ["doctor1"]
        self.assertNotContains(response, not_expected_value)


class ElementValidationViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.refbook1 = test_container.create_refbook('refbook1')
        cls.refbook2 = test_container.create_refbook('refbook2')
        cls.version1_1 = test_container.create_version(
            'version1-1', cls.refbook1)
        cls.version1_2 = test_container.create_version(
            'version1-2', cls.refbook1)
        cls.version1_3 = test_container.create_version(
            'version1-3', cls.refbook1)
        cls.version2_1 = test_container.create_version(
            'version2-1', cls.refbook2)
        cls.version2_2 = test_container.create_version(
            'version2-2', cls.refbook2)
        test_container.create_element('element1', cls.version1_1)
        test_container.create_element('element2', cls.version1_1)
        test_container.create_element('element2', cls.version1_2)
        test_container.create_element('element3', cls.version1_2)
        test_container.create_element('element1', cls.version1_3)
        test_container.create_element('element3', cls.version1_3)
        test_container.create_element('element1', cls.version2_1)
        test_container.create_element('element2', cls.version2_2)
        cls.yes = 'Element is in RefBook'
        cls.no = 'No such Element in RefBook'

    def test_check_element_without_version(self):
        c = Client()
        url = reverse_lazy('check-element', args=['1'])
        response = c.get(f'{url}?code=D1&value=doctor1')
        self.assertContains(response, self.yes)
        response = c.get(f'{url}?code=D1&value=doctor2')
        self.assertContains(response, self.no)
        response = c.get(f'{url}?code=D3&value=doctor3')
        self.assertContains(response, self.yes)
        response = c.get(f'{url}?code=D2&value=doctor2')
        self.assertContains(response, self.no)

        url = reverse_lazy('check-element', args=['2'])
        response = c.get(f'{url}?code=D1&value=doctor1')
        self.assertContains(response, self.no)
        response = c.get(f'{url}?code=D2&value=doctor2')
        self.assertContains(response, self.yes)

    def test_check_element_with_version(self):
        c = Client()
        url = reverse_lazy('check-element', args=['1'])
        response = c.get(f'{url}?code=D1&value=doctor1&version=1.0')
        self.assertContains(response, self.yes)
        response = c.get(f'{url}?code=D2&value=doctor2&version=1.0')
        self.assertContains(response, self.yes)
        response = c.get(f'{url}?code=D3&value=doctor3&version=1.0')
        self.assertContains(response, self.no)

        response = c.get(f'{url}?code=D1&value=doctor1&version=3.0')
        self.assertContains(response, self.yes)
        response = c.get(f'{url}?code=D2&value=doctor2&version=3.0')
        self.assertContains(response, self.no)
        response = c.get(f'{url}?code=D3&value=doctor3&version=3.0')
        self.assertContains(response, self.yes)

        url = reverse_lazy('check-element', args=['2'])
        response = c.get(f'{url}?code=D1&value=doctor1&version=1.0')
        self.assertContains(response, self.yes)
        response = c.get(f'{url}?code=D2&value=doctor2&version=1.0')
        self.assertContains(response, self.no)

        response = c.get(f'{url}?code=D1&value=doctor1&version=2.0')
        self.assertContains(response, self.no)
        response = c.get(f'{url}?code=D2&value=doctor2&version=2.0')
        self.assertContains(response, self.yes)
