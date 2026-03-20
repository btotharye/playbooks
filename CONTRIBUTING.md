# Contributing to Syntaxctl

Thanks for interest in Syntaxctl! We welcome contributions.

## How to Contribute

### Adding a New Prompt

1. Create a new file in `prompts/{category}/{task_name}.yaml`
2. Follow the YAML format (see existing prompts for examples)
3. Include metadata, inputs, outputs, and prompt_text
4. Add at least one example with input/output
5. Test your prompt with Claude
6. Update quality_score (0-1) based on testing
7. Add test_count and production_tested fields
8. Open a PR with description of the prompt

### Improving Existing Prompts

1. Test the prompt in your use case
2. Document improvements
3. Update quality_score if reliability changed
4. Include before/after examples
5. Open a PR explaining the improvement

### Code Changes

1. Follow PEP 8 style
2. Add tests for new functionality
3. Run `pytest` and `ruff` locally
4. Update README if needed
5. Open PR with description

## Prompt Format

```yaml
metadata:
  id: "category-task-version"
  name: "Human Readable Name"
  category: "deployment|cost_optimization|incident_response|compliance|security"
  version: "1.0.0"
  quality_score: 0.85  # 0-1
  production_tested: true
  test_count: 25

inputs:
  - name: "param_name"
    type: "string|integer|float|array"
    description: "What is this?"
    example: "example_value"

outputs:
  - name: "output_name"
    type: "string|integer|array"
    description: "What does this mean?"

prompt_text: |
  You are an expert...
  
  {param_name}: {param_example}
  
  Respond with JSON:
  {{...}}

examples:
  - input: {...}
    output: {...}
```

## Testing Prompts

Before submitting:

1. Copy the prompt_text
2. Substitute real values for {placeholders}
3. Paste into Claude
4. Test with 3-5 different scenarios
5. Record test results

Quality scores:
- 0.9-1.0: Excellent, production-ready
- 0.8-0.9: Good, works most cases
- 0.7-0.8: Decent, needs refinement
- <0.7: Alpha, not production-ready

## Code Review

- Quality > quantity (fewer well-tested prompts beats many mediocre ones)
- Production examples required
- Clear variable naming
- Good descriptions

## Questions?

Open a discussion: github.com/btotharye/playbooks/discussions
