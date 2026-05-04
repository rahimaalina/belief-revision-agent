# Belief Revision Agent

This project implements the **belief base component** of a belief revision system for propositional logic.

## 📌 Overview

In artificial intelligence, a belief revision system is responsible for maintaining a consistent set of beliefs when new information is introduced.  

This repository currently implements the following stages of a belief revision system:

- Designing a belief base
- Storing logical formulas
- Managing priorities of beliefs
- Logical entailment using resolution

The system has been extended with a reasoning component that allows the agent to derive conclusions from the belief base.

---

## 🧠 What is a Belief Base?

A belief base is a collection of logical statements (beliefs) that an agent considers true.

Examples of beliefs:
- `A` → atomic proposition  
- `A -> B` → implication  
- `¬A` → negation  

The belief base acts as the **foundation** for reasoning and belief revision.

---

## ⚙️ Features

- Store propositional logic formulas  
- Assign priorities to beliefs  
- Add new beliefs  
- Remove existing beliefs  
- Display the belief base  

---

## 🔍 Logical Entailment

The system includes a logical entailment module that determines whether a given formula follows from the belief base.

The implementation is based on the **resolution method** for propositional logic.

### How it works

To check whether a belief base `B` entails a formula `φ`, the system:

1. Converts all formulas into Conjunctive Normal Form (CNF)
2. Adds the negation of the query `NOT φ`
3. Applies the resolution algorithm
4. Checks whether a contradiction (empty clause) is derived

If a contradiction is found, the query is entailed by the belief base.

### Supported logical transformations

- Implication elimination:  
  `A -> B` → `NOT A OR B`

- De Morgan’s laws:  
  `NOT (A AND B)` → `NOT A OR NOT B`  
  `NOT (A OR B)` → `NOT A AND NOT B`

- Double negation:  
  `NOT NOT A` → `A`

- Distribution:  
  `A OR (B AND C)` → `(A OR B) AND (A OR C)`

### Example

Given:

```
A
A -> B
```

Query:

```
B
```

Result:

```
True
```

---

⚠️ **Note**

The logical parser supports a restricted subset of propositional logic expressions and is designed for the scope of this project.

## Expansion

The system supports the expansion operation, which is used to add new information to the belief base.

### Definition

Expansion is defined as:
`B + φ = B ∪ {φ}`

This means that the new belief φ is simply added to the belief base without removing any existing beliefs.

### Implementation

Expansion is implemented through the expand() method in the belief base:

- Adds a new belief with an optional priority
- Does not check for consistency
- Does not modify existing beliefs

Internally, the method reuses the add() function.

### Example 
`bb = BeliefBase()`

`bb.add("A")`
`bb.add("A -> B")`

`bb.expand("B")`

`bb.show()`

Belief Base:
- `A`
- `A -> B`
- `B`

