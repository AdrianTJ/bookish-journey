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

echo Setting IDs
gcloud ai models list --region=us-central1 --filter=meanshift > temp.txt
meanshift_model_id=$(awk -F ' ' 'FNR == 2 {print $1}' temp.txt)
sed -i '/meanshift_model/d' GCP_model_details.yaml
echo -e '\n'meanshift_model_id: $(awk -F ' ' 'FNR == 2 {print $1}' temp.txt) >> GCP_model_details.yaml

gcloud ai endpoints list --region=us-central1 --filter=meanshift > temp.txt
meanshift_endpoint_id=$(awk -F ' ' 'FNR == 2 {print $1}' temp.txt)
sed -i '/meanshift_endpoint/d' GCP_model_details.yaml
echo -e '\n'meanshift_endpoint_id: $(awk -F ' ' 'FNR == 2 {print $1}' temp.txt) >> GCP_model_details.yaml
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