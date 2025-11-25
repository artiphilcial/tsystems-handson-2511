#Sample Materials, provided under license.
#Licensed Materials - Property of IBM.
#© Copyright IBM Corp. 2024,2025. All Rights Reserved.
#US Government Users Restricted Rights - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

"""
RAG Service Module
Handles all interactions with watsonx.ai QnA RAG deployment endpoints
"""

import requests
import time
import base64
from typing import Tuple, List, Dict, Optional
from pydantic import BaseModel


class RAGDocument(BaseModel):
    """Model for RAG source documents"""
    page_content: str
    metadata: dict


class RAGMessage(BaseModel):
    """Model for RAG chat messages with enhanced features"""
    id: str
    role: str
    text: str
    documents: List[RAGDocument] = []
    show_documents: bool = False
    log_id: str = ''
    rating_options: int = 5


class RAGService:
    """Service class for interacting with watsonx.ai QnA RAG deployments"""
    
    def __init__(self, config: dict):
        """
        Initialize RAG service with configuration
        
        Args:
            config: Dictionary containing:
                - deployment_url: RAG deployment endpoint URL
                - env_type: 'saas' or 'on-prem'
                - iam_apikey: IAM API key (for SaaS)
                - username: CPD username (for on-prem)
                - cpd_apikey: CPD API key (for on-prem)
                - enable_expert: Enable expert recommendations
                - is_expert_sample: Flag for sample expert profiles
                - rating_options: Number of rating options (2-5)
        """
        self.deployment_url = config.get('deployment_url', '')
        self.env_type = config.get('env_type', 'saas')
        self.iam_apikey = config.get('iam_apikey', '')
        self.username = config.get('username', '')
        self.cpd_apikey = config.get('cpd_apikey', '')
        self.enable_expert = config.get('enable_expert', False)
        self.is_expert_sample = config.get('is_expert_sample', False)
        self.rating_options = config.get('rating_options', 5)
        
        # Determine RAG version from URL
        if "/ai_service?" in self.deployment_url:
            self.version = "2.0"
        else:
            self.version = "1.x"
        
        # Token caching
        self.access_token = ''
        self.token_expires = 0
    
    def get_token(self, force: bool = False) -> str:
        """
        Retrieve and cache IAM access token
        
        Args:
            force: Force token refresh even if not expired
            
        Returns:
            Access token string
        """
        now = time.time()
        
        if self.token_expires <= now or force:
            if self.env_type == "saas":
                if not self.iam_apikey or not self.deployment_url:
                    raise ValueError("Missing RAG credentials for watsonx.ai SaaS")
                
                # Get access token for watsonx.ai SaaS
                response = requests.post(
                    'https://iam.cloud.ibm.com/identity/token',
                    data={
                        'apikey': self.iam_apikey,
                        'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'
                    }
                )
                
                if response.status_code == 200:
                    resp = response.json()
                    if 'access_token' not in resp:
                        raise ValueError("Unexpected token format")
                    
                    self.access_token = resp['access_token']
                    # Calculate expiration time (subtract 5 minutes as precaution)
                    self.token_expires = (
                        now + resp.get('expires_in', resp.get('expiration', now))
                    ) - 300
                else:
                    raise ValueError(f"Token request failed with status {response.status_code}")
            
            elif self.env_type == "on-prem":
                if not self.username or not self.cpd_apikey or not self.deployment_url:
                    raise ValueError("Missing RAG credentials for watsonx.ai on-prem")
                
                # Get access token for watsonx.ai On Prem
                user_pass_string = f"{self.username}:{self.cpd_apikey}"
                self.access_token = base64.b64encode(user_pass_string.encode()).decode()
            else:
                raise ValueError("QNA_RAG_ENV_TYPE must be 'saas' or 'on-prem'")
        
        return self.access_token
    
    def _exec_request(self, payload: dict, url: str, ignore_errors: bool = False) -> Optional[requests.Response]:
        """
        Execute HTTP request to RAG endpoint
        
        Args:
            payload: Request payload
            url: Endpoint URL
            ignore_errors: Don't raise exceptions on errors
            
        Returns:
            Response object or None on error
        """
        # Prepare headers based on environment type
        if self.env_type == "on-prem":
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'ZenApiKey {self.get_token()}'
            }
        else:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.get_token()}'
            }
        
        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)
            
            if response.status_code != 200 and not ignore_errors:
                raise ValueError(f"Request failed with status code: {response.status_code}")
            
            return response
        except Exception as e:
            if not ignore_errors:
                raise ValueError(f"Request failed: {str(e)}")
            return None
    
    def ping(self) -> Tuple[bool, int]:
        """
        Health check for RAG endpoint
        
        Returns:
            Tuple of (success: bool, status_code: int)
        """
        if self.version == "1.x":
            payload = {"input_data": [{"fields": [""], "values": [[""]]}]}
        else:
            payload = {"": ""}
        
        response = self._exec_request(payload, self.deployment_url, ignore_errors=True)
        status_code = response.status_code if response else 0
        
        return status_code == 200, status_code
    
    def get_response(self, prompt: str) -> Tuple[str, List[dict], str]:
        """
        Generate response using RAG
        
        Args:
            prompt: User's question
            
        Returns:
            Tuple of (response_text, source_documents, log_id)
        """
        url = self.deployment_url
        
        if self.version == "1.x":
            payload = {
                "input_data": [{
                    "fields": ["Text"],
                    "values": [[prompt]]
                }]
            }
            response = self._exec_request(payload, url)
            
            if not response:
                return 'I am not able to reply due to a technical issue.', [], ''
            
            data = response.json()
            text = data['predictions'][0]['values'][0][0]['response']
            documents = data['predictions'][0]['values'][0][0].get('source_documents', [])
            log_id = data['predictions'][0]['values'][0][0].get('log_id', '')
        
        else:  # version 2.0
            url = url.replace("/ai_service?", "/ai_service/qna?")
            payload = {"question": prompt}
            response = self._exec_request(payload, url)
            
            if not response:
                return 'I am not able to reply due to a technical issue.', [], ''
            
            data = response.json()
            text = data['result']['response']
            documents = data['result'].get('source_documents', [])
            log_id = data['result'].get('log_id', '')
        
        return text, documents, log_id
    
    def send_feedback(self, log_id: str, value: str, comment: Optional[str] = None) -> dict:
        """
        Submit user feedback for a response
        
        Args:
            log_id: Log ID from the response
            value: Feedback value (0-100)
            comment: Optional feedback comment
            
        Returns:
            Dictionary with status and message
        """
        if not log_id:
            return {'status': 'error', 'message': 'No log_id provided'}
        
        url = self.deployment_url
        
        if self.version == "1.x":
            payload = {
                "input_data": [{
                    "fields": ["log_id", "value", "comment"],
                    "values": [[log_id, value, comment or '']]
                }]
            }
            response = self._exec_request(payload, url)
            
            if response and response.status_code == 200:
                result = response.json()['predictions'][0]['values'][0][0]
                return {
                    'status': 'ok' if result == 'ok' else 'error',
                    'message': 'Feedback submitted successfully' if result == 'ok' else 'Feedback submission failed'
                }
        
        else:  # version 2.0
            url = url.replace("/ai_service?", "/ai_service/log_feedback?")
            payload = {
                "log_id": log_id,
                "value": value,
                "comment": comment or ''
            }
            response = self._exec_request(payload, url)
            
            if response and response.status_code == 200:
                result = response.json()
                return {
                    'status': result.get('status', 'error'),
                    'message': 'Feedback submitted successfully' if result.get('status') == 'ok' else 'Feedback submission failed'
                }
        
        return {'status': 'error', 'message': 'Feedback submission failed'}
    
    def get_expert_recommendation(self, log_id: str) -> dict:
        """
        Get expert recommendation for a question
        
        Args:
            log_id: Log ID from the response
            
        Returns:
            Dictionary with expert details or error
        """
        if not log_id:
            return {'status': 'error', 'message': 'No log_id provided'}
        
        url = self.deployment_url
        
        if self.version == "1.x":
            payload = {
                "input_data": [{
                    "fields": ["_function", "log_id"],
                    "values": [["recommend_top_experts", log_id]]
                }]
            }
            response = self._exec_request(payload, url)
            
            if response and response.status_code == 200:
                data = response.json()
                experts = data['predictions'][0]['values'][0][0]
                status = data['predictions'][0]['values'][0][1]
                
                if 'expert_details' in status and len(experts) > 0:
                    return {
                        'status': 'ok',
                        'expert': experts[0],
                        'is_sample': self.is_expert_sample
                    }
        
        else:  # version 2.0
            url = url.replace("/ai_service?", "/ai_service/recommended_experts?")
            payload = {"log_id": log_id}
            response = self._exec_request(payload, url)
            
            if response and response.status_code == 200:
                data = response.json()
                
                if 'expert_details' in data.get('expert_status', '') and len(data.get('recommended_top_experts', [])) > 0:
                    return {
                        'status': 'ok',
                        'expert': data['recommended_top_experts'][0],
                        'is_sample': self.is_expert_sample
                    }
        
        return {'status': 'error', 'message': 'No experts found for this topic'}

