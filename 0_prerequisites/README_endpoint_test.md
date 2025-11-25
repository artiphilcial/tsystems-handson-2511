# watsonx.ai Endpoint Connectivity Test

This script tests basic network connectivity to watsonx.ai endpoints used in the workshop.

**No API keys required** - it simply checks if your network allows access to IBM Cloud and watsonx.ai services.

## What it tests

The script verifies access to these key endpoints:

1. **IBM Cloud IAM Token Endpoint** - Required for authentication
   - `https://iam.cloud.ibm.com/identity/token`

2. **watsonx.ai Foundation Models API** - Lists available models
   - `https://us-south.ml.cloud.ibm.com/ml/v1/foundation_model_specs`

3. **watsonx.ai Text Generation API** - Core inference endpoint
   - `https://us-south.ml.cloud.ibm.com/ml/v1/text/generation`

4. **watsonx.ai Deployments API** - Deployment management endpoint
   - `https://us-south.ml.cloud.ibm.com/ml/v1/deployments`

## How to run

### Prerequisites
- Python 3.8+
- `uv` package manager installed

### Steps

1. **Navigate to the prerequisites directory:**
   ```bash
   cd 0_prerequisites
   ```

2. **Run the test:**
   ```bash
   uv run test_wx_endpoints.py
   ```

   Or if you have the dependencies installed:
   ```bash
   python test_wx_endpoints.py
   ```

### Expected output

✅ **REACHABLE:** Endpoint is accessible (any HTTP response including 200, 401, 403, 405)
⚠️ **UNEXPECTED:** Endpoint responded with an unusual status code
❌ **TIMEOUT/CONNECTION ERROR:** Network cannot reach the endpoint

## Notes

- This test does **not** require API keys or credentials
- It only checks if your network can reach the endpoints
- Any HTTP response (including authentication errors) means the endpoint is reachable
- You'll configure your actual API credentials later in the workshop