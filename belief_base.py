class BeliefBase:
    def __init__(self):
        # List to store beliefs
        self.beliefs = []

        # Dictionary to store priorities
        self.priority = {}

    def add(self, belief, priority=1):
        """Add a belief with a priority"""
        if belief not in self.beliefs:
            self.beliefs.append(belief)
            self.priority[belief] = priority

    def remove(self, belief):
        """Remove a belief"""
        if belief in self.beliefs:
            self.beliefs.remove(belief)
            del self.priority[belief]

    def show(self):
        """Display all beliefs"""
        print("Belief Base:")
        for b in self.beliefs:
            print(f"- {b} (priority {self.priority[b]})")