echo Setting up envirement variables
. ./GCP_variables.sh
printf "Done\n\n"


echo Uploading Model
gcloud ai models upload \
  --region=$region \
  --display-name=$meanshift_display_name \
  --container-image-uri=$container_name \
  --artifact-uri=$meanshift_uri
printf "Done\n\n"

echo Creating endpoint
gcloud ai endpoints create \
  --region=$region \
  --display-name=$meanshift_endpoint_name
printf "Done\n\n"

echo Deploying Model
gcloud ai endpoints deploy-model $meanshift_endpoint_id \
  --region=$region \
  --model=$meanshift_model_id \
  --display-name=$meanshift_display_name \
  --machine-type=$machine_name \
  --min-replica-count=1 \
  --max-replica-count=1 \
  --traffic-split=0=100
printf "Done\n\n"