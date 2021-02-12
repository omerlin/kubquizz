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


ID                                    CREATE_TIME                DURATION  SOURCE                                                                                     IMAGES                             STATUS
c411e802-5e1a-47b3-87ed-06ba2dce0eff  2021-02-12T09:50:56+00:00  47S       gs://quizz022021_cloudbuild/source/1613123410.312352-511918710133477cbee02f257a9d959c.tgz  eu.gcr.io/quizz022021/srvquizz:v1  SUCCESS

```
This create an image in the form : eu.gcr.io/$PROJECT/srvquizz:v1

### Optional: **booking** the External floating IP

REMARK: This is not necessary, the service will provide one IP (sufficient in our case)

```
gcloud compute addresses create srvapp-ip --region $REGION
gcloud compute addresses describe srvapp-ip --region $REGION
```

Then add the external IP in the srvapp-service.yml LoadBalancer configuration

## Install srvapp application
cd ~/kubquizz/server
kubectl create configmap quizz-data --from-file=./resources/quizz.yml
kubectl create -f manifest/cm_redishost.yml
kubectl create -f manifest/redis.yml
kubectl create -f manifest/srvapp.yml
kubectl create -f manifest/srvapp-service.yml

vagrant@controller:~/kubquizz/server$ kubectl get svc
NAME         TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)        AGE
kubernetes   ClusterIP      10.120.0.1    <none>          443/TCP        137m
redis        ClusterIP      None          <none>          6379/TCP       41m
srvquizz     LoadBalancer   10.120.8.24   35.205.41.166   80:32640/TCP   12m

### mapping with gandi.net
quizz	A	1800	35.205.41.166

so ... now the server is accessible over internet on http://quizz.cossme.pw
