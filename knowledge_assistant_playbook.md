# Knowledge Assistant Playbook (Gamma-Governed)

## Use Case
Enterprise internal knowledge assistant with controlled outputs.

## Prompt Structure

1. Context Injection:
- Only use approved knowledge base
- No external assumptions

2. Validation Step:
- Check completeness of information
- If missing → request clarification

3. Output Rules:
- Provide answer ONLY if confidence is high
- Otherwise respond:
  "Insufficient information to proceed safely"

## Governance Layer
- All responses evaluated before exposure
- Unsafe or uncertain outputs are blocked
