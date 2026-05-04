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

    def contains(self, belief):
        """Check if a belief exists in the belief base"""
        return belief in self.beliefs

    def get_priority(self, belief):
        """Return the priority of a belief"""
        if belief in self.priority:
            return self.priority[belief]
        return None

    def update_priority(self, belief, priority):
        """Update the priority of an existing belief"""
        if belief in self.beliefs:
            self.priority[belief] = priority

    def get_all_beliefs(self):
        """Return all beliefs"""
        return self.beliefs

    def get_sorted_beliefs(self):
        """Return beliefs sorted by priority"""
        return sorted(self.beliefs, key=lambda b: self.priority[b])

    def to_cnf(self, belief):
        """
        Convert a belief into a simple CNF clause list.

        Supported input examples:
        - A
        - NOT A
        - A AND B
        - A OR B
        - A -> B
        - NOT (A AND B)
        - NOT (A OR B)

        Output format:
        - Each returned item is one clause string.
        - Literals inside one clause are separated by OR.
        """
        belief = belief.strip()

        # Remove one outer pair of parentheses if the whole formula is wrapped
        belief = self.remove_outer_parentheses(belief)

        # Handle double negation: NOT NOT A becomes A
        if belief.startswith("NOT NOT "):
            return self.to_cnf(belief[8:].strip())

        # Handle negated implication: NOT (A -> B) becomes A AND NOT B
        if belief.startswith("NOT (") and belief.endswith(")"):
            inside = belief[5:-1].strip()

            if "->" in inside:
                left, right = inside.split("->", 1)
                return self.to_cnf(f"{left.strip()} AND NOT {right.strip()}")

            # Handle De Morgan: NOT (A AND B) becomes NOT A OR NOT B
            and_parts = self.split_top_level(inside, "AND")
            if len(and_parts) > 1:
                return [" OR ".join(f"NOT {part.strip()}" for part in and_parts)]

            # Handle De Morgan: NOT (A OR B) becomes NOT A AND NOT B
            or_parts = self.split_top_level(inside, "OR")
            if len(or_parts) > 1:
                clauses = []
                for part in or_parts:
                    clauses.extend(self.to_cnf(f"NOT {part.strip()}"))
                return clauses

        # Handle implication: A -> B becomes NOT A OR B
        if "->" in belief:
            left, right = belief.split("->", 1)
            left = self.remove_outer_parentheses(left.strip())
            right = self.remove_outer_parentheses(right.strip())
            return [f"NOT {left} OR {right}"]

        # Handle conjunction: A AND B becomes separate clauses A and B
        and_parts = self.split_top_level(belief, "AND")
        if len(and_parts) > 1:
            clauses = []

            for part in and_parts:
                clauses.extend(self.to_cnf(part.strip()))

            return clauses

        # Handle distribution: A OR (B AND C) becomes (A OR B) AND (A OR C)
        or_parts = self.split_top_level(belief, "OR")
        if len(or_parts) > 1:
            distributed = self.distribute_or_over_and(belief)
            if distributed is not None:
                return distributed

            return [" OR ".join(self.remove_outer_parentheses(part.strip()) for part in or_parts)]

        # Literal case: A or NOT A
        return [belief]

    def remove_outer_parentheses(self, formula):
        """Remove one pair of outer parentheses only if they wrap the whole formula."""
        formula = formula.strip()

        if not (formula.startswith("(") and formula.endswith(")")):
            return formula

        depth = 0
        for index, char in enumerate(formula):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1

            # If depth reaches 0 before the final character, the outer parentheses
            # do not wrap the whole formula.
            if depth == 0 and index < len(formula) - 1:
                return formula

        return formula[1:-1].strip()

    def split_top_level(self, formula, operator):
        """
        Split a formula by AND/OR only when the operator is not inside parentheses.
        Example: A OR (B AND C) split by OR becomes ["A", "(B AND C)"].
        Example: A OR (B AND C) split by AND stays ["A OR (B AND C)"].
        """
        parts = []
        current = []
        depth = 0
        tokens = formula.split()

        for token in tokens:
            depth += token.count("(")
            depth -= token.count(")")

            if token == operator and depth == 0:
                parts.append(" ".join(current).strip())
                current = []
            else:
                current.append(token)

        parts.append(" ".join(current).strip())
        return parts

    def distribute_or_over_and(self, belief):
        """
        Handle simple distribution cases needed for CNF.
        Examples:
        - A OR (B AND C) becomes ["A OR B", "A OR C"]
        - (A AND B) OR C becomes ["A OR C", "B OR C"]
        """
        or_parts = self.split_top_level(belief, "OR")

        for index, part in enumerate(or_parts):
            clean_part = self.remove_outer_parentheses(part.strip())
            and_parts = self.split_top_level(clean_part, "AND")

            if len(and_parts) > 1:
                other_parts = or_parts[:index] + or_parts[index + 1:]
                distributed_clauses = []

                for and_part in and_parts:
                    new_or_parts = other_parts + [and_part.strip()]
                    new_clause = " OR ".join(
                        self.remove_outer_parentheses(p.strip()) for p in new_or_parts
                    )
                    distributed_clauses.extend(self.to_cnf(new_clause))

                return distributed_clauses

        return None

    def is_tautology(self, clause):
        """
        Check if a clause is always true.
        Example: A OR NOT A is a tautology.
        """
        literals = [literal.strip() for literal in clause.split(" OR ")]

        for literal in literals:
            opposite = self.get_opposite_literal(literal)
            if opposite in literals:
                return True

        return False

    def get_opposite_literal(self, literal):
        """
        Return the opposite of a literal.
        Example: A becomes NOT A, and NOT A becomes A.
        """
        literal = literal.strip()

        if literal.startswith("NOT "):
            return literal[4:].strip()

        return "NOT " + literal

    def get_cnf_beliefs(self):
        """Return all beliefs converted to CNF clauses."""
        cnf_beliefs = []

        for belief in self.beliefs:
            for clause in self.to_cnf(belief):
                if not self.is_tautology(clause):
                    cnf_beliefs.append(clause)

        return cnf_beliefs

    def show(self):
        """Display all beliefs"""
        print("Belief Base:")
        for b in self.beliefs:
            print(f"- {b} (priority {self.priority[b]})")

    #Contraction
    def contract(self, phi):
            from entailment import Entailment

            entailment = Entailment(self)

            # Vacuity
            if not entailment.entails(phi):
                return

            temp = BeliefBase()
            for b in self.beliefs:
                temp.add(b, self.priority[b])

            for belief in temp.get_sorted_beliefs():
                temp.remove(belief)

                if not Entailment(temp).entails(phi):
                    break

            self.beliefs = temp.beliefs
            self.priority = temp.priority

    def expand(self, phi, priority=1):
        """
        Expansion:
        B + phi = B union {phi}

        This only adds the new belief.
        It does not check consistency.
        It does not remove anything.
        """
        if not self.contains(phi):
            self.add(phi, priority) 