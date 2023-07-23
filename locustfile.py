from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/auth/login/")
        self.client.get("/accounts/signup/")