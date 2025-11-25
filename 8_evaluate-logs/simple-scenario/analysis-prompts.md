# Simple Scenario - LLM Analysis Prompts

> 📋 **Quick Reference**: See [expected-outcomes.md](./expected-outcomes.md) for detailed quality criteria and validation checklist.

## Prompt Templates for Customer Portal Log Analysis

### 🎯 Prompt 1: Initial Analysis

```
I have a log file from a customer portal application that's experiencing issues. 
Please analyze these logs and:

1. Identify all distinct problems or issues present
2. Determine the root cause of each issue
3. Assess the severity and impact of each problem
4. Provide a timeline of events
5. Suggest specific debugging steps and fixes

Here are the logs:

[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Issues list, root causes, severity levels, timeline, recommendations. [See details →](./expected-outcomes.md#-prompt-1-initial-analysis)

---

### 🔍 Prompt 2: Authentication Issue Deep Dive

```
Focus specifically on authentication-related issues in these logs:

1. Identify all failed login attempts
2. Determine if there are patterns (brute force, credential stuffing, etc.)
3. Explain the account lockout mechanism
4. Assess if the security measures are working correctly
5. Recommend improvements to the authentication system

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Login analysis, security patterns, lockout evaluation. [See details →](./expected-outcomes.md#-prompt-2-authentication-issue-deep-dive)

---

### 💾 Prompt 3: Database Performance Analysis

```
Analyze the database-related issues in these logs:

1. Identify all database connection problems
2. Calculate connection pool utilization over time
3. Find slow queries and their execution times
4. Determine the root cause of connection exhaustion
5. Provide specific SQL optimization recommendations

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Pool metrics, slow queries, root cause, SQL optimizations. [See details →](./expected-outcomes.md#-prompt-3-database-performance-analysis)

---

### 📊 Prompt 4: Impact Assessment

```
Based on these logs, provide a business impact assessment:

1. How many customers were affected?
2. What was the duration of the outage/degradation?
3. Which services were impacted?
4. Calculate the approximate downtime percentage
5. Estimate the customer experience impact (1-10 scale)

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Impact numbers, availability metrics, downtime calculation. [See details →](./expected-outcomes.md#-prompt-4-impact-assessment)

---

### 🛠️ Prompt 5: Remediation Plan

```
Based on your analysis of these logs, create a detailed remediation plan:

1. Immediate actions (next 1 hour)
2. Short-term fixes (next 24 hours)
3. Medium-term improvements (next week)
4. Long-term architectural changes (next month)
5. Monitoring and alerting recommendations

For each action, provide:
- Specific commands or code changes
- Expected impact
- Risk level
- Estimated time to implement

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Prioritized actions, implementation steps, risk assessment. [See details →](./expected-outcomes.md#-prompt-5-remediation-plan)

---

### 📈 Prompt 6: Monitoring Strategy

```
Based on the issues found in these logs, design a monitoring strategy:

1. What metrics should we track?
2. What alert thresholds should we set?
3. What dashboards should we create?
4. What log patterns should trigger alerts?
5. Provide example Prometheus/Grafana queries

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Metrics, thresholds, dashboards, alert rules, queries. [See details →](./expected-outcomes.md#-prompt-6-monitoring-strategy)

---

### 🔄 Prompt 7: Incident Report Generation

```
Generate a formal incident report based on these logs:

1. Executive Summary (2-3 sentences)
2. Timeline of Events (with timestamps)
3. Root Cause Analysis
4. Impact Assessment
5. Resolution Steps Taken
6. Preventive Measures
7. Lessons Learned

Format the report professionally for management review.

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Professional incident report with timeline and action items. [See details →](./expected-outcomes.md#-prompt-7-incident-report-generation)

---

### 🧪 Prompt 8: Test Case Generation

```
Based on the issues found in these logs, generate test cases to prevent similar problems:

1. Unit tests for authentication logic
2. Integration tests for database connection handling
3. Load tests for connection pool behavior
4. Security tests for account lockout
5. Provide test code in Python/Java

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Test cases, sample code, expected behaviors, edge cases. [See details →](./expected-outcomes.md#-prompt-8-test-case-generation)

---

### 🎓 Prompt 9: Training Material

```
Create training material for the operations team based on these logs:

1. Common issues and how to identify them
2. Step-by-step troubleshooting guide
3. When to escalate
4. Useful commands and queries
5. Best practices for log analysis

Make it suitable for junior engineers.

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Training docs, troubleshooting guides, command reference. [See details →](./expected-outcomes.md#-prompt-9-training-material)

---

### 🔮 Prompt 10: Predictive Analysis

```
Analyze these logs to predict potential future issues:

1. What patterns indicate impending failures?
2. What early warning signs should we watch for?
3. What capacity planning insights can you derive?
4. What proactive measures should we take?
5. Create a predictive alert strategy

Logs:
[PASTE CONTENTS OF customer-portal.log HERE]
```

**Expected Output:** Prediction patterns, warning signs, capacity insights. [See details →](./expected-outcomes.md#-prompt-10-predictive-analysis)

---

## 📋 Prompt Chaining Example

For complex analysis, chain prompts together:

```
Step 1: Use Prompt 1 (Initial Analysis)
   ↓
Step 2: Use Prompt 3 (Database Deep Dive) on identified DB issues
   ↓
Step 3: Use Prompt 5 (Remediation Plan) based on findings
   ↓
Step 4: Use Prompt 6 (Monitoring Strategy) to prevent recurrence
   ↓
Step 5: Use Prompt 7 (Incident Report) for documentation
```

---

## 🎯 Quality Validation

For detailed success criteria, quality indicators, and example outputs, see **[expected-outcomes.md](./expected-outcomes.md)**.

**Quick Checklist:**
- ✅ All major issues identified
- ✅ Accurate root cause analysis
- ✅ Actionable, specific fixes
- ✅ Code/command examples included
- ✅ Business impact considered

---

## 🔗 Related Resources

- **Expected Outcomes Cheat Sheet**: [expected-outcomes.md](./expected-outcomes.md) ⭐
- **Main README**: [../README.md](../README.md)
- **Log File**: `customer-portal.log`
- **Complex Scenario**: [../complex-scenario/analysis-prompts.md](../complex-scenario/analysis-prompts.md)