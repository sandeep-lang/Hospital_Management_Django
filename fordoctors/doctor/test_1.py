import unittest
import requests
import json

# Create your tests here.
class TestDoctorActions(unittest.TestCase):
    def test_login(self):
        unknownuserresponse = requests.post('http://127.0.0.1:8001/api/login',
                                            {
                                                "username": "sandeep", 
                                                "password": "sandy"
                                            })
        unknownusercontent = json.loads(unknownuserresponse.content)
        wrongpasswordresponse = requests.post('http://127.0.0.1:8001/api/login',
                                            {
                                                 "username":"Dr.Thomas",
                                                 "password":"sandep1"
                                               })
        wrongpasscontent = json.loads(wrongpasswordresponse.content)
        existinguserresponse = requests.post('http://127.0.0.1:8001/api/login',
                                            {
                                               "username":"Dr.Thomas",
                                               "password":"sandeep1"
                                             })
        existingusercontent = json.loads(existinguserresponse.content)
        self.assertEqual(wrongpasscontent["detail"],"Please enter valid password")
        self.assertEqual(unknownusercontent["detail"],"User Not Found")
        assert "jwt" in existingusercontent
    
    def test_userview(self):
        userviewresponse = requests.get(
            'http://127.0.0.1:8001/api/dapp')
        userviewcontent = json.loads(userviewresponse.content)
        self.assertEqual(
            userviewcontent["detail"],"Unauthenticated")

    def test_logout(self):
        alreadyloggedoutresponse = requests.post(
            'http://127.0.0.1:8001/api/logout')
        alreadyloggedoutcontent = json.loads(alreadyloggedoutresponse.content)
        self.assertEqual( 
            alreadyloggedoutcontent["message"],"Your Successfully Loggedout" ) 



