import random
from locust import HttpLocust, TaskSet, task
from pyquery import PyQuery


class BrowseDocumentation(TaskSet):
    def on_start(self):
        # assume all users arrive at the index page
        self.index_page()
    
    @task(1)
    def index_page(self):
        r = self.client.get("/")

    @task(2)
    def login(self):
        self.client.post("/login", {"username":"demo", "password":"demo"})

class AwesomeUser(HttpLocust):
    task_set = BrowseDocumentation
    host = "http://localhost:8888"
    
    # we assume someone who is browsing the Locust docs, 
    # generally has a quite long waiting time (between 
    # 20 and 600 seconds), since there's a bunch of text 
    # on each page
    min_wait = 20  * 1000
    max_wait = 600 * 1000
