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

## What the results mean

- **All tests pass:** Your network allows access to watsonx.ai - you're ready for the workshop! ✅
- **Partial success:** Some endpoints work, others may be blocked - check with your network admin ⚠️
- **All tests fail:** Your network is likely blocking watsonx.ai endpoints - contact IT support ❌

## Troubleshooting

### Common issues:

1. **Connection timeouts:** Corporate firewall may be blocking external APIs
2. **SSL/TLS errors:** Proxy or security software interference
3. **DNS resolution fails:** Network DNS configuration issues

### Solutions:

- Check with your network administrator about accessing IBM Cloud endpoints
- Try running from a different network (mobile hotspot) to isolate network issues
- Contact workshop organizers if you continue having connectivity issues

## Notes

- This test does **not** require API keys or credentials
- It only checks if your network can reach the endpoints
- Any HTTP response (including authentication errors) means the endpoint is reachable
- You'll configure your actual API credentials later in the workshop