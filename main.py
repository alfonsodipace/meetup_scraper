import requests
from bs4 import BeautifulSoup
import json

URL = ""


class Event:
    def __init__(self, name, url, description, startDate, endDate, location):
        self.name = name
        self.url = url
        self.description = description
        self.startDate = startDate
        self.endDate = endDate
        self.location = location
        # self.locationUrl = "https://www.google.com/maps/search/?api=1&query=" + location


def get_event_from_meetup(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    try:
        soup = BeautifulSoup(r.content, 'html5lib')
    except Exception as e:
        print(e)
        return None
    script = soup.find_all('script', attrs={"type": "application/ld+json"})
    if len(script) == 0:
        return None
    for i in range(len(script)):
        json_script = json.loads(script[i].string)
        if "@type" in json_script:
            if json_script["@type"] == "Event":
                name = json_script["name"]
                url = json_script["url"]
                description = json_script["description"]
                startDate = json_script["startDate"]
                endDate = json_script["endDate"]
                location = json_script["location"]["name"]
                event = Event(name, url, description, startDate, endDate, location)
                return event
    return None


event = get_event_from_meetup(URL)
if event is not None:
    print(event.name)
else:
    print("Event not found")
