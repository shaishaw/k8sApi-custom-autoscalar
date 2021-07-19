# Follow-up questions for the task

## How long did it take you to solve the exercise? Please be honest, we evaluate your answer to this question based on your experience.

- Overall excercise to work end to end with all the test case took me around 3-4 hrs. Let me segregate the work and effort metrics
  - main.py ~ 2hrs (End to end python cli test)
  - Lint fix for main.py ~30mins
  - rbac+deployment manifest ~ 30mins
  - Multiple use case test with end to end and bug fixes. ~ 2hrs 

## Which additional steps would you take in order to make this code production ready? Why?

- Code improvement: 
  Optimise main.py to move out from while True condition to application server.
  Create a wrapper class for basic k8s api methods.
  Should have a healthcheck endpoint

- Kubernetes yaml: 
  Resource{limits:"", resources: ""} must be estimateed properly and updated before moving to prod
  Add probes: Liveness/Readiness
  Node selectors : This should be must to have as this can estimate the pod and and available resources. 


## Which step took most of the time? Why?

- Fixing Lint warnings/erros and kubernetes API config while making API calls from pod. I had spend sometime to read about the python-k8s api
  calls while running from a pod.

## Do you have any feedback for us? (Any mistakes you've found in the challenge, something was not working with your setup, you've lost a lot of time with something avoidable etc.)

- The overall assignment is well crafted and I really enjoyed while working on it.

- While running multiple test cases I see that the job submitted to the camunda-engine is not processed and keep building.
  
  ex: Scenario-1 
      - make scale N=20; This will keep submitting the process.
      - let say after sometime it reached to a state where the process count to 501 & replica count scaled to 4.
      - make scale N=2; this will change the process submition rate but the api will return process count as 503 and so on.
    
-  I was bit stuck here how to test the other scenario like sscaling down ? I did test that manually after tearing down and building back the        cluster. There should be some other way which I have not tried though.
           

- I have faced issue only with the process-started image. Pod is continously running in Imagepullback state and was not able to pull image
  eg: Events:
        Warning  Failed     3s (x2 over 19s)  kubelet            Failed to pull image "registry.camunda.cloud/library/sre-interview-process-starter:1.0.19": rpc error: code = Unknown desc = failed to pull and unpack image "registry.camunda.cloud/library/sre-interview-process-starter:1.0.19": failed to resolve reference "registry.camunda.cloud/library/sre-interview-process-starter:1.0.19": failed to do request: Head https://registry.camunda.cloud/v2/library/sre-interview-process-starter/manifests/1.0.19: x509: certificate signed by unknown authority
        Warning  Failed     3s (x2 over 19s)  kubelet            Error: ErrImagePull 
