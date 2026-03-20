# Playbooks

**Battle-tested prompts for infrastructure agents. Like Ansible playbooks, but for AI.**

Transform your infrastructure operations with production-grade prompts for:
- 🚀 **Safe Deployments** — Canary rollouts, blue-green strategies, auto-rollback
- 💰 **Cost Optimization** — Find waste, reserved instances, spot opportunities
- 🔧 **Incident Response** — Diagnose issues, find root causes, auto-remediate
- ✅ **Compliance** — Verify MFA, encryption, audit logs, policy compliance
- 🛡️ **Security** — Vulnerability analysis, exposure assessment, patch recommendations

## Quick Start

### Install

```bash
pip install playbooks
# or with uv
uv pip install playbooks
```

### Use with Claude Directly

1. Browse prompts: `github.com/btotharye/syntaxctl/tree/main/prompts`
2. Copy the YAML prompt you need
3. Paste into Claude with your context
4. Get structured guidance in 30 seconds

### Use in Your Agent

```python
from playbooks import PromptLibrary

library = PromptLibrary()

# Load a prompt
prompt = library.get_prompt("deployment", "canary_rollout")

# Customize for your service
customized = prompt.customize(
    service_name="api-server",
    risk_level="critical",
    deployment_frequency=5,
    current_error_budget=25,
    slo=99.95
)

# Send to Claude (or any LLM)
response = claude.messages.create(
    messages=[{"role": "user", "content": customized}]
)

# Parse response
decision = json.loads(response.content[0].text)
print(f"Strategy: {decision['strategy']}")
print(f"Canary %: {decision['canary_percentage']}")
```

### Command Line

```bash
# List all prompts
playbooks list

# List by category
playbooks list --category deployment

# Show details
playbooks show deployment-canary-001

# Search
playbooks search "cost"

# Show version
playbooks version
```

## Available Prompts

### Deployment (5 prompts)
- `canary_rollout_strategy` — Decide rollout %, timing, and metrics
- `safe_deployment` — Validate safe to deploy
- `detect_bad_deployment` — Find issues early
- `rollback_decision` — Should we rollback?
- `blue_green_strategy` — Alternative to canary

### Cost Optimization (5 prompts)
- `find_waste` — Identify unused resources
- `reserved_vs_ondemand` — RI opportunity scoring
- `spot_decision` — When to use spot instances
- `region_optimization` — Region cost analysis
- `multi_cloud_arbitrage` — Cheapest cloud option

### Incident Response (7 prompts)
- `diagnose_high_error_rate` — Root cause analysis
- `diagnose_latency_spike` — Latency troubleshooting
- `diagnose_memory_leak` — Memory issue diagnosis
- `find_root_cause` — General root cause finder
- `remediation_decision` — Recommended fixes
- `post_incident_analysis` — Learning from incidents
- `escalation_decision` — When to page the team

### Compliance (5 prompts)
- `verify_mfa_enabled` — MFA enforcement check
- `check_encryption` — Encryption at rest/transit
- `audit_access_logs` — Access logging validation
- `data_residency` — Data location verification
- `policy_compliance` — General policy check

### Security (4 prompts)
- `analyze_vulnerability` — CVE impact assessment
- `assess_exposure` — Exposure analysis
- `recommend_patches` — Patch recommendations
- `security_hardening` — Hardening strategies

## Architecture

```
syntaxctl/
├── prompts/          (YAML prompt templates)
├── src/
│   ├── syntaxctl/    (Python library)
│   └── cli/          (Command-line tool)
├── examples/         (Usage examples)
└── tests/            (Test suite)
```

## Example: Incident Response

```python
from syntaxctl import PromptLibrary
import anthropic

library = PromptLibrary()

# Load incident response prompt
prompt = library.get_prompt("incident_response", "diagnose_error_rate")

# Customize with your monitoring data
customized = prompt.customize(
    error_rate=5.2,
    baseline_error_rate=0.3,
    recent_changes="Deployed v1.2.3 two hours ago",
    logs="""
    [ERROR] Connection refused: database connection pool exhausted
    [ERROR] 500 error: Cannot acquire database connection
    [WARN] Slow query detected: SELECT * FROM users (2.5s)
    """,
    metrics="""
    Error rate: 5.2% (baseline 0.3%)
    Database connections: 95/100 (pool size)
    CPU: 45%
    Memory: 60%
    """
)

# Get Claude's diagnosis
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": customized}]
)

# Parse and act on diagnosis
diagnosis = json.loads(response.content[0].text)
print(f"Root Cause: {diagnosis['root_cause']}")
print(f"Confidence: {diagnosis['confidence']}")
print(f"Immediate Actions: {diagnosis['immediate_actions']}")
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Add a new prompt:
1. Create `prompts/{category}/{task_name}.yaml`
2. Follow the prompt format (see examples)
3. Include quality metrics and production test count
4. Add examples with inputs/outputs
5. Open a PR

### Improve existing prompts:
1. Test in production
2. Document improvements
3. Update quality_score based on results
4. Open a PR with before/after examples

## Quality Metrics

Each prompt includes:
- **quality_score** (0-1) — How well it works in practice
- **production_tested** (true/false) — Has been used in production
- **test_count** — Number of production test runs

Lower-quality prompts are marked `🚧` in listings.

## Use Cases

### For SREs
Quick diagnostics when issues hit at 3am:
```bash
syntaxctl show incident-response-error-rate
# Copy prompt → Paste into Claude → Get diagnosis
```

### For Platform Engineers
Build infrastructure automation:
```python
agent = DeploymentAgent()
agent.library = PromptLibrary()
strategy = agent.decide_rollout(service)
```

### For DevOps Teams
Consistent approach to cost optimization:
```python
cost_agent = CostOptimizationAgent()
prompts = cost_agent.library.list_prompts("cost_optimization")
```

## License

MIT

## Support

- **Issues:** github.com/btotharye/playbooks/issues
- **Discussions:** github.com/btotharye/playbooks/discussions
- **Docs:** playbooks.sh

---

**Made with ❤️ for infrastructure teams.**

Like kubectl for prompts. Control your agents from the command line.
