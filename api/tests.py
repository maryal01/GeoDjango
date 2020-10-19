from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json
from pprint import pprint
class downwardHUCTestCase(APITestCase):
    def test_Exists(self):
        url = reverse("downward")
        data = {"resource_list": [
                {"latitude": -112.7955016686925,
                "longitude": 33.5684547051867,
                "type": "POINT"},
                
                {"latitude": -83.19692015421879,
                "longitude": 42.04347594515679,
                "type": "POINT"},

                {"low_latitude": -83.20552828858041,
                "high_latitude": -83.20545665108051,
                "low_longitude": 42.03679305975049,
                "high_longitude":42.03673690141721,
                "type": "BOX"} ] 
            }
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
# use the above data to test it through postman
# the response you get is
'''{
    "HUC_ID": [
        "1507",
        "0410",
        "0409",
        "0426"
    ]
}'''

class upwardHUCTestCase(APITestCase):
    def test_Exists(self):
        url = reverse("upward")
        data = {"resource_list": [
                {"latitude": -112.7955016686925,
                "longitude": 33.5684547051867,
                "type": "POINT"},
                
                {"latitude": -83.19692015421879,
                "longitude": 42.04347594515679,
                "type": "POINT"},

                {"low_latitude": -83.20552828858041,
                "high_latitude": -83.20545665108051,
                "low_longitude": 42.03679305975049,
                "high_longitude":42.03673690141721,
                "type": "BOX"} ] 
            }
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# use the above data to test it through postman
# the response you get is
'''{
    "HUC_ID": [
        "04100001",
        "04260000",
        "04090004",
        "15070103",
        "04100013",
        "15070101"
    ]
}'''