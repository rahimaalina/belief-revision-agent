from belief_base import BeliefBase
from entailment import Entailment

# Create belief base
bb = BeliefBase()

# Add beliefs
bb.add("A", priority=1)
bb.add("A -> B", priority=2)
bb.add("C", priority=2)

# Show beliefs
bb.show()

entailment = Entailment(bb)

# Test entailment (should be True)
print("Does belief base entail B?")
print(entailment.entails("B"))

# Test a false entailment (should be False)
print("Does belief base entail D?")
print(entailment.entails("D"))

# Test negation (should be False because C is in KB)
print("Does belief base entail NOT C?")
print(entailment.entails("NOT C"))

# Test CNF conversion with more complex inputs
bb.add("A AND D", priority=1)
bb.add("NOT (A AND B)", priority=1)
bb.add("A OR (B AND C)", priority=1)

print("\nCNF beliefs after adding more formulas:")
print(bb.get_cnf_beliefs())