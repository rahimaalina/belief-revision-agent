from belief_base import BeliefBase

# Create belief base
bb = BeliefBase()

# Add beliefs
bb.add("A", priority=1)
bb.add("A -> B", priority=2)
bb.add("C", priority=2)

# Show beliefs
bb.show()