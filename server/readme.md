= Simple server part for quizz application
In the manifest/ subdirectory there are the files for kubernetes deployment
We explain here the deployment on GCP

== pre-requisites

(kubecl GKE api must be enabled)

First we set up gcloud to connect to the gcloud project :
gcloud config set project mytestproject-225717
gcloud container clusters get-credentials test-cluster

(we potentially have to set the kubectl context if we are multi project )
kubectl config get-contexts
kubectl config set-context gke_mytestproject-225717_europe-west1-b_test-cluster

== Kubernetes setup

gcloud container clusters create test-cluster --num-nodes=3 --enable-ip-alias

gcloud compute --project=mytestproject-225717 disks create redis-disk --zone=europe-west1-b --type=pd-ssd --size=1GB


Build de container : (cloud build api must be authorized)
git clone https://github.com/omerlin/kubquizz.git
cd kubquizz/server
gcloud builds submit --tag eu.gcr.io/mytestproject-225717/srvquizz:v1 .

gcloud compute addresses create srvapp-ip --region europe-west1
gcloud compute addresses describe srvapp-ip --region europe-west1

Then add the external IP in the srvapp-service.yml LoadBalancer configuration


