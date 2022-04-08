echo Setting up envirement variables
. ./GCP_variables.sh
printf "Done\n\n"

echo Setting project up
gcloud config set project $project_id
printf "Done\n\n"

echo Enabling APIs
gcloud services enable compute.googleapis.com \
                         containerregistry.googleapis.com \
                         aiplatform.googleapis.com \
                         cloudbuild.googleapis.com
printf "Done\n\n"

echo Making a bucket, if it exists, returns error
gsutil mb -l us-central1 $bucket_path
printf "Done\n\n"