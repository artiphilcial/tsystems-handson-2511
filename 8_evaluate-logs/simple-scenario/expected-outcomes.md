# Expected Outcomes Cheat Sheet - Simple Scenario

> **Quick Reference Guide**: Use this to validate LLM responses and understand what good analysis looks like.

---

## 🎯 Prompt 1: Initial Analysis

**What to Look For:**
- ✅ List of identified issues (with severity levels)
- ✅ Root cause analysis for each issue
- ✅ Severity assessment (Critical, High, Medium, Low)
- ✅ Chronological timeline with timestamps
- ✅ Actionable recommendations with specific steps

**Quality Indicators:**
- Issues are distinct and not duplicated
- Root causes go beyond symptoms
- Timeline shows cause-and-effect relationships
- Recommendations are specific (not generic advice)

---

## 🔍 Prompt 2: Authentication Issue Deep Dive

**What to Look For:**
- ✅ Failed login analysis (count, patterns, users affected)
- ✅ Security pattern detection (brute force, credential stuffing)
- ✅ Account lockout evaluation (threshold, duration, effectiveness)
- ✅ Security recommendations (specific improvements)

**Quality Indicators:**
- Identifies attack patterns vs. legitimate failures
- Evaluates security mechanism effectiveness
- Provides concrete security improvements
- Considers user experience impact

---

## 💾 Prompt 3: Database Performance Analysis

**What to Look For:**
- ✅ Connection pool metrics (utilization over time)
- ✅ Slow query identification (with execution times)
- ✅ Root cause of exhaustion (not just symptoms)
- ✅ SQL optimization suggestions (specific queries/indexes)

**Quality Indicators:**
- Quantifies connection pool usage patterns
- Identifies specific slow queries with timings
- Explains why exhaustion occurred
- Provides executable SQL statements

---

## 📊 Prompt 4: Impact Assessment

**What to Look For:**
- ✅ Customer impact numbers (affected users)
- ✅ Service availability metrics (uptime %)
- ✅ Downtime calculation (duration, windows)
- ✅ Customer experience score (1-10 scale with justification)

**Quality Indicators:**
- Uses actual numbers from logs
- Calculates availability percentage correctly
- Considers business hours vs. off-hours
- Provides context for experience score

---

## 🛠️ Prompt 5: Remediation Plan

**What to Look For:**
- ✅ Prioritized action plan (immediate → long-term)
- ✅ Specific implementation steps (commands, code changes)
- ✅ Risk assessment (for each action)
- ✅ Time estimates (realistic)

**Quality Indicators:**
- Actions are prioritized by impact and urgency
- Includes actual commands/code snippets
- Considers risks and mitigation
- Time estimates are reasonable

---

## 📈 Prompt 6: Monitoring Strategy

**What to Look For:**
- ✅ Metrics list (specific, measurable)
- ✅ Alert thresholds (with justification)
- ✅ Dashboard designs (layout, widgets)
- ✅ Alert rules (conditions, severity)
- ✅ Sample queries (Prometheus, SQL, etc.)

**Quality Indicators:**
- Metrics are actionable and relevant
- Thresholds based on observed behavior
- Dashboards show key indicators
- Queries are executable

---

## 🔄 Prompt 7: Incident Report Generation

**What to Look For:**
- ✅ Professional incident report (management-ready)
- ✅ Executive summary (2-3 sentences)
- ✅ Timeline with timestamps
- ✅ Clear action items (owners, deadlines)

**Quality Indicators:**
- Executive summary is concise and clear
- Timeline is accurate and complete
- Action items are specific and assigned
- Professional tone throughout

---

## 🧪 Prompt 8: Test Case Generation

**What to Look For:**
- ✅ Test case descriptions (clear scenarios)
- ✅ Sample test code (Python/Java)
- ✅ Expected behaviors (assertions)
- ✅ Edge cases to cover

**Quality Indicators:**
- Tests cover the actual issues found
- Code is executable and follows best practices
- Includes both positive and negative tests
- Edge cases are realistic

---

## 🎓 Prompt 9: Training Material

**What to Look For:**
- ✅ Training documentation (clear, structured)
- ✅ Troubleshooting flowcharts (decision trees)
- ✅ Command reference (copy-paste ready)
- ✅ Best practices guide

**Quality Indicators:**
- Suitable for junior engineers
- Step-by-step instructions
- Real examples from the logs
- Includes "when to escalate" guidance

---

## 🔮 Prompt 10: Predictive Analysis

**What to Look For:**
- ✅ Failure prediction patterns (early warning signs)
- ✅ Early warning indicators (specific metrics)
- ✅ Capacity recommendations (scaling guidance)
- ✅ Proactive measures (preventive actions)

**Quality Indicators:**
- Patterns are based on log evidence
- Indicators are measurable
- Capacity recommendations are data-driven
- Proactive measures are actionable

---

## 📋 General Quality Checklist

Use this for any prompt response:

### Content Quality
- [ ] Addresses all points in the prompt
- [ ] Uses evidence from the logs
- [ ] Provides specific, actionable recommendations
- [ ] Includes examples (code, commands, queries)
- [ ] Considers business impact

### Technical Accuracy
- [ ] Root causes are correct (not just symptoms)
- [ ] Timing and causation are accurate
- [ ] Technical recommendations are sound
- [ ] Code/commands are executable
- [ ] Follows best practices

### Presentation
- [ ] Well-structured and organized
- [ ] Uses appropriate formatting
- [ ] Includes relevant metrics/numbers
- [ ] Professional tone
- [ ] Easy to understand

---

## 🎯 Example: Good vs. Poor Output

### ❌ Poor Output Example
```
Issue: Database problems
Severity: High
Fix: Optimize the database
```

### ✅ Good Output Example
```
## Issue: Database Connection Pool Exhaustion

**Severity**: Critical
**First Occurrence**: 2024-01-15 10:15:23
**Last Occurrence**: 2024-01-15 10:45:17
**Frequency**: 47 occurrences over 30 minutes

### Root Cause
Connection pool exhausted (20/20 connections in use) due to:
1. Slow query on `customer_orders` table (avg 8.2s execution time)
2. Missing index on `customer_id` column
3. Connections not being released due to long-running transactions

### Impact
- 47 failed requests (503 errors)
- ~15 customers affected
- 30-minute service degradation

### Evidence
```
[2024-01-15 10:15:23] ERROR: Connection pool exhausted (20/20)
[2024-01-15 10:15:24] WARN: Query execution time: 8.2s
```

### Recommended Fix
1. Add index immediately:
   ```sql
   CREATE INDEX idx_customer_orders_customer_id 
   ON customer_orders(customer_id);
   ```
2. Increase pool size to 30 connections
3. Add connection timeout monitoring
4. Implement query timeout (5s max)

### Prevention
- Monitor connection pool utilization (alert at 80%)
- Add slow query logging (threshold: 1s)
- Regular index analysis
- Connection leak detection
```

---

## 📚 Related Resources

- **Prompt Templates**: `analysis-prompts.md`
- **Log File**: `customer-portal.log`
- **Main Documentation**: `../README.md`
- **Complex Scenario**: `../complex-scenario/expected-outcomes.md`