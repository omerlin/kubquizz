# Simple server part for quizz application
In the manifest/ subdirectory there are the files for kubernetes deployment
We explain here the deployment on GC

## pre-requisites

*(kubectl GKE api must be enabled)*
```
sudo /opt/google-cloud-sdk/bin/gcloud components install kubectl
```

You need first a project code, a region and zone
```
PROJECT=xxxxx
REGION=europe-west1
ZONE=europe-west1-b
```
First we set up gcloud to connect to the gcloud project :
```
gcloud config set project $PROJECT
gcloud container clusters get-credentials test-cluster
```

*(we potentially have to set the kubectl context if we are multi project )*
```
kubectl config get-contexts
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


