

Steps to build execute the autoscaler

- 1) Build the Docker image from Dockerfile.
     eg: docker build -t local.registry/camunda-autoscaler:1.0.0
- 2) We have default values but we can edit configurable parameters.
- 3) Deploy the autoscalar deployemnt.
     kubectl apply -f autoscaler.yml : This will create following resources
        a) ServiceAccount:camunda-autoscaler
        b) Role: camunda-autoscaler
        c) Rolebinding: camunda-autoscaler
        d) deployment pod:
- 4) default namespace deployment is : default        

Configurable parameters (Examples):
- name: CAMUNDA_URL
  value: "http://camunda-service:8080/"
- name: CAMUNDA_API
  value: "engine-rest/history/process-instance/count"
- name: DELAY
  value: "10"
- name: DEPLOY_NAME
  value: camunda-deployment
- name: PROCESS_CYCLE
  value: "10"
- name: PROCESS_MIN_PER_INSTANCE
  value: "20"
- name: PROCESS_MAX_PER_INSTANCE
  value: "50"
- name: POD_MAX_SCALE
  value: "4"

Note : Added few sample test case execution under test-case-log  