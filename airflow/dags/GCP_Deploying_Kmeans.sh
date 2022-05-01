# Get the local variables, we don't include them because they contain sensitive information
echo Setting up envirement variables
. ./GCP_variables.sh
printf "Done\n\n"

# Upload model to VertexAI
echo Uploading Model
gcloud ai models upload \
  --region=$region \
  --display-name=$kmeans_display_name \
  --container-image-uri=$container_name \
  --artifact-uri=$kmeans_uri
printf "Done\n\n"

# Create the endpoint that the model is going to be deployed to. 
echo Creating endpoint
gcloud ai endpoints create \
  --region=$region \
  --display-name=$kmeans_endpoint_name
printf "Done\n\n"

# From the newly created model and endpoint, grab their IDs, so that we can use them in the next step to deploy the model. 
echo Setting IDs
gcloud ai models list --region=us-central1 --filter=kmeans > temp.txt
kmeans_model_id=$(awk -F ' ' 'FNR == 2 {print $1}' temp.txt)
sed -i '/kmeans_model/d' GCP_model_details.yaml
echo -e '\n'kmeans_model_id: $(awk -F ' ' 'FNR == 2 {print $1}' temp.txt) >> GCP_model_details.yaml

gcloud ai endpoints list --region=us-central1 --filter=kmeans > temp.txt
kmeans_endpoint_id=$(awk -F ' ' 'FNR == 2 {print $1}' temp.txt)
sed -i '/kmeans_endpoint/d' GCP_model_details.yaml
echo -e '\n'kmeans_endpoint_id: $(awk -F ' ' 'FNR == 2 {print $1}' temp.txt) >> GCP_model_details.yaml
printf "Done\n\n"

# Deploy model to VertexAI
echo Deploying Model
gcloud ai endpoints deploy-model $kmeans_endpoint_id \
  --region=us-central1 \
  --model=$kmeans_model_id \
  --display-name=$kmeans_display_name \
  --machine-type=$machine_name \
  --min-replica-count=1 \
  --max-replica-count=1 \
  --traffic-split=0=100
printf "Done\n\n"
