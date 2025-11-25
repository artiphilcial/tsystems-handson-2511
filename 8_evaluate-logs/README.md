# Log Analysis with AI - Hands-on Workshop

## Overview

This section of the workshop demonstrates how to leverage Large Language Models (LLMs) to analyze system logs, identify issues, and generate actionable debugging steps. We'll explore two scenarios of increasing complexity that are relevant to telecommunications operations at T-Systems.

## Using the Log Analysis Assistant

For this section of the workshop, we'll use the **Log Analysis Assistant** prompt template available in the [Chat with your models](../2_chat-with-your-models/README.md) application.

### Getting Started

1. Navigate to the chat application: `cd 2_chat-with-your-models`
2. Run the application: `uv run streamlit run app/frontend/app.py`
3. In the sidebar, select **"Log Analysis Assistant"** from the prompt template dropdown
4. The assistant is pre-configured to analyze system logs, identify issues, trace cascading failures, and provide debugging recommendations

## Workshop Structure

### 📋 Scenario 1: Simple - Customer Portal Authentication Issues

**Background:** The T-Systems customer portal is experiencing authentication issues, slow response times, and database connection problems.

**Location:** `simple-scenario/`
- Contains `customer-portal.log` with traditional syslog format
- **Prompt Templates**: `analysis-prompts.md` - Ready-to-use prompts for LLM analysis
- **Quality Cheat Sheet**: `expected-outcomes.md` - Validation criteria and examples ⭐

**What you'll learn:**
- Analyzing single application logs
- Identifying authentication failures and account lockouts
- Diagnosing database connection pool exhaustion
- Providing immediate remediation steps

### 🏗️ Scenario 2: Complex - Microservices Billing System

**Background:** A microservices-based billing platform experiencing cascading failures across API Gateway, Billing Service, and Database.

**Location:** `complex-scenario/`
- Contains three log files: `api-gateway.log`, `billing-service.log`, `database.log`
- **Prompt Templates**: `analysis-prompts.md` - Advanced multi-service analysis prompts
- **Quality Cheat Sheet**: `expected-outcomes.md` - Comprehensive validation guide ⭐

**What you'll learn:**
- Correlating logs across multiple services
- Tracing requests using request IDs
- Understanding cascading failure patterns
- Evaluating resilience patterns (circuit breakers, timeouts)
- Providing architectural improvements
