#!/bin/bash

# test_api.sh - Simple script to test the Iris API endpoints
# Usage: ./test_api.sh <API_URL>
# Example: ./test_api.sh http://35.188.110.134

API_URL=${1:-"http://localhost:8200"}

echo "🔍 Testing Iris API at: $API_URL"
echo "=================================="

# Test liveness probe
echo "1. Testing liveness probe..."
LIVENESS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/live_check)
if [ "$LIVENESS_RESPONSE" = "200" ]; then
    echo "   ✅ Liveness check: PASSED (HTTP $LIVENESS_RESPONSE)"
else
    echo "   ❌ Liveness check: FAILED (HTTP $LIVENESS_RESPONSE)"
fi

# Test readiness probe
echo "2. Testing readiness probe..."
READINESS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/ready_check)
if [ "$READINESS_RESPONSE" = "200" ]; then
    echo "   ✅ Readiness check: PASSED (HTTP $READINESS_RESPONSE)"
else
    echo "   ❌ Readiness check: FAILED (HTTP $READINESS_RESPONSE)"
fi

# Test welcome endpoint
echo "3. Testing welcome endpoint..."
WELCOME_RESPONSE=$(curl -s $API_URL/)
echo "   Response: $WELCOME_RESPONSE"

# Test prediction endpoint
echo "4. Testing prediction endpoint..."
PREDICTION_DATA='{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
echo "   Input: $PREDICTION_DATA"

PREDICTION_RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$PREDICTION_DATA" \
    $API_URL/predict/)

if [[ $PREDICTION_RESPONSE == *"predicted_class"* ]]; then
    echo "   ✅ Prediction: PASSED"
    echo "   Response: $PREDICTION_RESPONSE"
else
    echo "   ❌ Prediction: FAILED"
    echo "   Response: $PREDICTION_RESPONSE"
fi

echo ""
echo "🏁 Test completed!"

# Test with different sample data
echo ""
echo "5. Testing with different Iris samples..."

# Sample for each class
declare -a samples=(
    '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'  # Likely setosa
    '{"sepal_length": 7.0, "sepal_width": 3.2, "petal_length": 4.7, "petal_width": 1.4}'  # Likely versicolor  
    '{"sepal_length": 6.3, "sepal_width": 3.3, "petal_length": 6.0, "petal_width": 2.5}'  # Likely virginica
)

for i in "${!samples[@]}"; do
    sample="${samples[$i]}"
    echo "   Sample $((i+1)): $sample"
    
    response=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "$sample" \
        $API_URL/predict/)
    
    echo "   Prediction: $response"
    echo ""
done
