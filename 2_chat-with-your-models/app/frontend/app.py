import streamlit as st
import os
import uuid
import requests
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import Credentials
from dotenv import load_dotenv

# Import RAG service
try:
    from rag_service import RAGService, RAGMessage, RAGDocument
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("Warning: RAG service not available. Install pydantic and requests.")


load_dotenv()

# DTAG Colors
DT_MAGENTA = "#E20074"

# Page Config
st.set_page_config(
    page_title="watsonx AI Chat", 
    page_icon="💬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# custom CSS with dark mode support
st.markdown(f"""
    <style>
    /* Remove forced white background to respect theme */
    .stApp {{
        background-color: transparent;
    }}
    
    /* Dark mode specific styles */
    [data-testid="stAppViewContainer"] {{
        background-color: var(--background-color);
    }}
    
    /* Ensure chat messages are readable in dark mode */
    [data-testid="stChatMessageContent"] {{
        color: var(--text-color);
    }}
    
    /* Style headings */
    h1 {{
        color: {DT_MAGENTA};
    }}
    
    /* Button styling */
    .stButton>button {{
        background-color: {DT_MAGENTA};
        color: white;
    }}
    .stButton>button:hover {{
        background-color: #C40063;
    }}
    
    /* Ensure info boxes are readable in dark mode */
    .stAlert {{
        color: var(--text-color);
    }}
    
    /* Source documents table styling */
    .source-docs-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }}
    .source-docs-table th {{
        background-color: {DT_MAGENTA};
        color: white;
        padding: 10px;
        text-align: left;
    }}
    .source-docs-table td {{
        padding: 10px;
        border: 1px solid #ddd;
    }}
    </style>
""", unsafe_allow_html=True)


def initialize_rag_service():
    """Initialize RAG service with configuration from environment"""
    if not RAG_AVAILABLE:
        return None
    
    try:
        config = {
            'deployment_url': os.getenv('QNA_RAG_DEPLOYMENT_URL', ''),
            'env_type': os.getenv('QNA_RAG_ENV_TYPE', 'saas'),
            'iam_apikey': os.getenv('QNA_RAG_SAAS_IAM_APIKEY', ''),
            'username': os.getenv('QNA_RAG_ONPREM_CPD_USERNAME', ''),
            'cpd_apikey': os.getenv('QNA_RAG_ONPREM_CPD_APIKEY', ''),
            'enable_expert': os.getenv('ENABLE_EXPERT_RECOMMENDATION', 'False') == 'True',
            'is_expert_sample': os.getenv('IS_EXPERT_SAMPLE', 'False') == 'True',
            'rating_options': int(os.getenv('FEEDBACK_RATING_OPTIONS', '5'))
        }
        
        if not config['deployment_url']:
            return None
            
        return RAGService(config)
    except Exception as e:
        st.error(f"Failed to initialize RAG service: {str(e)}")
        return None


def display_rag_message(msg: RAGMessage):
    """Display a RAG message with documents and feedback options"""
    with st.chat_message(msg.role):
        st.markdown(msg.text)
        
        # Show source documents if toggled
        if msg.show_documents and msg.documents:
            st.markdown("### 📚 Source Documents")
            for i, doc in enumerate(msg.documents, 1):
                with st.expander(f"Document {i}: {doc.metadata.get('title', 'Unknown')}"):
                    st.markdown(f"**Source:** [{doc.metadata.get('title', 'Unknown')}]({doc.metadata.get('document_url', '#')})")
                    st.markdown(f"**Content:**\n\n{doc.page_content}")
        
        # Show document toggle button
        if msg.documents and msg.role == 'assistant':
            if st.button(
                ('Hide' if msg.show_documents else 'Show') + ' source documents',
                key=f'toggle_docs_{msg.id}'
            ):
                msg.show_documents = not msg.show_documents
                st.rerun()
        
        # Show feedback buttons for assistant messages with log_id
        if msg.log_id and msg.role == 'assistant':
            render_feedback_buttons(msg)


def render_feedback_buttons(msg: RAGMessage):
    """Render feedback rating buttons"""
    st.markdown("**Rate this response:**")
    
    # Check if this message is awaiting feedback comment
    awaiting_comment = st.session_state.get('awaiting_feedback_comment', {}).get(msg.id, False)
    
    if not awaiting_comment:
        # Show rating buttons
        cols = st.columns(msg.rating_options)
        
        # Define emoji options based on rating_options
        if msg.rating_options == 2:
            emojis = ['👎', '👍']
        elif msg.rating_options == 3:
            emojis = ['😠', '😐', '😀']
        elif msg.rating_options == 4:
            emojis = ['😠', '🙁', '🙂', '😀']
        else:  # 5 options
            emojis = ['😡', '😠', '🙁', '😐', '🙂']
        
        for i, emoji in enumerate(emojis):
            value = round(100 * (i / (msg.rating_options - 1)))
            if cols[i].button(emoji, key=f'feedback_{msg.id}_{i}'):
                handle_feedback(msg.id, msg.log_id, str(value))


def handle_feedback(msg_id: str, log_id: str, value: str):
    """Handle feedback submission"""
    feedback_value = int(value)
    
    if feedback_value < 100:
        # Request comment for negative feedback
        st.session_state.awaiting_feedback_comment = {msg_id: True}
        st.session_state.pending_feedback = {
            'msg_id': msg_id,
            'log_id': log_id,
            'value': value
        }
        st.rerun()
    else:
        # Submit positive feedback immediately
        submit_feedback(log_id, value, None)


def submit_feedback(log_id: str, value: str, comment: str = None):
    """Submit feedback to RAG service"""
    if 'rag_service' not in st.session_state or not st.session_state.rag_service:
        st.error("RAG service not available")
        return
    
    try:
        result = st.session_state.rag_service.send_feedback(log_id, value, comment)
        
        if result['status'] == 'ok':
            feedback_value = int(value)
            
            if feedback_value < 100:
                # Show expert recommendation button for negative feedback
                response_text = f"Thanks for your feedback! {result['message']}"
                
                if st.session_state.rag_service.enable_expert:
                    response_text += "\n\nWould you like to see an expert recommendation for this question?"
                    
                    new_msg = RAGMessage(
                        id=str(uuid.uuid4()),
                        role='assistant',
                        text=response_text
                    )
                    st.session_state.rag_messages.append(new_msg)
                    
                    # Store log_id for expert recommendation
                    st.session_state.expert_log_id = log_id
                    st.session_state.show_expert_button = True
            else:
                # Positive feedback
                new_msg = RAGMessage(
                    id=str(uuid.uuid4()),
                    role='assistant',
                    text=f"Thanks for your positive feedback! {result['message']}\n\nFeel free to ask another question."
                )
                st.session_state.rag_messages.append(new_msg)
        else:
            st.error(f"Feedback submission failed: {result.get('message', 'Unknown error')}")
    
    except Exception as e:
        st.error(f"Error submitting feedback: {str(e)}")
    
    # Clear pending feedback
    st.session_state.awaiting_feedback_comment = {}
    st.session_state.pending_feedback = {}
    st.rerun()


def get_expert_recommendation():
    """Get and display expert recommendation"""
    if 'rag_service' not in st.session_state or not st.session_state.rag_service:
        st.error("RAG service not available")
        return
    
    log_id = st.session_state.get('expert_log_id', '')
    if not log_id:
        st.error("No log ID available for expert recommendation")
        return
    
    try:
        result = st.session_state.rag_service.get_expert_recommendation(log_id)
        
        if result['status'] == 'ok':
            expert = result['expert']
            is_sample = result.get('is_sample', False)
            
            expert_text = ""
            if is_sample:
                expert_text = "**Note:** This is a synthetic expert profile generated using watsonx.ai.\n\n"
            
            expert_text += "### 👤 Recommended Expert\n\n"
            expert_text += f"**Name:** {expert.get('name', 'N/A')}\n\n"
            expert_text += f"**Email:** {expert.get('email', 'N/A')}\n\n"
            expert_text += f"**Position:** {expert.get('position', 'N/A')}\n\n"
            expert_text += f"**Domain:** {expert.get('domain', 'N/A')}\n\n"
            expert_text += "Feel free to contact this expert for more detailed information."
            
            new_msg = RAGMessage(
                id=str(uuid.uuid4()),
                role='assistant',
                text=expert_text
            )
            st.session_state.rag_messages.append(new_msg)
        else:
            new_msg = RAGMessage(
                id=str(uuid.uuid4()),
                role='assistant',
                text=f"No experts found for this topic. {result.get('message', '')}\n\nPlease ask another question."
            )
            st.session_state.rag_messages.append(new_msg)
    
    except Exception as e:
        st.error(f"Error getting expert recommendation: {str(e)}")
    
    # Clear expert button state
    st.session_state.show_expert_button = False
    st.session_state.expert_log_id = ''
    st.rerun()


# sidebar
with st.sidebar:
    # Deutsche Telekom Logo Header
    st.markdown(
    """
    <div style='text-align: center; padding: 1px;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/d/dd/Deutsche_Telekom_2022.svg'
             alt='Deutsche Telekom Logo'
             style='width: 50px; max-width: 20%; height: auto;'>
    </div>
    """,
    unsafe_allow_html=True
)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"### <span style='color:{DT_MAGENTA}'>Configuration</span>", unsafe_allow_html=True)
    
    # Show credentials status
    project_id = os.getenv("WATSONX_PROJECT_ID", "")
    api_key = os.getenv("WATSONX_API_KEY", "")
    
    missing = []
    if not project_id:
        missing.append("WATSONX_PROJECT_ID")
    if not api_key:
        missing.append("WATSONX_API_KEY")
    
    if missing:
        st.error(f"⚠️ Missing in .env: {', '.join(missing)}")
    else:
        st.success("✓ Credentials loaded")
    
    # Check for template deployments
    template_deployments = {
        "Customer Service": os.getenv("CUSTOMER_SERVICE_DEPLOYMENT_ID", ""),
        "Claims Expert": os.getenv("CLAIMS_EXPERT_DEPLOYMENT_ID", ""),
        "Log Analysis Assistant": os.getenv("LOG_ANALYSIS_DEPLOYMENT_ID", "")
    }
    
    deployed_templates = [name for name, dep_id in template_deployments.items() if dep_id]
    if deployed_templates:
        st.info(f"🚀 Deployed templates: {', '.join(deployed_templates)}")
    
    # RAG Toggle
    use_rag = st.toggle("Use RAG", value=os.getenv("USE_RAG", "False") == "True")
    
    # Initialize RAG service if enabled
    if use_rag and RAG_AVAILABLE:
        if 'rag_service' not in st.session_state or st.session_state.rag_service is None:
            with st.spinner("Initializing RAG service..."):
                st.session_state.rag_service = initialize_rag_service()
                
                # Check connection only once during initialization
                if st.session_state.rag_service:
                    with st.spinner("Checking RAG connection..."):
                        ok, status_code = st.session_state.rag_service.ping()
                        st.session_state.rag_connection_ok = ok
                        st.session_state.rag_connection_status = status_code
                else:
                    st.session_state.rag_connection_ok = False
                    st.session_state.rag_connection_status = 0
        
        # Display connection status from cached result
        if st.session_state.rag_service:
            if st.session_state.get('rag_connection_ok', False):
                st.success(f"✓ RAG endpoint connected (v{st.session_state.rag_service.version})")
            else:
                st.error(f"✗ RAG connection failed (status: {st.session_state.get('rag_connection_status', 0)})")
        else:
            st.error("✗ RAG service initialization failed")
            st.info("Check your RAG configuration in .env file")
    elif use_rag and not RAG_AVAILABLE:
        st.error("✗ RAG dependencies not installed")
        st.info("Install: pip install pydantic requests")
    
    # Show appropriate configuration based on mode
    if not use_rag:
        # Define template deployments mapping
        template_deployments = {
            "Customer Service": os.getenv("CUSTOMER_SERVICE_DEPLOYMENT_ID", ""),
            "Claims Expert": os.getenv("CLAIMS_EXPERT_DEPLOYMENT_ID", ""),
            "Log Analysis Assistant": os.getenv("LOG_ANALYSIS_DEPLOYMENT_ID", "")
        }
        
        # Normal mode configuration
        st.markdown("**Prompt Template**")
        
        prompt_templates = {
            "Customer Service": {
                "system": "You are a helpful customer service assistant for Deutsche Telekom. Answer the customer's question directly and concisely. Be friendly and professional. Only respond as the assistant - do not generate the customer's side of the conversation.",
                "greeting": "Hello! I'm here to help with any questions or issues you may have regarding Deutsche Telekom's products and services, such as your mobile or internet plans, billing, or technical support. How can I assist you today?"
            },
            "Claims Expert": {
                "system": "You are a claims expert for Versi insurance services. Help customers file and process insurance claims by gathering necessary information about accidents, damages, and incidents. Ask clarifying questions to collect complete details including date, time, location, description of incident, damages, injuries, and supporting documentation. Be empathetic and professional. Only respond as the claims expert - do not continue the conversation on behalf of the customer.",
                "greeting": "Hello! I'm your Deutsche Telekom Claims Expert. I'm here to assist you with filing and processing your insurance claim. Please provide details about your incident, including the date, time, location, what happened, any damages or injuries, and any written documentation. How can I help you with your claim today?"
            },
            "Log Analysis Assistant": {
                "system": "You are a log analysis expert for T-Systems telecommunications operations. Analyze system logs from customer portals, billing systems, and microservices architectures. Identify issues, determine root causes, assess severity and impact, provide timelines of events, and suggest specific debugging steps and fixes. You can analyze both traditional syslog format and structured JSON logs. Correlate events across multiple services using request IDs and timestamps. Evaluate resilience patterns like circuit breakers and timeouts. Only provide your analysis - do not simulate the user's questions.",
                "greeting": "Hello! I'm your T-Systems Log Analysis Assistant. I can help you analyze system logs from customer portals, billing systems, and microservices. I'll identify issues, trace cascading failures, determine root causes, and provide actionable debugging steps. Please paste your log files or describe the system issue you're investigating."
            },
            "Custom": {
                "system": "custom",
                "greeting": ""
            }
        }
        
        selected_template = st.selectbox(
            "Select Template",
            options=list(prompt_templates.keys()),
            index=0  # Default to Customer Service (first option)
        )
        
        # Check if selected template has a deployment
        current_deployment_id = template_deployments.get(selected_template, "")
        
        if current_deployment_id:
            # Show deployment info
            st.success(f"🚀 Using deployed template")
            st.text_input("Deployment ID", value=current_deployment_id, disabled=True, key="deployment_display")
            prompt_prefix = ""
            initial_greeting = ""
            model_id = None  # Not used in deployment mode
        else:
            # Use local template configuration
            if selected_template == "Custom":
                prompt_prefix = st.text_area("Custom Prompt Template", value="")
                initial_greeting = ""
            else:
                prompt_prefix = prompt_templates[selected_template]["system"]
                initial_greeting = prompt_templates[selected_template]["greeting"]
            
            # model Selection with shortened display names
            model_options = {
                'Granite 3.3 8B': 'ibm/granite-3-3-8b-instruct',
                'Granite 8B Code': 'ibm/granite-8b-code-instruct',
                'Llama 3.2 90B Vision': 'meta-llama/llama-3-2-90b-vision-instruct',
                'Llama 3.3 70B': 'meta-llama/llama-3-3-70b-instruct',
                'Llama 3 405B': 'meta-llama/llama-3-405b-instruct',
                'Llama 4 Maverick 17B': 'meta-llama/llama-4-maverick-17b-128e-instruct-fp8',
                'Mistral Medium': 'mistralai/mistral-medium-2505',
                'Mistral Small 24B': 'mistralai/mistral-small-3-1-24b-instruct-2503',
                'GPT OSS 120B': 'openai/gpt-oss-120b'
            }
            
            selected_model_name = st.selectbox(
                "Model",
                options=list(model_options.keys()),
                index=7  # Default to Mistral Small 24B
            )
            
            model_id = model_options[selected_model_name]
    else:
        # RAG mode - no template/model selection needed
        st.info("📚 RAG Mode Active\n\nQuestions will be answered using your document knowledge base.")
    
    if st.button("Clear Chat"):
        if use_rag:
            st.session_state.rag_messages = []
            st.session_state.awaiting_feedback_comment = {}
            st.session_state.pending_feedback = {}
            st.session_state.show_expert_button = False
        else:
            st.session_state.messages = []
        st.rerun()

# main Title
st.markdown(f"<h1 style='color:{DT_MAGENTA}'>watsonx.ai Chat</h1>", unsafe_allow_html=True)

# Show mode indicator
if use_rag:
    st.info("📚 **RAG Mode**: Chatting with your document knowledge base")
else:
    # Check if current template has deployment
    if 'selected_template' in locals() and 'template_deployments' in locals():
        current_deployment_id = template_deployments.get(selected_template, "")
        if current_deployment_id:
            st.info(f"🚀 **Deployment Mode**: {selected_template} (deployed)")
        elif 'prompt_prefix' in locals() and prompt_prefix:
            st.info(f"📝 **Direct Mode**: {selected_template}")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_messages" not in st.session_state:
    st.session_state.rag_messages = []

if "current_template" not in st.session_state:
    st.session_state.current_template = None

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "normal"

if "awaiting_feedback_comment" not in st.session_state:
    st.session_state.awaiting_feedback_comment = {}

if "pending_feedback" not in st.session_state:
    st.session_state.pending_feedback = {}

if "show_expert_button" not in st.session_state:
    st.session_state.show_expert_button = False

if "expert_log_id" not in st.session_state:
    st.session_state.expert_log_id = ''

if "rag_connection_ok" not in st.session_state:
    st.session_state.rag_connection_ok = False

if "rag_connection_status" not in st.session_state:
    st.session_state.rag_connection_status = 0

# Handle mode switching
current_mode = "rag" if use_rag else "normal"
if st.session_state.current_mode != current_mode:
    st.session_state.current_mode = current_mode
    # Mode changed - clear temporary states
    st.session_state.awaiting_feedback_comment = {}
    st.session_state.pending_feedback = {}
    st.session_state.show_expert_button = False
    
    # If switching away from RAG, clear the service (will reinitialize if switched back)
    if not use_rag and 'rag_service' in st.session_state:
        st.session_state.rag_service = None
        st.session_state.rag_connection_ok = False
        st.session_state.rag_connection_status = 0

# Check if template changed in normal mode
if not use_rag:
    if st.session_state.current_template != selected_template:
        st.session_state.current_template = selected_template
        st.session_state.messages = []
        if initial_greeting:
            st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# Initialize RAG messages with greeting if empty
if use_rag and not st.session_state.rag_messages:
    greeting_msg = RAGMessage(
        id=str(uuid.uuid4()),
        role='assistant',
        text="Hi there! I am a QnA chatbot with access to your document knowledge base. Please ask me a question!"
    )
    st.session_state.rag_messages.append(greeting_msg)

# Display messages based on mode
if use_rag:
    # Display RAG messages
    for msg in st.session_state.rag_messages:
        display_rag_message(msg)
    
    # Show expert recommendation button if needed
    if st.session_state.show_expert_button:
        if st.button("🎓 Get Expert Recommendation", key="expert_rec_button"):
            get_expert_recommendation()
else:
    # Display normal messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle chat input
if prompt := st.chat_input("Type your message here..."):
    # Check if awaiting feedback comment
    if st.session_state.awaiting_feedback_comment:
        # This is a feedback comment
        pending = st.session_state.pending_feedback
        if pending:
            submit_feedback(pending['log_id'], pending['value'], prompt)
    elif use_rag:
        # RAG mode
        if not st.session_state.get('rag_service'):
            st.error("❌ RAG service not initialized. Please check your configuration.")
        else:
            # Add user message
            user_msg = RAGMessage(
                id=str(uuid.uuid4()),
                role='user',
                text=prompt
            )
            st.session_state.rag_messages.append(user_msg)
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get RAG response
            with st.chat_message("assistant"):
                with st.spinner("Searching knowledge base..."):
                    try:
                        text, documents, log_id = st.session_state.rag_service.get_response(prompt)
                        
                        # Convert documents to RAGDocument objects
                        rag_docs = [
                            RAGDocument(
                                page_content=doc.get('page_content', ''),
                                metadata=doc.get('metadata', {})
                            )
                            for doc in documents
                        ]
                        
                        assistant_msg = RAGMessage(
                            id=str(uuid.uuid4()),
                            role='assistant',
                            text=text,
                            documents=rag_docs,
                            log_id=log_id,
                            rating_options=st.session_state.rag_service.rating_options
                        )
                        
                        st.session_state.rag_messages.append(assistant_msg)
                        st.markdown(text)
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        error_msg_obj = RAGMessage(
                            id=str(uuid.uuid4()),
                            role='assistant',
                            text=error_msg
                        )
                        st.session_state.rag_messages.append(error_msg_obj)
            
            st.rerun()
    else:
        # Normal mode
        project_id = os.getenv("WATSONX_PROJECT_ID")
        api_key = os.getenv("WATSONX_API_KEY")
        
        if not project_id or not api_key:
            st.error("❌ Please configure WATSONX_PROJECT_ID and WATSONX_API_KEY in your .env file")
        else:
            # add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        # setup wx credentials
                        credentials = Credentials(
                            url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
                            api_key=api_key
                        )
                        
                        # Check if current template has a deployment
                        template_deployments = {
                            "Customer Service": os.getenv("CUSTOMER_SERVICE_DEPLOYMENT_ID", ""),
                            "Claims Expert": os.getenv("CLAIMS_EXPERT_DEPLOYMENT_ID", ""),
                            "Log Analysis Assistant": os.getenv("LOG_ANALYSIS_DEPLOYMENT_ID", "")
                        }
                        
                        current_template = st.session_state.get('current_template', '')
                        deployment_id = template_deployments.get(current_template, "")
                        
                        if deployment_id:
                            # Deployment mode - use deployed prompt template via direct API call
                            # The deployed template only expects 'input' variable
                            prompt_variables = {
                                "input": prompt
                            }
                            
                            # Get IAM token
                            token_response = requests.post(
                                'https://iam.cloud.ibm.com/identity/token',
                                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                data={
                                    'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
                                    'apikey': api_key
                                }
                            )
                            
                            if token_response.status_code != 200:
                                raise Exception(f"Failed to get IAM token: {token_response.text}")
                            
                            iam_token = token_response.json()['access_token']
                            
                            # Call the v1 text generation endpoint directly
                            deployment_url = f"{credentials.url}/ml/v1/deployments/{deployment_id}/text/generation?version=2021-05-01"
                            
                            generation_response = requests.post(
                                deployment_url,
                                headers={
                                    'Content-Type': 'application/json',
                                    'Accept': 'application/json',
                                    'Authorization': f'Bearer {iam_token}'
                                },
                                json={
                                    "parameters": {
                                        "prompt_variables": prompt_variables
                                    }
                                }
                            )
                            
                            if generation_response.status_code != 200:
                                raise Exception(f"Deployment request failed: {generation_response.text}")
                            
                            response = generation_response.json()['results'][0]['generated_text']
                        else:
                            # Direct model inference mode
                            # model parameters with stop sequences to prevent continuing conversation
                            parameters = {
                                GenParams.MAX_NEW_TOKENS: 4000,
                                GenParams.TEMPERATURE: 0.7,
                                GenParams.TOP_P: 1,
                                GenParams.TOP_K: 50,
                                GenParams.STOP_SEQUENCES: ["<|user|>", "<|system|>", "\n\nUser:", "\nUser:", "\n\nHuman:", "\nHuman:"]
                            }
                            
                            # Build conversation with proper structure to prevent model from continuing user's message
                            conversation_parts = []
                            
                            # Add system instruction if template is selected
                            if 'prompt_prefix' in locals() and prompt_prefix:
                                conversation_parts.append(f"<|system|>\n{prompt_prefix.strip()}")
                            
                            # Add conversation history with clear role separation
                            for msg in st.session_state.messages[:-1]:  # Exclude current message
                                if msg['role'] == 'user':
                                    conversation_parts.append(f"<|user|>\n{msg['content']}")
                                else:
                                    conversation_parts.append(f"<|assistant|>\n{msg['content']}")
                            
                            # Add current user message and prompt for assistant response
                            conversation_parts.append(f"<|user|>\n{prompt}")
                            conversation_parts.append("<|assistant|>")
                            
                            # Build the full prompt with clear structure
                            full_prompt = "\n\n".join(conversation_parts)
                            
                            # initialize model
                            model = ModelInference(
                                model_id=model_id if 'model_id' in locals() else 'ibm/granite-3-3-8b-instruct',
                                params=parameters,
                                credentials=credentials,
                                project_id=project_id
                            )
                            
                            # generate response
                            response = model.generate_text(prompt=full_prompt)
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        error_msg = f"❌ Error: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})

