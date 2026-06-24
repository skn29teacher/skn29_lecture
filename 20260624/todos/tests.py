from django.test import TestCase

# Create your tests here.
class TodoViewTest(TestCase):
    def test_about(self):
        response = self.client.post("/about/")
        self.assertContains(response,"데이터가 제출되었습니다")
    def test_root(self):
        response = self.client.get("/about/")
        self.assertContains(response,"classView")
