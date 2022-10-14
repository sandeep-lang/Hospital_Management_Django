import unittest
import requests
import json


class TestPatientActions(unittest.TestCase):
    def test_register(self):
        alreadyexistinguserresponse = requests.post('http://127.0.0.1:8000/api/register',
                                                    {
                                                        "name": "vikram",
                                                        "email": "vikram@gmail.com",#done
                                                        "password": "sandep1"
                                                    })
        content = json.loads(alreadyexistinguserresponse.content)
        #assert content["email"] == ["user with this email already exists."]
        self.assertEqual(content["email"], [
                         "user with this email already exists."])

    def test_login(self):
        unknownuserresponse = requests.post('http://127.0.0.1:8000/api/login',
                                            {
                                                "email": "abcd@gmail.com", 
                                                "password": "efgh"
                                            })
        unknownusercontent = json.loads(unknownuserresponse.content)
        wrongpasswordresponse = requests.post('http://127.0.0.1:8000/api/login',
                                              {
                                                  "email": "vikram@gmail.com",
                                                  "password": "sandeep1"  #done
                                              })
        wrongpasscontent = json.loads(wrongpasswordresponse.content)
        existinguserresponse = requests.post('http://127.0.0.1:8000/api/login',
                                             {
                                                 "email": "vikram@gmail.com",
                                                 "password": "sandep1"
                                             })
        existingusercontent = json.loads(existinguserresponse.content)
        self.assertEqual(wrongpasscontent["detail"], "Incorrect Password")
        self.assertEqual(unknownusercontent["detail"], "No User Found")
        assert "jwt" in existingusercontent

    def test_logout(self):
        alreadyloggedoutresponse = requests.post(
            'http://127.0.0.1:8000/api/logout')
        alreadyloggedoutcontent = json.loads(alreadyloggedoutresponse.content)
        self.assertEqual( 
            alreadyloggedoutcontent["message"],"Your Successfully Loggedout" ) 

    def test_userview(self):
        userviewresponse = requests.get(
            'http://127.0.0.1:8000/api/profile')
        userviewcontent = json.loads(userviewresponse.content)
        self.assertEqual(
            userviewcontent["detail"], "Unauthenticated")

    def test_bookappointment(self):
        bookappointmentresponse = requests.post(
            'http://127.0.0.1:8000/api/papp',
            {
                "patientname":"vikram",
                "email":"vikram@gmail.com",
                "doctorid":2,
                "doctorname":"Dr.Ravi",
                "department":"ENT",
                "phone":9100745256,
                "gender":"male",
              "appointmentdate":"2022-10-09",
             "appointmenttime":"16:30-17:00",
            "symptoms":"cold"
            })
        bookappointmentcontent = json.loads(bookappointmentresponse.content)
        self.assertEqual(
            bookappointmentcontent["detail"], "Unauthenticated")

    def test_updateappointment(self):
        updateappointmentresponse = requests.put(
            'http://127.0.0.1:8000/api/update',
            {
                
                    "appointmentid":27,
                    "patientid":38,
                    "doctorid":2,
                    "doctorname":"Dr.Ravi",
                    "department":"ENT",
                    "patientname":"vikram",
                    "email":"vikram@gmail.com",
                    "phone":9100745256,
                    "gender":"male",
                    "appointmentdate":"2022-10-10",
                    "appointmenttime":"13:00-13:30",
                    "symptoms":"cold"


                
            })
        updateappointmentcontent = json.loads(
            updateappointmentresponse.content)
        self.assertEqual(
            updateappointmentcontent["detail"], "Unauthenticated")

    def test_deleteappointment(self):
        deleteappointmentresponse = requests.delete(
            'http://127.0.0.1:8000/api/delete')
        deleteappointmentcontent = json.loads(
            deleteappointmentresponse.content)
        print(deleteappointmentcontent["detail"])
        self.assertEqual(
            deleteappointmentcontent["detail"],"login with correct details")

    def test_makepayment(self):
        makepaymentresponse = requests.post(
        'http://127.0.0.1:8000/api/payment',
            {
                 "appointmentid":30,
                 "nameoncard":"vikram",
                 "cardnumber":1234567890,
                 "expirymonth":"10",
                 "expiryyear":"2022",
                  "cvv":"170"

})
        makepaymentcontent = json.loads(makepaymentresponse.content)
        self.assertEqual(
            makepaymentcontent["detail"], "Unauthenticated")