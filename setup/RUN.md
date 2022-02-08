# Settin-up and running:

## Setup requiremenets (once):
### virtualenv tool is recommended for local only requirement installations.
while in project root:
```bash
sudo apt install python3-pip
pip install virtualenv
source ~/.profile
## in project folder:
virtualenv .kubespray-ve
source .kubespray-ve/bin/activate
sudo pip3 install -r requirements.txt

deactivate
```
NOTE: `python3-env` (`python3-virtualenv` ??) is the reccommended way. It is installed via apt /iof pip. Rest should be the same, but not tested.
//TODO: replace python3-env with virtualenv in docs, when tested.

```bash
sudo apt install python3-virtualenv
### rest is the same, but try to refrain from using sudo when installing stuff.
```

## in each project run:
while in project root:

```bash
virtualenv .kubespray-ve
## .. do some work, like lots of: 
  # ansible-playbook -i inventory/$CLUSTER_FOLDER/hosts.yaml -u kos -b -v --private-key=~/.ssh/id_rsa cluster.yml 2>&1 | tee ansible_run_01-out.tx
## when finished working with the repo, run:
deactivate
```

## Once:
while in project root:
```bash
# prepare folder for cluster
$ declare -r CLUSTER_FOLDER='my-cluster'
    ## NOTE: do not run any of the below two lines, if you only intend to work on 'my-cluster'.
    # for remote installation
    cp -rfp inventory/sample inventory/$CLUSTER_FOLDER
    # for local installation
    cp -rfp inventory/local inventory/$CLUSTER_FOLDER
    ## There is already a 'my-cluster' in inventory folder. Don't overwrite it!!!

## change the ip to your target machine
$ declare -a IPS=(192.168.122.154)
$ CONFIG_FILE=inventory/$CLUSTER_FOLDER/hosts.yaml python3 contrib/inventory_builder/inventory.py ${IPS[@]}
```

..checked & corrected k8s IPVS mode and metallb problem...

## (for each) run :
while in project root (, don't forget virtualenv stuff, before and after, once):
```bash
declare -r CLUSTER_FOLDER='my-cluster'
ansible-playbook -i inventory/$CLUSTER_FOLDER/hosts.yaml -u kos -b -v --private-key=~/.ssh/id_rsa cluster.yml 2>&1 | tee setup/ansible-run-01.log
```

## add ingress lb service:
apply `setup/nginx-ingress-controller-lb-service.yaml`
### disable hostports, if u want:
```bash
kubectl -n ingress-nginx edit daemonset.apps/ingress-nginx-controller
## comment all (3) hostPort s..
```

## in the guest machine:
copy config for current user:
```bash
mkdir -p $HOME/.kube
sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

## update from upstream:

```bash
git remote add upstream git@github.com:kubernetes-sigs/kubespray.git
git pull -X theirs upstream release-2.18
## make changes, add and commit..
git push
## do not forget to commit and push the main module, since it holds a reference to submodule HEAD's.
cd ../..
## make changes, add and commit
git push
```