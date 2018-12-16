* Simple server part for quizz application
In the manifest/ subdirectory there are the files for kubernetes deployment


* Instructions for GCP GKE deployment:

First we set up gcloud to connect to the gcloud project :
gcloud config set project mytestproject-225717

(kubecl GKE api must be enabled)
kubectl config use-context gke_mytestproject-225717_europe-west1-b_test-cluster

Then we create a 
gcloud container clusters create test-cluster --num-nodes=3 --enable-ip-alias

gcloud compute --project=mytestproject-225717 disks create redis-disk --zone=europe-west1-b --type=pd-ssd --size=1GB


Build de container : (cloud build api must be authorized)
git clone https://github.com/omerlin/kubquizz.git
cd kubquizz/server
gcloud builds submit --tag eu.gcr.io/mytestproject-225717/srvquizz:v1 .

gcloud compute addresses create srvapp-ip --region europe-west1
gcloud compute addresses describe srvapp-ip --region europe-west1



