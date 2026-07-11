---------------------------- MODULE LDREA ----------------------------
(***************************************************************************)
(* Machine-checked model of the L-DREA non-compensatory reference monitor. *)
(* A Permit-to-Act decision must be reachable ONLY when every enforcement   *)
(* control holds; if any control fails the decision must be SAFE_STATE.     *)
(* This is the formal companion to faithful_gate() in maincode.py.          *)
(***************************************************************************)
EXTENDS Naturals, TLC

CONSTANTS Controls          \* the set of enforcement control names

VARIABLES passed,           \* [Controls -> BOOLEAN] : which controls currently hold
          decision          \* "PENDING" | "PERMIT" | "SAFE_STATE"

vars == <<passed, decision>>

AllHold == \A c \in Controls : passed[c] = TRUE

TypeOK ==
    /\ passed \in [Controls -> BOOLEAN]
    /\ decision \in {"PENDING", "PERMIT", "SAFE_STATE"}

Init ==
    /\ passed \in [Controls -> BOOLEAN]   \* explore every combination of controls
    /\ decision = "PENDING"

Decide ==
    /\ decision = "PENDING"
    /\ decision' = IF AllHold THEN "PERMIT" ELSE "SAFE_STATE"
    /\ UNCHANGED passed

Done ==
    /\ decision # "PENDING"
    /\ UNCHANGED vars

Next == Decide \/ Done

Spec == Init /\ [][Next]_vars

\* Safety: a PERMIT is only ever reached when every control holds.
NoUnauthorizedPermit == (decision = "PERMIT") => AllHold

\* Non-compensatory: any single failing control forbids a PERMIT.
NonCompensatory == (\E c \in Controls : passed[c] = FALSE) => (decision # "PERMIT")
=============================================================================
