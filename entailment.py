class Entailment:
    def __init__(self, belief_base):
        self.bb = belief_base

    def entails(self, query):
        """
        Check if the belief base entails the query using resolution.
        We test whether belief base + NOT query creates a contradiction.
        """
        clauses = self.bb.get_cnf_beliefs()
        clauses.extend(self.negate(query))
        return self.resolution(clauses)

    def negate(self, formula):
        """Return the CNF clauses for the negation of a formula."""
        formula = formula.strip()

        if formula.startswith("NOT "):
            return self.bb.to_cnf(formula[4:].strip())

        return self.bb.to_cnf("NOT " + formula)

    def resolution(self, clauses):
        """
        Resolution algorithm.
        Returns True if contradiction is found, meaning the query is entailed.
        Returns False if no contradiction can be found.
        """
        clause_sets = [self.parse_clause(clause) for clause in clauses]

        while True:
            new_clauses = []

            for i in range(len(clause_sets)):
                for j in range(i + 1, len(clause_sets)):
                    resolvents = self.resolve_pair(clause_sets[i], clause_sets[j])

                    for resolvent in resolvents:
                        if resolvent == set():
                            return True

                        if resolvent not in clause_sets and resolvent not in new_clauses:
                            new_clauses.append(resolvent)

            if not new_clauses:
                return False

            clause_sets.extend(new_clauses)

    def parse_clause(self, clause):
        """
        Convert a clause string into a set of literals.
        Example: "NOT A OR B" becomes {"NOT A", "B"}.
        """
        parts = clause.split(" OR ")
        return set(part.strip() for part in parts)

    def resolve_pair(self, clause1, clause2):
        """
        Try to resolve two clauses.
        Returns a list of all possible resolvents.
        """
        resolvents = []

        for literal in clause1:
            opposite = self.bb.get_opposite_literal(literal)

            if opposite in clause2:
                resolvent = (clause1 - {literal}) | (clause2 - {opposite})

                if not self.bb.is_tautology(" OR ".join(resolvent) if resolvent else ""):
                    resolvents.append(resolvent)

        return resolvents