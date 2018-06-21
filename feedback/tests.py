from django.test import TestCase

from .models import Feedback, Category, Response

from .views import _get_page_range

class FeedbackTestCase(TestCase):

    def setUp(self):
        # Setup Others category
        category_others = Category(name='Others')
        category_others.save()

    def test_feedback(self):
        # Get Others category
        category_others = Category.objects.get(pk='Others')

        # Test create one feedback
        feedback01 = Feedback(message='Feedback 01')
        feedback01.category = category_others
        feedback01.save()
        self.assertEqual(Feedback.objects.get().message, 'Feedback 01')

        # Test create more feedback
        feedback02 = Feedback(message='Feedback 02')
        feedback02.category = category_others
        feedback02.save()
        feedback01_02 = Feedback(message='Feedback 01')
        feedback01_02.category = category_others
        feedback01_02.save()
        self.assertEqual(len(Feedback.objects.all()), 3)

    def test_category(self):
        # Get Others category
        category_others = Category.objects.get(pk='Others')

        # Test create feedback specified category
        feedback01 = Feedback(message='Feedback 01')
        feedback01.category = category_others
        feedback01.save()
        self.assertEqual(Feedback.objects.get().category, category_others)

        # Test add existing category
        category_others = Category(name='Others')
        category_others.save()
        self.assertEqual(len(Category.objects.all()), 1)

        # Test add more category
        category_social = Category(name='Social')
        category_social.save()
        self.assertEqual(len(Category.objects.all()), 2)

        # Test change category
        feedback01.category = category_social
        feedback01.save()
        self.assertEqual(Feedback.objects.get().category, category_social)

        # Test remove category
        category_social.delete()
        self.assertEqual(Feedback.objects.get().category, category_others)

        # Test remove feedback
        category_website = Category(name='Website')
        category_website.save()
        feedback01.category = category_website
        feedback01.save()
        feedback01.delete()
        self.assertEqual(Category.objects.get(pk='Website'), category_website)

class PaginatorTestCase(TestCase):

    def test_get_page_range(self):
        # Test enough space to show all pages
        self.assertEqual(_get_page_range(1, 10, 5), range(1, 11))

        # Test current page in the middle
        self.assertEqual(_get_page_range(4, 10, 2), range(2, 7))

        # Test current page in the front
        self.assertEqual(_get_page_range(2, 10, 2), range(1, 6))

        # Test current page in the back
        self.assertEqual(_get_page_range(8, 10, 3), range(4, 11))

        # Test current page is the first one
        self.assertEqual(_get_page_range(1, 10, 3), range(1, 8))

        # Test current page is the last one
        self.assertEqual(_get_page_range(10, 10, 3), range(4, 11))
