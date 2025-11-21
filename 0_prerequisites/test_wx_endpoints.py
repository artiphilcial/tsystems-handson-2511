#!/usr/bin/env python3
"""
watsonx.ai Endpoint Connectivity Test

This script tests basic network connectivity to watsonx.ai endpoints
to ensure workshop participants can access the required services.
No API keys required - just checks if endpoints are reachable.
"""

import sys
import requests

def test_endpoint(url, description, timeout=10):
    """Test if an endpoint is reachable (any response means it's accessible)"""
    print(f"Testing {description}...")
    print(f"  URL: {url}")
    
    try:
        # Use GET request for better compatibility
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        status_code = response.status_code
        
        # Any HTTP response means the endpoint is reachable
        # 200: Success, 400: Bad request (reachable), 401/403: Auth required (reachable)
        # 404: Not found (reachable), 405: Method not allowed (reachable)
        if status_code in [200, 400, 401, 403, 404, 405]:
            print(f"  ✅ REACHABLE - Status: {status_code}")
            return True
        else:
            print(f"  ⚠️  UNEXPECTED - Status: {status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"  ❌ TIMEOUT - Request timed out after {timeout}s")
        return False
    except requests.exceptions.ConnectionError:
        print(f"  ❌ CONNECTION ERROR - Cannot reach endpoint")
        return False
    except Exception as e:
        print(f"  ❌ ERROR - {str(e)}")
        return False

def main():
    """Run all endpoint tests"""
    print("=" * 60)
    print("watsonx.ai Endpoint Connectivity Test")
    print("=" * 60)
    print()
    print("Testing basic connectivity to IBM Cloud and watsonx.ai...")
    print("(No API keys required - just checking if endpoints are reachable)")
    print()
    
    # Test results
    results = []
    
    # 1. Test IBM Cloud IAM endpoint
    results.append(test_endpoint(
        "https://iam.cloud.ibm.com/identity/token",
        "IBM Cloud IAM Token Endpoint"
    ))
    print()
    
    # 2. Test watsonx.ai ML endpoint (default US South)
    watsonx_url = "https://us-south.ml.cloud.ibm.com"
    results.append(test_endpoint(
        f"{watsonx_url}/ml/v1/foundation_model_specs?version=2023-05-29",
        "watsonx.ai Foundation Models API"
    ))
    print()
    
    # 3. Test watsonx.ai text generation endpoint
    results.append(test_endpoint(
        f"{watsonx_url}/ml/v1/text/generation?version=2023-05-29",
        "watsonx.ai Text Generation API"
    ))
    print()
    
    # 4. Test watsonx.ai deployments endpoint
    results.append(test_endpoint(
        f"{watsonx_url}/ml/v1/deployments?version=2021-05-01",
        "watsonx.ai Deployments API"
    ))
    print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    successful_tests = sum(results)
    total_tests = len(results)
    
    if successful_tests == total_tests:
        print(f"🎉 ALL TESTS PASSED ({successful_tests}/{total_tests})")
        print("✅ Your network allows access to watsonx.ai endpoints")
        print("✅ You're ready for the workshop!")
    elif successful_tests > 0:
        print(f"⚠️  PARTIAL SUCCESS ({successful_tests}/{total_tests})")
        print("🔍 Some endpoints are reachable, but others failed")
        print("⚠️  Check the failed tests above")
    else:
        print(f"❌ ALL TESTS FAILED (0/{total_tests})")
        print("🚫 Your network may be blocking watsonx.ai endpoints")
    
    print()
    print("Next steps:")
    if successful_tests < total_tests:
        print("- Check your network/firewall settings")
        print("- Contact your network administrator if needed")
        print("- Try from a different network (e.g., mobile hotspot)")
    else:
        print("- Proceed with the workshop setup")
        print("- Make sure to configure your .env file with API credentials")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Made with Bob
