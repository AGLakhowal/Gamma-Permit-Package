from gamma_governance import GammaEngine, ActionProposal
from execution_layer import FinancialActuator

# Initialize the deterministic governance engine
# v1.1 implements the Lakhowal Law of Concurrence (LLC)
gamma = GammaEngine(
    policy_version="1.4.2",
    fail_closed=True
)

# AI model proposes an externally effective action (e.g., from an LLM or RL agent)
proposal = ActionProposal(
    action_type="FUNDS_TRANSFER",
    amount=500000,
    target_node="EXTERNAL_GATEWAY",
    uncertainty_score=0.85
)

# Governance layer evaluates the Gamma value (Γ)
permit = gamma.evaluate(proposal)

if permit.is_valid() and permit.gamma_value == 0:
    # SUCCESS: The actuator MUST cryptographically verify the token before acting.
    # This is the non-bypassable enforcement boundary.
    FinancialActuator.verify_and_execute(proposal, permit.get_cryptographic_token())
else:
    # FAILURE: Deterministic denial → transition to safe state.
    print(f"Execution Denied. Violations: {permit.get_violations()}")
    FinancialActuator.safe_halt()
