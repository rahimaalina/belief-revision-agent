from belief_base import BeliefBase
from entailment import Entailment

# Create belief base
bb = BeliefBase()

# Add beliefs
bb.add("A", priority=1)
bb.add("A -> B", priority=2)
bb.add("C", priority=2)

# Show beliefs
print("Initial belief base:")
bb.show()
#------------------------------


# Entailment
entailment = Entailment(bb)

# Entailment tests before contraction
print("\nEntailment tests (before contracting):")
# Test entailment (should be True)
print("Does belief base entail B?")
print(entailment.entails("B"))

# Test a false entailment (should be False)
print("Does belief base entail D?")
print(entailment.entails("D"))

# Test negation (should be False because C is in KB)
print("Does belief base entail NOT C?")
print(entailment.entails("NOT C"))
#------------------------------

# Contraction
print("\nContracting by B...")
bb.contract("B")

print("\nBelief base after contraction:")
bb.show()

entailment = Entailment(bb)

print("\nEntailment tests (after contracting):")
# Test entailment (should be False after contraction)
print("Does belief base entail B?")
print(entailment.entails("B"))
# Test a false entailment (should still be False)
print("Does belief base entail D?")
print(entailment.entails("D"))
# Test negation (should still be False because C is in KB)
print("Does belief base entail NOT C?")
print(entailment.entails("NOT C"))
#------------------------------

# Expansion

# Test expansion with new beliefs
bb.expand("D", priority=1)

print("\nBelief base after expansion:")
bb.show()


# Entailment after expansion
print("\nEntailment tests after expansion:")
print("Does belief base entail B?")
print(entailment.entails("B"))
print("Does belief base entail D?")
# This should be True since we added D in the expansion step
print(entailment.entails("D"))
# Test negation (should still be False because C is in KB)
print("Does belief base entail NOT C?")
print(entailment.entails("NOT C"))  
#------------------------------


# Test CNF conversion with more complex inputs
bb2 = BeliefBase()

# Add more complex beliefs
bb2.add("A -> B", priority=2)
bb2.add("C", priority=2)

print("\nAdding more complex beliefs")
# Test CNF conversion
bb2.add("A AND D", priority=1)
bb2.add("NOT (A AND B)", priority=1)
bb2.add("A OR (B AND C)", priority=1)

print("\nBelief base after adding more complex beliefs:")
bb2.show()

print("\nCNF beliefs after adding more formulas:")
print(bb2.get_cnf_beliefs())