# Expected Outcomes Cheat Sheet - Complex Scenario

> **Quick Reference Guide**: Use this to validate LLM responses for multi-service microservices analysis.

---

## 🎯 Prompt 1: Multi-Service Correlation Analysis

**What to Look For:**
- ✅ Cross-service event correlation (using request_ids)
- ✅ Root cause identification (primary + contributing factors)
- ✅ Cascading failure diagram (visual or text-based)
- ✅ Timeline with all services (synchronized timestamps)
- ✅ Service-specific recommendations (actionable per service)

**Quality Indicators:**
- Events are correlated across all three services
- Root cause is the true origin (not downstream symptoms)
- Failure propagation is clearly explained
- Timeline shows cause-and-effect across services
- Recommendations address each service's issues

---

## 🔗 Prompt 2: Request Tracing

**What to Look For:**
- ✅ Request flow diagrams (gateway → service → database)
- ✅ Timing breakdown per service (latency at each hop)
- ✅ Failure point identification (where and why)
- ✅ Performance comparison (successful vs. failed requests)

**Quality Indicators:**
- Complete journey traced for each request_id
- Timing shows cumulative latency
- Failure points are specific (service + operation)
- Comparison reveals performance patterns

---

## 💾 Prompt 3: Database Performance Deep Dive

**What to Look For:**
- ✅ Query performance analysis (execution times, patterns)
- ✅ Index recommendations with SQL (CREATE INDEX statements)
- ✅ Deadlock explanation (which transactions, why)
- ✅ Connection pool tuning (size, timeout recommendations)
- ✅ Query optimization suggestions (specific rewrites)

**Quality Indicators:**
- Identifies specific problematic queries
- Explains why queries are slow (missing indexes, locks)
- Provides executable SQL for indexes
- Connection pool recommendations are data-driven
- Query optimizations are concrete

---

## 🔄 Prompt 4: Circuit Breaker Analysis

**What to Look For:**
- ✅ Circuit breaker timeline (open → half-open → closed)
- ✅ Configuration evaluation (threshold appropriateness)
- ✅ Effectiveness assessment (did it protect the system?)
- ✅ Improvement recommendations (tuning parameters)

**Quality Indicators:**
- Timeline shows state transitions with timestamps
- Evaluates if threshold (5 failures) was appropriate
- Assesses if circuit breaker prevented further damage
- Recommendations are specific (e.g., "reduce to 3 failures")

---

## ⚡ Prompt 5: Performance Bottleneck Identification

**What to Look For:**
- ✅ Bottleneck inventory (ranked by impact)
- ✅ Performance metrics (response times, throughput)
- ✅ Resource utilization analysis (CPU, memory, connections)
- ✅ Optimization roadmap (prioritized improvements)

**Quality Indicators:**
- Bottlenecks are ranked by severity
- Metrics are quantified (not just "slow")
- Resource constraints are identified
- Roadmap is actionable and prioritized

---

## 🏗️ Prompt 6: Architecture Review

**What to Look For:**
- ✅ Architecture assessment (what works, what doesn't)
- ✅ Pattern evaluation (circuit breakers, timeouts, etc.)
- ✅ Improvement recommendations (caching, queues, etc.)
- ✅ Architecture diagram description (revised design)

**Quality Indicators:**
- Evaluates actual patterns in use
- Identifies architectural weaknesses
- Recommendations are architectural (not just code fixes)
- Diagram description is clear and implementable

---

## 📊 Prompt 7: Capacity Planning

**What to Look For:**
- ✅ Current capacity metrics (load, utilization)
- ✅ Growth projections (2x, 5x, 10x scenarios)
- ✅ Scaling recommendations (horizontal, vertical)
- ✅ Auto-scaling policies (triggers, thresholds)

**Quality Indicators:**
- Current metrics are extracted from logs
- Projections are based on observed patterns
- Scaling recommendations are specific
- Auto-scaling policies are implementable

---

## 🛡️ Prompt 8: Resilience Pattern Evaluation

**What to Look For:**
- ✅ Pattern-by-pattern evaluation (timeouts, retries, etc.)
- ✅ Effectiveness scores (working/not working)
- ✅ Gap analysis (missing patterns)
- ✅ Implementation recommendations (specific patterns to add)

**Quality Indicators:**
- Evaluates all resilience patterns present
- Scores are justified with evidence
- Identifies missing critical patterns
- Recommendations are prioritized

---

## 🔍 Prompt 9: Observability Assessment

**What to Look For:**
- ✅ Logging assessment (sufficient, consistent, useful)
- ✅ Missing metrics identification (what should be tracked)
- ✅ Tracing recommendations (distributed tracing strategy)
- ✅ Dashboard designs (layout, widgets, queries)
- ✅ Alert rules (conditions, thresholds, severity)

**Quality Indicators:**
- Evaluates current logging quality
- Identifies specific missing metrics
- Tracing recommendations are practical
- Dashboard designs are actionable
- Alert rules are implementable

---

## 🚨 Prompt 10: Incident Response Playbook

**What to Look For:**
- ✅ Step-by-step playbook (detection → resolution)
- ✅ Decision trees (if X then Y)
- ✅ Command references (copy-paste ready)
- ✅ Communication templates (stakeholder updates)

**Quality Indicators:**
- Playbook covers full incident lifecycle
- Decision trees handle multiple scenarios
- Commands are executable
- Templates are professional

---

## 📈 Prompt 11: SLO/SLI Definition

**What to Look For:**
- ✅ SLI definitions (what to measure)
- ✅ SLO targets (acceptable thresholds)
- ✅ Error budget calculations (math shown)
- ✅ Prometheus queries (executable)
- ✅ Dashboard designs (SLO tracking)

**Quality Indicators:**
- SLIs are measurable and relevant
- SLO targets are realistic
- Error budget math is correct
- Prometheus queries work
- Dashboards show SLO compliance

---

## 🔐 Prompt 12: Security Analysis

**What to Look For:**
- ✅ Security assessment (vulnerabilities, risks)
- ✅ Vulnerability identification (specific issues)
- ✅ Compliance check (logging sensitive data?)
- ✅ Security recommendations (hardening measures)

**Quality Indicators:**
- Identifies actual security issues in logs
- Vulnerabilities are specific and actionable
- Checks for sensitive data exposure
- Recommendations follow security best practices

---

## 💰 Prompt 13: Cost Optimization

**What to Look For:**
- ✅ Resource utilization analysis (over/under-provisioned)
- ✅ Over/under-provisioning identification (specific resources)
- ✅ Cost optimization recommendations (concrete actions)
- ✅ Savings estimates (quantified)

**Quality Indicators:**
- Analysis is based on actual usage patterns
- Identifies specific over-provisioned resources
- Recommendations have cost impact estimates
- Savings are quantified (e.g., "reduce by 30%")

---

## 🧪 Prompt 14: Chaos Engineering Scenarios

**What to Look For:**
- ✅ Experiment designs (specific failure scenarios)
- ✅ Test scenarios (how to reproduce safely)
- ✅ Success criteria (what defines success)
- ✅ Implementation guides (step-by-step)

**Quality Indicators:**
- Experiments target actual failure modes
- Scenarios are safe to run
- Success criteria are measurable
- Implementation is detailed

---

## 📝 Prompt 15: Post-Mortem Report

**What to Look For:**
- ✅ Professional post-mortem (executive-ready)
- ✅ Executive summary (concise, clear)
- ✅ Detailed timeline (all services, synchronized)
- ✅ Action items (owners, deadlines, priorities)
- ✅ Lessons learned (what to do differently)

**Quality Indicators:**
- Executive summary is 2-3 sentences
- Timeline is complete and accurate
- Action items are specific and assigned
- Lessons learned are actionable
- Professional tone throughout

---

## 🎯 Advanced Techniques Quality Indicators

### Comparative Analysis
- ✅ Side-by-side comparison of successful vs. failed requests
- ✅ Differences clearly identified (timing, resources, paths)
- ✅ Insights explain why one succeeded and other failed

### Time-Series Analysis
- ✅ Metrics presented in time intervals (5-min buckets)
- ✅ Trends are visible (degradation over time)
- ✅ Correlations between metrics shown

### Dependency Mapping
- ✅ All service dependencies identified
- ✅ Failure propagation paths shown
- ✅ Critical paths highlighted
- ✅ Visual representation (ASCII art or description)

---

## 📋 Multi-Service Analysis Checklist

### Cross-Service Correlation
- [ ] Events correlated using request_ids
- [ ] Timestamps synchronized across services
- [ ] Cause-and-effect relationships identified
- [ ] Cascading failure path traced

### Root Cause Analysis
- [ ] True root cause identified (not symptoms)
- [ ] Contributing factors listed
- [ ] Evidence from all services provided
- [ ] 5 Whys analysis performed

### Service-Specific Recommendations
- [ ] Each service has specific recommendations
- [ ] Recommendations address root causes
- [ ] Implementation steps provided
- [ ] Priority/impact assessed

### System-Wide Improvements
- [ ] Architectural improvements suggested
- [ ] Resilience patterns evaluated
- [ ] Observability gaps identified
- [ ] Long-term fixes proposed

---

## 🎯 Example: Excellent Multi-Service Analysis

```markdown
## Incident Analysis: Billing System Cascading Failure

### Executive Summary
Database deadlock at 10:20:12 caused connection pool exhaustion, 
triggering circuit breaker at API Gateway, resulting in 30-minute 
service outage affecting 47 customer transactions.

### Timeline (All Services)
| Time | Service | Event | Impact |
|------|---------|-------|--------|
| 10:20:12 | Database | Deadlock on accounts table | Transaction rolled back |
| 10:20:17 | Billing | Connection timeout (5s exceeded) | Request failed |
| 10:20:17 | Gateway | 504 Gateway Timeout | Customer sees error |
| 10:20:22 | Database | Connection pool exhausted (20/20) | New requests queued |
| 10:20:27 | Billing | 5 consecutive failures | Circuit breaker opens |
| 10:20:27 | Gateway | Circuit breaker OPEN | All requests rejected (503) |
| ... | ... | ... | ... |

### Root Cause Analysis

**Primary Root Cause**: Database deadlock on `accounts` table

**Contributing Factors**:
1. Missing index on `accounts.customer_id` (full table scan)
2. Long-running transactions (8.9s average)
3. Insufficient connection pool size (20 connections)
4. No connection timeout at application level

**Evidence**:
```
[Database 10:20:12] ERROR: deadlock detected
  Process 1234: UPDATE accounts SET balance = ...
  Process 5678: UPDATE accounts SET balance = ...
[Billing 10:20:17] ERROR: Connection timeout after 5000ms
[Gateway 10:20:27] WARN: Circuit breaker OPEN (5 failures)
```

### Cascading Failure Flow
```
Database Deadlock (10:20:12)
    ↓
Transaction Timeout (5s)
    ↓
Connection Not Released
    ↓
Pool Exhaustion (20/20)
    ↓
New Requests Timeout
    ↓
Circuit Breaker Opens (5 failures)
    ↓
Service Unavailable (503)
```

### Service-Specific Recommendations

#### Database (Priority: CRITICAL)
1. **Add index immediately**:
   ```sql
   CREATE INDEX idx_accounts_customer_id 
   ON accounts(customer_id);
   ```
   Impact: Reduce query time from 8.9s to <100ms
   
2. **Tune deadlock detection**:
   ```sql
   SET deadlock_timeout = '1s';
   ```
   
3. **Implement connection pooling at DB level**:
   - Deploy PgBouncer
   - Configure: pool_size=50, max_client_conn=100

#### Billing Service (Priority: HIGH)
1. **Increase connection pool size**:
   ```yaml
   database:
     pool_size: 30  # was 20
     max_overflow: 10
     pool_timeout: 30
   ```
   
2. **Add connection timeout monitoring**:
   ```python
   @app.before_request
   def check_pool_health():
       if pool.size() > pool.max_size * 0.8:
           alert("Connection pool at 80%")
   ```
   
3. **Implement retry with exponential backoff**:
   ```python
   @retry(stop=stop_after_attempt(3), 
          wait=wait_exponential(multiplier=1, min=1, max=10))
   def execute_query():
       ...
   ```

#### API Gateway (Priority: MEDIUM)
1. **Adjust circuit breaker threshold**:
   ```yaml
   circuit_breaker:
     failure_threshold: 3  # was 5
     timeout: 30s
     half_open_max_requests: 5
   ```
   
2. **Implement adaptive timeouts**:
   - Monitor P95 response time
   - Set timeout = P95 * 2
   
3. **Add request queuing**:
   - Queue size: 100
   - Timeout: 10s

### Impact Assessment
- **Duration**: 30 minutes (10:20 - 10:50)
- **Affected Requests**: 47 transactions
- **Estimated Customers**: ~15 unique users
- **Revenue Impact**: ~$2,350 (estimated)
- **SLO Breach**: 99.9% availability target missed

### Lessons Learned
1. ✅ Circuit breaker worked as designed (protected system)
2. ❌ Missing database indexes caused performance issues
3. ❌ Connection pool too small for peak load
4. ✅ Request IDs enabled effective troubleshooting
5. ❌ No proactive monitoring for connection pool exhaustion

### Action Items
| Priority | Action | Owner | Deadline | Status |
|----------|--------|-------|----------|--------|
| P0 | Add database index | DBA Team | Today | [ ] |
| P0 | Increase connection pool | Backend Team | Today | [ ] |
| P1 | Deploy PgBouncer | DevOps | This week | [ ] |
| P1 | Add pool monitoring | SRE Team | This week | [ ] |
| P2 | Tune circuit breaker | Backend Team | Next week | [ ] |
| P2 | Implement retry logic | Backend Team | Next week | [ ] |
```

---

## 📚 Related Resources

- **Prompt Templates**: `analysis-prompts.md`
- **Log Files**: `api-gateway.log`, `billing-service.log`, `database.log`
- **Main Documentation**: `../README.md`
- **Simple Scenario**: `../simple-scenario/expected-outcomes.md`