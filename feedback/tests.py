from django.test import TestCase

from .models import Feedback, Category, Response

class FeedbackTestCase(TestCase):

    def test_feedback(self):
        # Test create one feedback
        feedback01 = Feedback(message='Feedback 01')
        feedback01.save()
        self.assertEqual(Feedback.objects.get().message, 'Feedback 01')
        feedback02 = Feedback(message='Feedback 02')
        feedback02.save()
        feedback01_02 = Feedback(message='Feedback 01')
        feedback01_02.save()
        self.assertEqual(len(Feedback.objects.all()), 3)

    def test_category(self):
        # Test create feedback without category
        feedback01 = Feedback(message='Feedback 01')
        feedback01.save()
        self.assertEqual(Feedback.objects.get().category, None)
        # Test add category
        category_others = Category(name='Others')
        category_others.save()
        category_social = Category(name='Social')
        category_social.save()
        feedback01.category = category_others
        feedback01.save()
        self.assertEqual(Feedback.objects.get().category, category_others)
        # Test remove category
        category_social.delete()
        self.assertEqual(Feedback.objects.get().category.name, 'Others')
        category_others.delete()
        self.assertEqual(Feedback.objects.get().category, None)
        # Test remove feedback
        category_website = Category(name='Website')
        category_website.save()
        feedback01.category = category_website
        feedback01.save()
        feedback01.delete()
        self.assertEqual(Category.objects.get(), category_website)
