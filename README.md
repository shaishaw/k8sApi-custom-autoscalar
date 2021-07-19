# SRE Coding Challenge (Camunda Engine Kubernetes Autoscaler)

This challenge includes a test framework, that:

- allows the candidates to less time on setting up the environment for the autoscaler
- allows both the candidates and the evaluators to check if the submitted solutions works as expected

# File Structure

## settings.sh

A candidate needs to place the language of their choice and well as their name, for the test
framework to work.

## Makefile

The main entrypoint to invoke different commands from the test framework:

- **make build**: Builds the autoscaler app and pushes the docker image to local kind registry
- **make check**: Checks all required tools are installed
- **make create**: Creates local kind cluster
- **make deploy**: Deploys autoscaler
- **make full-test**: Runs the full testing suite
- **make help**: This help
- **make lint**: Runs linters, check missing TODOs
- **make prepare**: Installs PostgreSQL, Camunda Engine, Process Starter in the local kind cluster
- **make scale**: Changes Process Starter's Process Creation rate (usage: make scale N=...)
- **make teardown**: Destroys local kind cluster and registry
- **make test**: Runs basic tests to check that autoscaler works

A candidate does not need to touch this file.

## Questions.md

A list of questions for the candidate to answer.

## autoscaler-*

These are the directories where a candidate needs to place the code for their autoscaler app 
(based on the language of their choice.)

## k8s-resources

Includes Kubernetes manifests for the Camunda Engine, PostgreSQL and Process Starter components.

A candidate needs to place the manifests for deploying their autoscaler app in the `autoscaler.yml` file.

## Scripts

Auxilliary scripts using by the `make` targets.

A candidate does not need to touch those.
A candidate normally does not need to run these directly.

- **_library.sh**: Library of the most-used reusable functions of the test framework
- **build-push-autoscaler.sh**: Builds autoscaler's docker image and pushes it to the registry of the test cluster
- **check-installed-tools.sh**: Checks that the required utilities for the challenge are installed (e.g. Docker)
- **check-todos.sh**: Checks that the TODOs are fixed by the candidate
- **codestyle.sh**: Runs a linter for the autoscaler code
- **create-kind-cluster.sh**: Creates a test kind cluster with the name from `settings.sh`
- **delete-kind-cluster.sh**: Deletes a test kind cluster and its registry
- **deploy-autoscaler.sh**: Deploys autoscaler app in the test cluster
- **deploy-camunda.sh**: Deploys Camunda Engine in the test cluster
- **deploy-postgresql.sh**: Deploys PostgreSQL in the test cluster
- **deploy-process-starter.sh**: Deploys Process Starter in the test cluster
- **parselog.sh**: Parses test log and outputs various stats on it
- **test-autoscaler.sh**: Tests the autoscaler's behaviour for different process creation rates.

++++++++++++++++++++++ Full Test of  code execution +++++++++++++++++

REMMACF0NHJG5M:camunda-sre-interview-1.0.1 sshashank$ make full-test
/Library/Developer/CommandLineTools/usr/bin/make start-log
Saving logfile to: /var/folders/qk/m0lc3hcd4yj45_hxygxn0zyry_h2dh/T/tmp.J55LyLCw
/Library/Developer/CommandLineTools/usr/bin/make check || ( /Library/Developer/CommandLineTools/usr/bin/make end-log ; exit 1 )
./scripts/check-installed-tools.sh
[Tue Jun 22 19:52:23 IST 2021] --------------------------------------------------
[Tue Jun 22 19:52:23 IST 2021] [TEST] Checking that docker is installed
[Tue Jun 22 19:52:23 IST 2021] --------------------------------------------------
[Tue Jun 22 19:52:24 IST 2021] [PASS] docker is installed
[Tue Jun 22 19:52:24 IST 2021] [INFO] Docker version 20.10.6, build 370c289
[Tue Jun 22 19:52:24 IST 2021] [INFO] Docker daemon is runnning
[Tue Jun 22 19:52:24 IST 2021] --------------------------------------------------
[Tue Jun 22 19:52:24 IST 2021] [TEST] Checking that kubectl is installed
[Tue Jun 22 19:52:24 IST 2021] --------------------------------------------------
[Tue Jun 22 19:52:24 IST 2021] [PASS] kubectl is installed
[Tue Jun 22 19:52:24 IST 2021] [INFO] Client Version: version.Info{Major:"1", Minor:"21", GitVersion:"v1.21.2", GitCommit:"092fbfbf53427de67cac1e9fa54aaa09a28371d7", GitTreeState:"clean", BuildDate:"2021-06-16T12:59:11Z", GoVersion:"go1.16.5", Compiler:"gc", Platform:"darwin/amd64"}
[Tue Jun 22 19:52:24 IST 2021] --------------------------------------------------
[Tue Jun 22 19:52:24 IST 2021] [TEST] Checking that kind is installed
[Tue Jun 22 19:52:24 IST 2021] --------------------------------------------------
[Tue Jun 22 19:52:24 IST 2021] [PASS] kind is installed
[Tue Jun 22 19:52:24 IST 2021] [INFO] kind version 0.9.0
/Library/Developer/CommandLineTools/usr/bin/make bootstrap || ( /Library/Developer/CommandLineTools/usr/bin/make end-log ; exit 1 )
./scripts/create-kind-cluster.sh
No kind clusters found.
Creating cluster "shaishaw.shashank" ...
 ✓ Ensuring node image (kindest/node:v1.19.1) 🖼
 ✓ Preparing nodes 📦
 ✓ Writing configuration 📜
 ✓ Starting control-plane 🕹️
 ✓ Installing CNI 🔌
 ✓ Installing StorageClass 💾
Set kubectl context to "kind-shaishaw.shashank"
You can now use your cluster with:

kubectl cluster-info --context kind-shaishaw.shashank

Thanks for using kind! 😊
./scripts/deploy-postgresql.sh
Context "kind-shaishaw.shashank" modified.
[Tue Jun 22 19:53:10 IST 2021] [INFO] Deploying PostgreSQL for Camunda Engine
statefulset.apps/postgresql created
service/db created
[Tue Jun 22 19:53:14 IST 2021] [INFO] Waiting for PostgreSQL to be ready
Waiting for pod to be ready
error: no matching resources found
pod not created yet
Waiting for pod to be ready
error: no matching resources found
pod not created yet
Waiting for pod to be ready
pod/postgresql-0 condition met
./scripts/deploy-camunda.sh
Context "kind-shaishaw.shashank" modified.
[Tue Jun 22 19:54:43 IST 2021] [INFO] Deploying Camunda Engine
service/camunda-service created
deployment.apps/camunda-deployment created
[Tue Jun 22 19:54:45 IST 2021] [INFO] Waiting for Camunda Engine to be ready
deployment.apps/camunda-deployment condition met
Waiting for Camunda Engine pods to be ready...
Waiting for Camunda Engine pods to be ready...
Waiting for Camunda Engine pods to be ready...
Waiting for Camunda Engine pods to be ready...
Waiting for Camunda Engine pods to be ready...
Waiting for Camunda Engine pods to be ready...
./scripts/deploy-process-starter.sh 0
Context "kind-shaishaw.shashank" modified.
[Tue Jun 22 19:55:46 IST 2021] [INFO] Deploying Camunda Process Starter
deployment.apps/camunda-process-starter created
[Tue Jun 22 19:55:49 IST 2021] [INFO] Adjusting Process Starter rate to 0 processes created per period
[Tue Jun 22 19:55:49 IST 2021] [INFO] Waiting for Process Starter to be ready
Waiting for deployment "camunda-process-starter" rollout to finish: 0 of 1 updated replicas are available...
deployment "camunda-process-starter" successfully rolled out
deployment.apps/camunda-process-starter condition met
/Library/Developer/CommandLineTools/usr/bin/make lint || ( /Library/Developer/CommandLineTools/usr/bin/make end-log ; )
./scripts/check-todos.sh
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [TEST] Check that todos are addressed in Questions.md
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [PASS] No TODOs found in /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/..//Questions.md
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [TEST] Check that todos are addressed in autoscaler.yml
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [PASS] No TODOs found in /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/..//k8s-resources/autoscaler.yml
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [TEST] Check that todos are addressed in Dockerfile
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [PASS] No TODOs found in /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/../autoscaler-python/Dockerfile
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [TEST] Check that todos are addressed in README.md
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [PASS] No TODOs found in /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/../autoscaler-python/README.md
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [TEST] Check that todos are addressed in requirements.txt
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [PASS] No TODOs found in /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/../autoscaler-python/requirements.txt
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [TEST] Check that todos are addressed in main.py
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
grep: /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/../autoscaler-python/main.py: No such file or directory
[Tue Jun 22 19:55:57 IST 2021] [PASS] No TODOs found in /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/../autoscaler-python/main.py
./scripts/codestyle.sh
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
[Tue Jun 22 19:55:57 IST 2021] [TEST] Running a linter for your code
[Tue Jun 22 19:55:57 IST 2021] --------------------------------------------------
docker run --rm -v `pwd`:/data \
	  registry.camunda.cloud/library/cytopia/pylint@sha256:e8acf4bea77afd6a924e57fae1dfacdd5f7e288c3cc276d044a9a3a0719676f5 --rcfile=.pylintrc -s n src/__init__.py src/main.py
************* Module src.main
src/main.py:74:0: W0311: Bad indentation. Found 16 spaces, expected 12 (bad-indentation)
src/main.py:76:0: C0303: Trailing whitespace (trailing-whitespace)
src/main.py:40:4: R0201: Method could be a function (no-self-use)
src/main.py:73:15: W0703: Catching too general exception Exception (broad-except)
src/main.py:89:15: W0703: Catching too general exception Exception (broad-except)
src/main.py:186:19: W0703: Catching too general exception Exception (broad-except)
make[2]: *** [lint] Error 28
[Tue Jun 22 19:56:02 IST 2021] [WARN] Linting issues detected
/Library/Developer/CommandLineTools/usr/bin/make build || ( /Library/Developer/CommandLineTools/usr/bin/make end-log ; exit 1 )
./scripts/build-push-autoscaler.sh
[Tue Jun 22 19:56:02 IST 2021] --------------------------------------------------
[Tue Jun 22 19:56:02 IST 2021] [TEST] Applying code formatter to your autoscaler's code
[Tue Jun 22 19:56:02 IST 2021] --------------------------------------------------
...
[Tue Jun 22 19:56:02 IST 2021] [PASS] Autoformatted successfully
[Tue Jun 22 19:56:02 IST 2021] --------------------------------------------------
[Tue Jun 22 19:56:02 IST 2021] [TEST] Running linter for your Dockerfile
[Tue Jun 22 19:56:02 IST 2021] --------------------------------------------------
docker run --rm -i registry.camunda.cloud/library/hadolint/hadolint@sha256:c0aadd8ed276d99bd2d93661d8690f721b51c903600d58c73c00716879cfb718 < Dockerfile
[Tue Jun 22 19:56:04 IST 2021] [PASS] Dockerfile lint check passed
[Tue Jun 22 19:56:04 IST 2021] --------------------------------------------------
[Tue Jun 22 19:56:04 IST 2021] [TEST] Building Docker image of your autoscaler
[Tue Jun 22 19:56:04 IST 2021] --------------------------------------------------
make -C /Users/sshashank/dev/kubernetes/kind/camunda-sre-interview-1.0.1/scripts/../autoscaler-python build CLUSTER=shaishaw.shashank
docker build -t local.registry/camunda-autoscaler:1.0.0 .
[+] Building 13.6s (9/9) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                                                                     0.0s
 => => transferring dockerfile: 126B                                                                                                                                                                                                     0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                        0.0s
 => => transferring context: 2B                                                                                                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/python:3.9.2                                                                                                                                                                          2.7s
 => [internal] load build context                                                                                                                                                                                                        0.0s
 => => transferring context: 9.23kB                                                                                                                                                                                                      0.0s
 => [1/4] FROM docker.io/library/python:3.9.2@sha256:d5d25f8ddcf983c0164bdcdc87b330d31417e2ce302dbd3e1d0e90fddf3ddff1                                                                                                                    0.0s
 => CACHED [2/4] WORKDIR /opt                                                                                                                                                                                                            0.0s
 => [3/4] COPY . /opt/                                                                                                                                                                                                                   0.1s
 => [4/4] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                                                                            10.1s
 => exporting to image                                                                                                                                                                                                                   0.6s
 => => exporting layers                                                                                                                                                                                                                  0.6s
 => => writing image sha256:81a63b3b9d8719ad209e905cedfba38ccf12fadcf7a211ff440c06c582190fe2                                                                                                                                             0.0s
 => => naming to local.registry/camunda-autoscaler:1.0.0                                                                                                                                                                                 0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[Tue Jun 22 19:56:19 IST 2021] [PASS] Build and tagged successfully
[Tue Jun 22 19:56:19 IST 2021] --------------------------------------------------
[Tue Jun 22 19:56:19 IST 2021] [TEST] Pushing Docker image of your autoscaler to local kind registry
[Tue Jun 22 19:56:19 IST 2021] --------------------------------------------------
kind load docker-image local.registry/camunda-autoscaler:1.0.0 --name shaishaw.shashank
Image: "local.registry/camunda-autoscaler:1.0.0" with ID "sha256:81a63b3b9d8719ad209e905cedfba38ccf12fadcf7a211ff440c06c582190fe2" not yet present on node "shaishaw.shashank-control-plane", loading...


[Tue Jun 22 19:57:42 IST 2021] [PASS] Pushed successfully
/Library/Developer/CommandLineTools/usr/bin/make deploy || ( /Library/Developer/CommandLineTools/usr/bin/make end-log ; exit 1 )
./scripts/deploy-autoscaler.sh
Context "kind-shaishaw.shashank" modified.
[Tue Jun 22 19:57:42 IST 2021] [INFO] Deploying Camunda Deployment Autoscaler
serviceaccount/camunda-autoscaler created
role.rbac.authorization.k8s.io/camunda-autoscaler created
rolebinding.rbac.authorization.k8s.io/camunda-autoscaler created
deployment.apps/camunda-autoscaler created
deployment.apps/camunda-autoscaler restarted
[Tue Jun 22 19:57:45 IST 2021] [INFO] Waiting for Camunda Deployment Autoscaler to be ready
Waiting for deployment "camunda-autoscaler" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "camunda-autoscaler" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "camunda-autoscaler" rollout to finish: 1 old replicas are pending termination...
deployment "camunda-autoscaler" successfully rolled out
deployment.apps/camunda-autoscaler condition met
/Library/Developer/CommandLineTools/usr/bin/make test || ( /Library/Developer/CommandLineTools/usr/bin/make end-log ; exit 1 )
make[1]: `test' is up to date.
/Library/Developer/CommandLineTools/usr/bin/make teardown || ( /Library/Developer/CommandLineTools/usr/bin/make end-log ; exit 1 )
./scripts/delete-kind-cluster.sh
Do you want to delete kind cluster and all resources in it? (y/n) Do you want to delete kind cluster and all resources in it? (y/n)Do you want to delete kind cluster and all resources in it? (y/n)y
[Tue Jun 22 20:02:42 IST 2021] [INFO] Skipping cluster deletion
/Library/Developer/CommandLineTools/usr/bin/make end-log
./scripts/parselog.sh

Tests:       14, Passed:       13, Failed:        0, Warnings:        1

Summary of FAIL and WARN tests

[Tue Jun 22 19:55:57 IST 2021] [TEST] Running a linter for your code
[Tue Jun 22 19:56:02 IST 2021] [WARN] Linting issues detected

