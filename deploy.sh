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

# Check if manifest.json has changed since last deployment
MANIFEST_CHANGED=false
if [ -f .last_deploy_manifest_hash ]; then
    LAST_HASH=$(cat .last_deploy_manifest_hash)
    CURRENT_HASH=$(sha256sum manifest.json | cut -d' ' -f1)
    if [ "$LAST_HASH" != "$CURRENT_HASH" ]; then
        MANIFEST_CHANGED=true
        echo "📋 manifest.json has changed since last deployment"
    fi
else
    MANIFEST_CHANGED=true
    echo "📋 First deployment or no previous manifest hash found"
fi

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
    
    # Save current manifest hash for future deployments
    sha256sum manifest.json | cut -d' ' -f1 > .last_deploy_manifest_hash
    
    # If manifest changed, prompt to update Slack app
    if [ "$MANIFEST_CHANGED" = true ]; then
        echo ""
        echo "🔄 manifest.json has changed. Slack Appの更新が必要です:"
        echo "1. 以下のコマンドでSlack Appを更新してください:"
        echo "   slack app update --manifest manifest.json"
        echo "2. または、Slack App管理画面で手動更新してください"
        echo ""
        
        # Ask if user wants to update the Slack app automatically
        read -p "Slack Appを自動更新しますか? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🔄 Slack Appを更新中..."
            if command -v slack &> /dev/null; then
                slack app update --manifest manifest.json
                if [ $? -eq 0 ]; then
                    echo "✅ Slack App updated successfully!"
                else
                    echo "❌ Failed to update Slack App. Please update manually."
                fi
            else
                echo "❌ slack CLI not found. Please install slack CLI or update manually."
            fi
        fi
    fi
    
    echo ""
    echo "📝 Next steps:"
    echo "1. Update your Slack app's Request URL to: ${SERVICE_URL}/slack/events"
    echo "2. Set environment variables for Slack tokens"
    echo "3. Configure Google Cloud credentials"
else
    echo "❌ Deployment failed"
    exit 1
fi