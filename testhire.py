import requests
import pytest
from jsonpath_ng import parse,jsonpath
import json
from conftest import login
from loggerclass import Baseclass 
import testdata  


class Testhire(Baseclass):
    
    ids = None
    draftids = None
    logs  = Baseclass.logger()
    
    def fixturevariable(self,login):
      self.token = login.token
    
    #@pytest.mark.skip
    @pytest.mark.run('first')
    def test_getalljobs(self):
        #logs = self.logger()
        url = testdata.testurl
        self.logs.info("Getjob API called successfully")

        dataload = "{\"query\":\"\\r\\n  query GetJobs($search: String, $filters: GetJobsFilter) {\\r\\n    getJobs(search: $search, filters: $filters) {\\r\\n      name\\r\\n      jobs {\\r\\n        _id\\r\\n        publish {\\r\\n          _id\\r\\n          title\\r\\n          category\\r\\n          createdAt\\r\\n          updatedAt\\r\\n        }\\r\\n        draft {\\r\\n          _id\\r\\n          title\\r\\n          description\\r\\n          category\\r\\n          createdAt\\r\\n          updatedAt\\r\\n        }\\r\\n        status\\r\\n        team {\\r\\n          userId\\r\\n          interviewRound\\r\\n          mailTemplate {\\r\\n            subject\\r\\n            body\\r\\n          }\\r\\n          role\\r\\n          user {\\r\\n            userId\\r\\n            email\\r\\n            firstName\\r\\n            lastName\\r\\n            profileUri\\r\\n            color\\r\\n            jobTitle\\r\\n            phoneNumber\\r\\n            timezone\\r\\n            theme\\r\\n            privileges {\\r\\n              admin\\r\\n              creator\\r\\n            }\\r\\n          }\\r\\n        }\\r\\n\\r\\n        createdBy\\r\\n        publishedAt\\r\\n      }\\r\\n    }\\r\\n  }\\r\\n\",\"variables\":{\"search\":\"\"}}"
        self.logs.info("Payload object created successfully")
        #payload = json.dumps(dataload)
        #logs.info('python payload converted in json format')
        
        headers = {'Authorization':f'Bearer {self.token}',
                  
        'Content-Type': 'application/json'
          } 
        self.logs.info("All header passed to server")
       
        #print(self.token)
        self.logs.info(f'Token printed for tracking,{self.token}')

        response = requests.request('POST',url,headers=headers,data=dataload)
        #print(response)
        output = response.json()
        print(output)
        #response =requests.post(url,headers=headers,data=payload)             
        self.logs.info('reponse object created for POST request and data sent to server')
        assert response.status_code == 200
       # methodname = requests.header.get('POST')
        self.logs.info('Assertion added to check response code 200')
        finalresponse = response.json()
        self.logs.info('Reponse converted into json format')
        #print('List of all jobs',finalresponse)
        content_type = response.headers.get("Content-Type")
        assert content_type == "application/json", "Unexpected Content-Type: " + content_type
        self.logs.info(f'Assertion added on content_type {content_type}')
        hireserver = response.headers.get('Server')
        assert hireserver == "cloudflare",'unexpected hireserver:'+ hireserver
        self.logs.info(f'Assertion added on servername {hireserver}')
        assert 'data','getjobs' in finalresponse
        assert isinstance(finalresponse,dict)
        self.logs.info('Assetion added to check elements in final response')
        #assert isinstance(finalresponse['name'],str)
        print('Test Run Successful')


    
    #@pytest.mark.skip
    def test_addjob(self):
        
        url = testdata.testurl
        #logs = self.logger()
        self.logs.info("URL called successfully for Addjob API")
        #self.jobname = jobname
        data = {"query": "\n  mutation AddJob(\n    $title: String!\n    $city: String\n    $country: InputCountry\n    $state: String\n    $category: Category\n  ) {\n    addJob(\n      title: $title\n      city: $city\n      country: $country\n      state: $state\n      category: $category\n    ) {\n      _id\n    }\n  }\n",
                              "variables": {
                                "title": testdata.nameofjob,
                                "country": {
                                  "isoCode": "",
                                  "name": ""
                                },
                                "city": testdata.city,
                                "state": testdata.state,
                                "category": testdata.categoryofjob
                              },
                              "operationName": "AddJob"}
        self.logs.info('Payload object created with all data')
        payload = json.dumps(data)
        self.logs.info('converted data object in json formated string')
        print(testdata.nameofjob)

        headers = {'Authorization':f'Bearer {self.token}',
        'Content-Type': 'application/json'
          }
        self.logs.info('headers object created with Authorization and Content-Type keys')
        response = requests.request('POST',url,headers=headers,data=payload)
        self.logs.info('API called using POST request and store into response object')

        finalreponse = response.json()
        self.logs.info('converted json response into python type')
            #output = json.dumps(finalreponse)

        if response.status_code == 200 and 'errors' in finalreponse:
                for error in finalreponse['errors']:
                    errmsg = error.get('message','')
                    print(f"Received the error in response: {errmsg}")
                    self.logs.error(f'Error received in the response:{errmsg}')

        elif response.status_code == 200:    
          #finalreponse = response.json()
          print(finalreponse)   #for tsting i removed output and out finalresponse ,in case error received revert it
          self.logs.info('Recevied response code as 200')
          path_exp = parse('$.data.addJob._id')
          matches = [match.value for match in path_exp.find(finalreponse)]
          Testhire.ids = '-'.join(matches)
          self.logs.info(f'Job id {Testhire.ids}getting exactred from reponse of addjob API')
          #print(Testhire.ids)
          return Testhire.ids
    
        elif response.status_code !=200:
            print(f'Error Received while adding job{response.status_code}')
            self.logs.error('Didnt receive response as 200 instead of it getting {response.status_code}')
            self.logs.error(response.text)
    


    #@pytest.mark.skip
    def test_publishjob(self):
        
        #logs = self.logger()
        url = testdata.testurl
        self.logs.info('Publish API url called successfully')
                

        data =  {
    "query": "\n  mutation PublishJob($jobId: String) {\n    publishJob(jobId: $jobId) {\n      _id\n    }\n  }\n",
    "variables": { "jobId": Testhire.ids },
    "operationName": "PublishJob"
                }
        self.logs.info("Payload object created successfully")

        payload = json.dumps(data)
        self.logs.info("python payload converted into JSON supported string")


        headers  = {'Authorization':f'Bearer {self.token}',
        'Content-Type': 'application/json'
          }
        self.logs.info('headers object created with Authorization and Content-Type keys')
        response = requests.request('POST',url,headers=headers,data=payload)
        self.logs.info('API called using POST request and store into response object')
        finalreponse = response.json()
        self.logs.info('Parse JSON content of http request')
        print(finalreponse)
        if response.status_code==200:
            print('API run successfully')
            self.logs.info(f'Published successfully {finalreponse}')
        
        elif response.status_code!=200:
            print(f'Unable to publish the job and received error {response.status_code}')

   # @pytest.mark.skip
    def test_makedraft(self):
        
        url = testdata.testurl

        data = {
    "query": "\n  mutation MakeDraft($jobId: String!) {\n    makeDraft(jobId: $jobId) {\n      _id\n      draft {\n        _id\n      }\n    }\n  }\n",
    "variables": {
        "jobId": Testhire.ids
    },
    "operationName": "MakeDraft"
}
        payload = json.dumps(data)

        headers  = {'Authorization':f'Bearer {self.token}',
        'Content-Type': 'application/json'
          }
        response = requests.request('POST',url,headers=headers,data=payload)
        finalresponse = response.json()
        print(response.text)
        path_exp = parse('$.data.makeDraft.draft._id')
        matches = [match.value for match in path_exp.find(finalresponse)]
        Testhire.draftids = '-'.join(matches)
        print(Testhire.draftids)
        return Testhire.draftids


    #@pytest.mark.run('third')
    #@pytest.mark.skip
    def test_getjob(self):
        
        
        #self.dataid = Testhire.test_addjob(self) #This is how we can use variable of one method into antoher method of class

        url = testdata.testurl

        data = {
  "query": "\n  query GetJob($jobId: String) {\n    getJob(jobId: $jobId) {\n      _id\n      publish {\n        _id\n        title\n        description\n        minQualificationScore\n        maxAssessmentDuration\n        isAssessmentEnabled\n        allowTabSwitching\n        videoIntro {\n          checked\n          required\n        }\n        resume {\n          checked\n          required\n        }\n        experience {\n          checked\n          required\n        }\n        location {\n          checked\n          required\n        }\n        currentSalary {\n          checked\n          required\n        }\n        expectedCTC {\n          checked\n          required\n        }\n        website {\n          checked\n          required\n        }\n        kpis\n        questions {\n          _id\n          question\n          type\n          importance\n          options {\n            label\n            isCorrect\n          }\n          versionId\n          attachment {\n            id\n            name\n            type\n            url\n            downloadUrl\n            timestamp\n            size\n          }\n        }\n        metaTitle\n        slug\n        metaDescription\n        employmentType\n        category\n        country {\n          name\n          isoCode\n        }\n        city\n        state\n        createdAt\n        updatedAt\n      }\n      draft {\n        _id\n        title\n        description\n        minQualificationScore\n        maxAssessmentDuration\n        isAssessmentEnabled\n        allowTabSwitching\n        videoIntro {\n          checked\n          required\n        }\n        resume {\n          checked\n          required\n        }\n        experience {\n          checked\n          required\n        }\n        location {\n          checked\n          required\n        }\n        currentSalary {\n          checked\n          required\n        }\n        expectedCTC {\n          checked\n          required\n        }\n        website {\n          checked\n          required\n        }\n        kpis\n        questions {\n          _id\n          question\n          type\n          importance\n          options {\n            label\n            isCorrect\n          }\n          versionId\n          attachment {\n            id\n            name\n            type\n            url\n            downloadUrl\n            timestamp\n            size\n          }\n        }\n        metaTitle\n        slug\n        metaDescription\n        employmentType\n        category\n        country {\n          name\n          isoCode\n        }\n        city\n        state\n        createdAt\n        updatedAt\n      }\n      status\n      createdBy\n      publishedAt\n      team {\n        userId\n        user {\n          userId\n          email\n          firstName\n          lastName\n          profileUri\n          color\n          jobTitle\n          phoneNumber\n          timezone\n          theme\n          privileges {\n            admin\n            creator\n          }\n        }\n        role\n        interviewRound\n        mailTemplate {\n          subject\n          body\n        }\n      }\n    }\n  }\n",
  "variables": {
    "jobId": Testhire.ids
        },
        
  "operationName": "GetJob"
}
        print(Testhire.ids)
        payload = json.dumps(data)
        
        headers = {'Authorization':f'Bearer {self.token}',
        'Content-Type': 'application/json'
          }
        
        response = requests.request('POST',url,headers=headers,data=payload)
        finalresponse = response.json()
        print(finalresponse)
        print('third')



   # @pytest.mark.skip
    def test_jobinsights(self):
      url = testdata.testurl

      payloaddata = {
    "query": "\n  query GetJobInsights {\n    getJobInsights {\n      insights {\n        _id\n        jobInsights {\n          qualifiedCandidates\n          totalCandidates\n          avgScore\n          shortlisted\n          new\n          rejected\n          interview\n        }\n        interviewInsights {\n          interviewRounds {\n            interviewRound\n            count\n          }\n        }\n      }\n    }\n  }\n",
    "operationName": "GetJobInsights"
  }
      
      payload = json.dumps(payloaddata)


      headers = {'Authorization':f'Bearer {self.token}',
          'Content-Type': 'application/json'
            }
      
      response = requests.request('POST',url=url,data=payload,headers=headers)
      finalesponse = response.json()
      print('Here is all job insights',finalesponse)    
     


    #@pytest.mark.skip
    def test_deletejob(self):
        url = testdata.testurl

        data =  {
    "query": "\n  mutation DeleteJob($jobId: String!) {\n    deleteJob(jobId: $jobId)\n  }\n",
  "variables": {
    "jobId": Testhire.ids
  },
  "operationName": "DeleteJob"
}
        
        payload = json.dumps(data)

        headers  = {'Authorization':f'Bearer {self.token}',
        'Content-Type': 'application/json'
          }
        response = requests.request('POST',url,headers=headers,data=payload)

        finalreponse = response.json()
        self.logs.info(f'Job deleted successfully {finalreponse}')
        print(finalreponse)
