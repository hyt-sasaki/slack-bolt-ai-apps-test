#!/bin/bash

# Cloud Run deployment script for Slack AI Chatbot

# Set project variables
PROJECT_ID=${GCP_PROJECT_ID:-"your-project-id"}
SERVICE_NAME="slack-ai-chatbot"
REGION=${GCP_REGION:-"us-central1"}
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying Slack AI Chatbot to Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Service: ${SERVICE_NAME}"
echo "Region: ${REGION}"

# Build and push the Docker image
echo "📦 Building Docker image..."
gcloud builds submit --tag ${IMAGE_NAME} .

if [ $? -ne 0 ]; then
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 3000 \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --set-env-vars "LOG_LEVEL=INFO" \
    --set-env-vars "PORT=3000"

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "📡 Getting service URL..."
    SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')
    echo "🌐 Service URL: ${SERVICE_URL}"
    echo ""
    echo "📝 Next steps:"
    echo "1. Update your Slack app's Request URL to: ${SERVICE_URL}/slack/events"
    echo "2. Set environment variables for Slack tokens"
    echo "3. Configure Google Cloud credentials"
else
    echo "❌ Deployment failed"
    exit 1
fi