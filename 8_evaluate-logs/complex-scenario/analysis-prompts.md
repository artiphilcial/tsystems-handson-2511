# Complex Scenario - LLM Analysis Prompts

> 📋 **Quick Reference**: See [expected-outcomes.md](./expected-outcomes.md) for detailed quality criteria, validation checklist, and example outputs.

## Prompt Templates for Microservices Billing System Analysis

### 🎯 Prompt 1: Multi-Service Correlation Analysis

```
I have logs from a microservices-based billing system experiencing a cascading failure. 
The system consists of:
- API Gateway (routes requests, implements circuit breakers)
- Billing Service (business logic, payment processing)
- PostgreSQL Database (data persistence with replication)

Please analyze these logs and:

1. Trace the cascading failure across all services
2. Identify the root cause and triggering event
3. Explain how the failure propagated through the system
4. Correlate events using request_ids and timestamps
5. Assess the effectiveness of resilience patterns (circuit breakers, timeouts)
6. Provide a detailed incident timeline
7. Recommend specific fixes for each service

API Gateway Logs:
[PASTE api-gateway.log CONTENTS]

Billing Service Logs:
[PASTE billing-service.log CONTENTS]

Database Logs:
[PASTE database.log CONTENTS]
```

**Expected Output:** Cross-service correlation, root cause, cascading failure diagram, timeline, service recommendations. [See details →](./expected-outcomes.md#-prompt-1-multi-service-correlation-analysis)

---

### 🔗 Prompt 2: Request Tracing

```
Please trace the following request IDs through all three services and provide:

1. Complete journey of each request
2. Timing at each service hop
3. Where each request succeeded or failed
4. What should have happened vs. what actually happened
5. Bottlenecks and delays identified

Request IDs to trace:
- req-i9j0k1l2 (payment request that failed)
- req-e5f6g7h8 (customer profile timeout)
- req-u1v2w3x4 (successful billing history request)

API Gateway Logs:
[PASTE api-gateway.log CONTENTS]

Billing Service Logs:
[PASTE billing-service.log CONTENTS]

Database Logs:
[PASTE database.log CONTENTS]
```

**Expected Output:** Request flow diagrams, timing breakdown, failure points, performance comparison. [See details →](./expected-outcomes.md#-prompt-2-request-tracing)

---

### 💾 Prompt 3: Database Performance Deep Dive

```
Analyze the database performance issues in detail:

1. What queries are causing problems?
2. Why is the UPDATE query taking 8.9 seconds?
3. What indexes are missing?
4. Analyze the deadlock that occurred
5. Explain the connection pool exhaustion
6. Provide specific CREATE INDEX statements
7. Recommend connection pool configuration changes
8. Suggest query optimization strategies

Database Logs:
[PASTE database.log CONTENTS]

Billing Service Logs (for context):
[PASTE billing-service.log CONTENTS]
```

**Expected Output:** Query analysis, index recommendations with SQL, deadlock explanation, pool tuning. [See details →](./expected-outcomes.md#-prompt-3-database-performance-deep-dive)

---

### 🔄 Prompt 4: Circuit Breaker Analysis

```
Evaluate the circuit breaker implementation:

1. When did the circuit breaker open and why?
2. Was the threshold appropriate (5 failures)?
3. How long was it open?
4. Did the half-open state work correctly?
5. When did it close and why?
6. What requests were rejected during the open state?
7. Recommend circuit breaker configuration improvements
8. Should we add circuit breakers elsewhere?

API Gateway Logs:
[PASTE api-gateway.log CONTENTS]

Billing Service Logs:
[PASTE billing-service.log CONTENTS]
```

**Expected Output:** Circuit breaker timeline, configuration evaluation, effectiveness assessment. [See details →](./expected-outcomes.md#-prompt-4-circuit-breaker-analysis)

---

### ⚡ Prompt 5: Performance Bottleneck Identification

```
Identify all performance bottlenecks in the system:

1. What are the slowest operations?
2. Where are the timeout thresholds being hit?
3. What's causing the replication lag?
4. Why are queries taking so long?
5. Is the connection pool sized correctly?
6. Are there any resource constraints?
7. Provide specific performance optimization recommendations

Include all three log files:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Bottleneck inventory, performance metrics, resource analysis, optimization roadmap. [See details →](./expected-outcomes.md#-prompt-5-performance-bottleneck-identification)

---

### 🏗️ Prompt 6: Architecture Review

```
Based on these logs, review the system architecture:

1. What architectural patterns are working well?
2. What patterns are failing or inadequate?
3. Are the service boundaries appropriate?
4. Is the database architecture suitable for the load?
5. Should we implement caching? Where?
6. Should we add message queues?
7. Recommend architectural improvements
8. Provide a revised architecture diagram description

Logs from all services:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Architecture assessment, pattern evaluation, improvements, diagram description. [See details →](./expected-outcomes.md#-prompt-6-architecture-review)

---

### 📊 Prompt 7: Capacity Planning

```
Analyze these logs for capacity planning insights:

1. What is the current load on each service?
2. What are the resource utilization patterns?
3. When did we hit capacity limits?
4. What are the growth trends?
5. Calculate required capacity for 2x, 5x, 10x load
6. Recommend scaling strategies
7. Identify single points of failure
8. Suggest auto-scaling policies

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Capacity metrics, growth projections, scaling recommendations, auto-scaling policies. [See details →](./expected-outcomes.md#-prompt-7-capacity-planning)

---

### 🛡️ Prompt 8: Resilience Pattern Evaluation

```
Evaluate all resilience patterns in the system:

1. Timeouts: Are they configured correctly?
2. Circuit Breakers: Working as intended?
3. Retry Logic: Is it present? Should it be?
4. Bulkheads: Are failures isolated?
5. Graceful Degradation: Is it implemented?
6. Health Checks: Are they effective?
7. Rate Limiting: Working correctly?
8. Recommend additional resilience patterns

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Pattern evaluation, effectiveness scores, gap analysis, implementation recommendations. [See details →](./expected-outcomes.md#-prompt-8-resilience-pattern-evaluation)

---

### 🔍 Prompt 9: Observability Assessment

```
Assess the observability of this system:

1. Is the logging sufficient?
2. Are request IDs consistently used?
3. What metrics are missing?
4. What additional log fields would help?
5. Recommend distributed tracing implementation
6. Suggest log aggregation strategy
7. Design monitoring dashboards
8. Create alert rules

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Logging assessment, missing metrics, tracing recommendations, dashboards, alerts. [See details →](./expected-outcomes.md#-prompt-9-observability-assessment)

---

### 🚨 Prompt 10: Incident Response Playbook

```
Create an incident response playbook based on this incident:

1. Detection: How to identify this issue quickly
2. Triage: Steps to assess severity
3. Mitigation: Immediate actions to restore service
4. Investigation: How to find root cause
5. Resolution: Steps to fix permanently
6. Communication: What to tell stakeholders
7. Post-mortem: What to document
8. Prevention: How to avoid recurrence

Base it on these logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Step-by-step playbook, decision trees, command references, communication templates. [See details →](./expected-outcomes.md#-prompt-10-incident-response-playbook)

---

### 📈 Prompt 11: SLO/SLI Definition

```
Based on these logs, define appropriate SLOs and SLIs:

1. What should we measure? (SLIs)
2. What are acceptable thresholds? (SLOs)
3. What is the error budget?
4. How do we calculate availability?
5. What are the critical user journeys?
6. Provide Prometheus queries for each SLI
7. Design SLO dashboards
8. Create SLO violation alerts

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** SLI definitions, SLO targets, error budgets, Prometheus queries, dashboards. [See details →](./expected-outcomes.md#-prompt-11-slosli-definition)

---

### 🔐 Prompt 12: Security Analysis

```
Analyze these logs for security concerns:

1. Are there any suspicious patterns?
2. Is rate limiting working correctly?
3. Are authentication/authorization issues present?
4. Are there any potential attack vectors?
5. Is sensitive data being logged?
6. Recommend security improvements
7. Suggest security monitoring rules

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Security assessment, vulnerability identification, compliance check, recommendations. [See details →](./expected-outcomes.md#-prompt-12-security-analysis)

---

### 💰 Prompt 13: Cost Optimization

```
Analyze resource usage for cost optimization:

1. What resources are over-provisioned?
2. What resources are under-provisioned?
3. Are there inefficient queries costing money?
4. Can we reduce database connections?
5. Should we use read replicas more?
6. Recommend cost-saving measures
7. Calculate potential savings

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Resource utilization, over/under-provisioning, cost optimizations, savings estimates. [See details →](./expected-outcomes.md#-prompt-13-cost-optimization)

---

### 🧪 Prompt 14: Chaos Engineering Scenarios

```
Based on these logs, design chaos engineering experiments:

1. What failure scenarios should we test?
2. How can we safely reproduce this incident?
3. What other failure modes should we explore?
4. Design specific chaos experiments
5. Define success criteria for each experiment
6. Provide implementation steps
7. Suggest tools (Chaos Monkey, Gremlin, etc.)

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Experiment designs, test scenarios, success criteria, implementation guides. [See details →](./expected-outcomes.md#-prompt-14-chaos-engineering-scenarios)

---

### 📝 Prompt 15: Post-Mortem Report

```
Generate a comprehensive post-mortem report:

1. Executive Summary
2. Incident Timeline (with all services)
3. Root Cause Analysis (5 Whys)
4. Impact Assessment (customers, revenue, SLOs)
5. What Went Well
6. What Went Wrong
7. Action Items (with owners and deadlines)
8. Lessons Learned

Format for executive review.

Logs:
[PASTE ALL THREE LOG FILES]
```

**Expected Output:** Professional post-mortem with executive summary, timeline, action items, lessons learned. [See details →](./expected-outcomes.md#-prompt-15-post-mortem-report)

---

## 🎯 Advanced Prompt Techniques

### Technique 1: Comparative Analysis

```
Compare the behavior of successful vs. failed requests:

Successful request: req-u1v2w3x4
Failed request: req-i9j0k1l2

What are the differences in:
1. Timing
2. Resource usage
3. Code paths taken
4. Database queries executed

Logs:
[PASTE ALL THREE LOG FILES]
```

### Technique 2: Time-Series Analysis

```
Analyze how metrics changed over time:

Create a time-series view of:
1. Request rate per service
2. Error rate per service
3. Response time percentiles
4. Database connection pool usage
5. Circuit breaker state changes

Present as a table with 5-minute intervals.

Logs:
[PASTE ALL THREE LOG FILES]
```

### Technique 3: Dependency Mapping

```
Create a dependency map showing:

1. Which services call which services
2. What databases each service uses
3. What external APIs are called
4. Where failures propagate
5. Critical paths through the system

Represent as a diagram description or ASCII art.

Logs:
[PASTE ALL THREE LOG FILES]
```

---

## 📋 Prompt Chaining for Complex Analysis

```
Step 1: Multi-Service Correlation (Prompt 1)
   ↓
Step 2: Request Tracing (Prompt 2) - Focus on failed requests
   ↓
Step 3: Database Deep Dive (Prompt 3) - Identified as root cause
   ↓
Step 4: Circuit Breaker Analysis (Prompt 4) - Evaluate protection
   ↓
Step 5: Architecture Review (Prompt 6) - Long-term fixes
   ↓
Step 6: Incident Response Playbook (Prompt 10) - Documentation
   ↓
Step 7: Post-Mortem Report (Prompt 15) - Final documentation
```

---

## 🎓 Quality Validation

For detailed success criteria, quality indicators, multi-service analysis checklist, and comprehensive example outputs, see **[expected-outcomes.md](./expected-outcomes.md)**.

**Quick Checklist:**
- ✅ Events correlated across all services
- ✅ True root cause identified (not symptoms)
- ✅ Cascading failure mechanism explained
- ✅ Resilience patterns evaluated
- ✅ Service-specific recommendations provided
- ✅ Architectural improvements included

---

## 🔗 Related Resources

- **Expected Outcomes Cheat Sheet**: [expected-outcomes.md](./expected-outcomes.md) ⭐
- **Main README**: [../README.md](../README.md)
- **Log Files**: `api-gateway.log`, `billing-service.log`, `database.log`
- **Simple Scenario**: [../simple-scenario/analysis-prompts.md](../simple-scenario/analysis-prompts.md)

---

## 🎯 Quick Reference

| Analysis Type | Use Prompt | Time Required |
|--------------|------------|---------------|
| Initial triage | Prompt 1 | 5-10 min |
| Request tracing | Prompt 2 | 10-15 min |
| Database issues | Prompt 3 | 15-20 min |
| Circuit breaker | Prompt 4 | 10 min |
| Architecture | Prompt 6 | 20-30 min |
| Post-mortem | Prompt 15 | 30-45 min |