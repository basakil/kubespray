# Settin-up and running:


while in project root:

## Once:
```bash
# Define a folder name
$ declare -r CLUSTER_FOLDER='my-cluster'
# This for remote installation
cp -rfp inventory/sample inventory/$CLUSTER_FOLDER
# This for local installation
cp -rfp inventory/local inventory/$CLUSTER_FOLDER

# For remote installation provide the ip address
$ declare -a IPS=(192.168.122.154)
$ CONFIG_FILE=inventory/$CLUSTER_FOLDER/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```

check & correct k8s IPVS mode and metallb problem.

## for each run:
```bash
declare -r CLUSTER_FOLDER='my-cluster'
ansible-playbook -i inventory/$CLUSTER_FOLDER/hosts.yaml -u kos -b -v --private-key=~/.ssh/id_rsa cluster.yml 2>&1 | tee setup/ansible-run-01.log
```
