# Simple server part for quizz application
In the manifest/ subdirectory there are the files for kubernetes deployment
We explain here the deployment on GC

## pre-requisites

* Project must be created 
* kubectl GKE api must be enabled
* gcloud tool must be installed

### gcloud installation
```
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-327.0.0-linux-x86_64.tar.gz
tar zxvf google-cloud-sdk-327.0.0-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh
#
# This command map with Oauth2 with your google account but also to project, region & zone
#
./google-cloud-sdk/bin/gcloud init
```


```
sudo /opt/google-cloud-sdk/bin/gcloud components install kubectl
```

To review configuration:
```
cat .config/gcloud/configurations/config_default
[core]
account = omerlin13@gmail.com
project = quizz022021

[compute]
zone = europe-west1-b
region = europe-west1
```


You need first a project code, a region and zone
```
export PROJECT=quizz022021
export REGION=europe-west1
export ZONE=europe-west1-b
```
First we set up gcloud to connect to the gcloud project :
```
gcloud config set project $PROJECT

```

*(we potentially have to set the kubectl context if we are multi project )*
```
kubectl config get-contexts
gcloud container clusters get-credentials test-cluster
# From: ~/.kube/config
MYCONTEXT=gke_mytestproject-225717_europe-west1-b_test-cluster
kubectl config set-context $MYCONTEXT
```
## Kubernetes setup

```
gcloud container clusters create test-cluster --num-nodes=3 --enable-ip-alias

gcloud compute --project=$PROJECT disks create redis-disk --zone=$ZONE --type=pd-ssd --size=1GB
```

### Build de container : 
*(cloud build api must be authorized)*
```
git clone https://github.com/omerlin/kubquizz.git
cd kubquizz/server
gcloud builds submit --tag eu.gcr.io/$PROJECT/srvquizz:v1 .
```
This create an image in the form : eu.gcr.io/$PROJECT/srvquizz:v1

### Optional: booking the External floating IP
```
gcloud compute addresses create srvapp-ip --region $REGION
gcloud compute addresses describe srvapp-ip --region $REGION
```

Then add the external IP in the srvapp-service.yml LoadBalancer configuration


