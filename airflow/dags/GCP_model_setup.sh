# Grab environment variables from another file, we don't store them here becasue they contain sensitive information. 
echo Setting up envirement variables
. ./GCP_variables.sh
printf "Done\n\n"

# Set up project ID, we use it when we enable APIs 
echo Setting project up
gcloud config set project $project_id
printf "Done\n\n"

# Enable the APIs that we use in the VertexAI workflow
echo Enabling APIs
gcloud services enable compute.googleapis.com \
                         containerregistry.googleapis.com \
                         aiplatform.googleapis.com \
                         cloudbuild.googleapis.com
printf "Done\n\n"

# Create a bucket, where the models and files will be stored. 
echo Making a bucket, if it exists, returns error
gsutil mb -l us-central1 $bucket_path
printf "Done\n\n"
