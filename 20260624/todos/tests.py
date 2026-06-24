from django.test import TestCase

# Create your tests here.
class TodoViewTest(TestCase):
    def test_about_post(self):
        response = self.client.post("/about/")
        self.assertContains(response,"데이터가 제출되었습니다")
    def test_about_get(self):
        response = self.client.get("/about/")
        self.assertContains(response,"클래스 뷰 기반")

    def test_root(self):
        response = self.client.get("")
        self.assertContains(response,"함수기반 뷰")
