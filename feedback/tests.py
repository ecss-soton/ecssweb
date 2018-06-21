from django.test import TestCase

from .models import Feedback, Category, Response

class FeedbackTestCase(TestCase):

    def setUp(self):
        # Setup Others category
        category_others = Category(name='Others')
        category_others.save()

    def test_feedback(self):
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
