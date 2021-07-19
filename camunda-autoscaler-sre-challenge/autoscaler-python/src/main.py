import logging
import datetime
import os
import time
import json
import requests
from kubernetes import client, config


#Kubernetes API

#config.load_kube_config() # Enable it while running script standalone
config.load_incluster_config()

#self.k8s_client_api = client.CoreV1Api()
#self.k8s_client_custom = client.CustomObjectsApi()

class Autoscalar:
    def __init__(self):

        """
        Initialise the params
        API endpoint to fetch process count
        """
        self.camunda_url = os.getenv('CAMUNDA_URL', 'http://camunda-service:8080/')
        self.api = os.getenv('CAMUNDA_API', 'engine-rest/history/process-instance/count')

        """Process cycle and scaling policy paramas"""

        self.delay = int(os.getenv('DELAY', '8'))
        """Camunda engine deployment name and namespace"""

        self.deploy_name = os.getenv('DEPLOY_NAME', "camunda-deployment")
        self.namespace = os.getenv('namespace', "default")
        self.process_cycle = int(os.getenv('PROCESS_CYCLE', '10'))
        self.k8s_client_apps = client.AppsV1Api()



    def format_date_camunda(self, date_time: datetime.datetime) -> str:
        """
        Returns a date time string for a using in a REST API call to Camunda Engine
        + is NOT URL-escaped

        Args:
            date_time: datetime.datetime object to convert

        Returns:
            str: String in the yyyy-MM-ddTHH:mm:ss.SSSZ format

        Example:
            date_time: datetime.datetime(2021, 1, 31, 12, 34, 56, 789000,
                tzinfo=datetime.timezone(datetime.timedelta(seconds=3600), 'CEST'))
            returns: 2021-01-31T12:34:56.789+0100
        """
        date = date_time.astimezone().isoformat(sep='T', timespec='milliseconds').replace('+', '%2b')
        return ''.join(date.rsplit(':', 1))

    def get_replica_count(self):

        """Get the replica count of deployment type in a namespace"""
        n_replicas = 0
        try:
            resp = self.k8s_client_apps.read_namespaced_deployment(
                self.deploy_name,
                self.namespace)
            if resp.status.available_replicas:
                n_replicas = resp.status.available_replicas
            else:
                logging.info("Available replica of deployment %s ", resp.status.available_replicas)
        except client.exceptions.ApiException as errh:
            logging.info("Not Found Error: %s", errh)
        except Exception as exc:
                logging.info("Error: %s", exc)
        return n_replicas
           

    def scale_deployment(self, replica_count):

        """Scale deployment to replica_count args self.deploy_name, self.namespace"""
        status = ""
        try:
            status = self.k8s_client_apps.patch_namespaced_deployment_scale(
                self.deploy_name,
                self.namespace,
                body={"spec":{"replicas":replica_count}})
        except client.exceptions.ApiException as errh:
            logging.info("Not Found Error: %s", errh)
        except Exception as exc:
            logging.info("Error: %s", exc)
        return status

    def patch_replica_scale(self, process_started):

        """
        Apply a deployment patch to scale-up/scale-down replica count
        Get the current replica count of deployment type in a namespace
        """
        n_replicas = self.get_replica_count()

        process_min_per_instance = int(os.getenv('PROCESS_MIN_PER_INSTANCE', '20'))
        process_max_per_instance = int(os.getenv('PROCESS_MAX_PER_INSTANCE', '50'))
        pod_max_scale = int(os.getenv('POD_MAX_SCALE', '4'))
        status = ""

        if n_replicas > 0:

            # Num of processes/node = process started N seconds/total num of pods
            # Evaluating process load and scaling policy accordingly
            # process_per_instance : process started per instance
            process_per_instance = int(process_started//n_replicas)


            if (process_per_instance >= process_max_per_instance) & (n_replicas < pod_max_scale):

                #Scaling up replica count

                logging.info("Camunda Engine Replicas: %s, "
                             "Process started in the last %s seconds: %s, "
                             "processes per instance: %s ",
                             n_replicas,
                             self.process_cycle,
                             process_started,
                             process_per_instance)
                logging.info("Action: Scaling up")
                status = self.scale_deployment(n_replicas+1)
                if status:
                    logging.info("Status of scaling request: %s", status.spec)

            elif (process_per_instance <= process_min_per_instance) & (n_replicas > 1):

                #Scaling down replica count

                logging.info("Camunda Engine Replicas: %s, "
                             "Process started in the last %s seconds: %s, "
                             "processes per instance: %s ",
                             n_replicas,
                             self.process_cycle,
                             process_started,
                             process_per_instance)
                logging.info("Action: Scaling down")
                status = self.scale_deployment(n_replicas-1)
                if status:
                    logging.info("Status of scaling request: %s", status.spec)
            else:
                logging.info("Camunda Engine Replicas: %s, "
                             "Process started in the last %s seconds: %s, "
                             "processes per instance: %s ",
                             n_replicas,
                             self.process_cycle,
                             process_started,
                             process_per_instance)
                logging.info("Action: Not scaling")


    def main(self):
        """
        Calculating timestamp for current time - N seconds (process_cycle)
        """
        while True:

            timestamp = self.format_date_camunda(
                datetime.datetime.now() - datetime.timedelta(seconds=self.process_cycle))
            request_param = {'startedAfter':timestamp}
            logging.info("Load monitor at process_cycle %s at : %s", self.process_cycle, timestamp)
            api = self.camunda_url+self.api
            #HEADERS = {'Content-Type': 'application/json'}
            #self.patch_replica_scale(100)

            #Calling Camunda engine rest api to get the current process count:

            try:
                response = requests.get(api, params=json.dumps(request_param), timeout=3)
                response.raise_for_status()
                response_data = response.json()
                logging.info("Process count: %s", response_data)
                self.patch_replica_scale(response_data['count'])
            except requests.exceptions.HTTPError as errh:
                logging.info("Http Error: %s", errh)
            except requests.exceptions.ConnectionError as errc:
                logging.info("Error Connecting: %s", errc)
            except requests.exceptions.Timeout as errt:
                logging.info("Timeout Error: %s", errt)
            except requests.exceptions.RequestException as err:
                logging.info("Oops: Something went wrong while getting response from Camunda engine: %s", err)
            except Exception as exc:
                logging.info("Error: %s", exc)

            time.sleep(self.delay)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)-15s: %(levelname)-8s: %(message)s")
    logging.info("Starting server load for process_cycle ")
    AUTOSCALER = Autoscalar()
    AUTOSCALER.main()
