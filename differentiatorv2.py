from kubernetes import config, client

# Load your cluster configuration
config.load_kube_config()

# Get the namespaces to compare
namespace1 = input("Enter the first namesapce: ")
namespace2 = input("Enter the namespace you want to compare with: ")
print(f"\nThe 2 namespaces to be compared are '{namespace1}' and '{namespace2}'\n")

# Get Kubernetes API client
v1 = client.AppsV1Api()

def compare_deployment_envs(deployment_name, namespace1, namespace2):
   #Compares environment variables of a deployment between two namespaces.

   try:
       dep1 = v1.read_namespaced_deployment(deployment_name, namespace1)
       dep2 = v1.read_namespaced_deployment(deployment_name, namespace2)

       # Handle potential lack of environment variables
       env1_names = {env.name for env in dep1.spec.template.spec.containers[0].env or []}
       env2_names = {env.name for env in dep2.spec.template.spec.containers[0].env or []}

       mismatching_envs = env1_names.symmetric_difference(env2_names)

       if mismatching_envs:
           print('-' * 100)
           print(f"Deployment '{deployment_name}' has mismatched environment variables:\n")
           for env in mismatching_envs:
               print(f"- {env}")  # Print only the mismatched variable names
           print('-' * 100)
       else:
           print('-' * 100)
           print(f"\nDeployment '{deployment_name}' has matching environment variables.\n")
           print('-' * 100)

   except client.rest.ApiException as e:
       print(f"Error: {e}")

# Get a list of matching deployment names
deployments1 = v1.list_namespaced_deployment(namespace1).items
deployments2 = v1.list_namespaced_deployment(namespace2).items

matching_names = set([dep.metadata.name for dep in deployments1]) & set([dep.metadata.name for dep in deployments2])

for deployment_name in matching_names:
   compare_deployment_envs(deployment_name, namespace1, namespace2)
