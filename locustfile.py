import json
import random
import string

from locust import FastHttpUser, TaskSet, between, task


def load_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


user_list = load_data("dummy_data.json")


class UserBehavior(TaskSet):
    credential = None
    following_post_ids = None
    access_token = None

    def on_start(self):
        # 각 사용자는 무작위로 아이디와 비밀번호를 선택
        self.credential = random.choice(user_list)
        self.login()

    def login(self):
        # 로그인 요청
        response = self.client.post(
            "/users/signin",
            json={
                "email": self.credential["email"],
                "password": self.credential["password"],
            },
        )

        # 응답에서 access_token 추출
        if response.status_code == 200:
            self.access_token = response.json().get("access_token")
        else:
            print(f"Login failed for {self.credential['username']}")
            self.access_token = None

        # headers = {"Authorization": f"Bearer {self.access_token}"}
        # response = self.client.get("/posts/following", headers=headers)
        # self.following_post_ids = response.json()

    # @task(weight=1)
    # def test_api_with_token(self):
    #     if self.access_token:
    #         headers = {"Authorization": f"Bearer {self.access_token}"}
    #         # 토큰을 이용해 API 호출
    #         self.client.get("/posts", headers=headers)
    #     else:
    #         print(f"No access token for {self.credential['username']}")

    @task(weight=10)
    def test_api_with_token(self):
        if self.access_token:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            # 토큰을 이용해 API 호출
            self.client.get(
                f"/posts?search={random.choice(string.ascii_letters)}", headers=headers
            )
        else:
            print(f"No access token for {self.credential['username']}")

    # @task(weight=3)
    # def test_api_with_following_posts(self):
    #     if self.access_token:
    #         headers = {"Authorization": f"Bearer {self.access_token}"}
    #         response = self.client.get("/posts/following", headers=headers)
    #         self.following_post_ids = response.json()
    #     else:
    #         print(f"No access token for {self.credential['username']}")

    # @task(weight=6)
    # def test_api_with_get_following_posts_details(self):
    #     if self.access_token and self.following_post_ids:
    #         headers = {"Authorization": f"Bearer {self.access_token}"}
    #         for i in range(10):
    #             self.client.get(
    #                 f"/posts/{random.choice(self.following_post_ids)['id']}",
    #                 headers=headers,
    #             )
    #     else:
    #         print(
    #             f"No access token for {self.credential['username']} or no following_id post"
    #         )


class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
