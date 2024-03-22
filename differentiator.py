import json
import sys
from kubernetes import client, config

# Load the kubeconfig file
config.load_kube_config()

# Define deployment names and namespaces
deployment_name = input("Enter the target deployment: ")
namespace1 = input("Enter the namespace of the target deployment: ")
print("The target deployment and namespace are:", deployment_name, ",", namespace1)
namespace2 = input("Enter the namespace to be compared: ")
print("The deployment and namespace to be comapred are:", deployment_name, ",", namespace2)

# Create a CoreV1Api instance
v1 = client.AppsV1Api()

try:
    # Get the specific deployment information
    deployment1 = v1.read_namespaced_deployment(deployment_name, namespace1)
    deployment2 = v1.read_namespaced_deployment(deployment_name, namespace2)

    # Get the environment variables for each deployment
    container1 = deployment1.spec.template.spec.containers[0]
    container2 = deployment2.spec.template.spec.containers[0]
    env_vars1 = container1.env
    env_vars2 = container2.env

    # Extract key names from V1EnvVar objects
    env_vars1_names = {env_var.name for env_var in env_vars1}
    env_vars2_names = {env_var.name for env_var in env_vars2}

    # Find keys present only in one deployment
    keys_only_in_deployment1 = env_vars1_names - env_vars2_names
    keys_only_in_deployment2 = env_vars2_names - env_vars1_names

    # Print the differences
    if len(keys_only_in_deployment1) == 0 and len(keys_only_in_deployment2) == 0:
        print(deployment_name, "has matched")
    else:
        print("Keys only in", namespace1,":", keys_only_in_deployment1)
        print("Keys only in", namespace2,":", keys_only_in_deployment2)

except client.exceptions.ApiException as e:
    print(f"API error: {e}")

