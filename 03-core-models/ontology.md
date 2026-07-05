---
title: Ontology
type: Foundation
status: Draft
version: 0.1
confidence: Medium
owner: David Wolfe / ChatGPT
updated: 2026-07-06
---

# Ontology

> "Before we can reason about the world, we must first decide what kinds of things exist."

---

# Purpose

This document defines the ontology of the Identity Operating System.

An ontology is not a philosophy.

It is not a design system.

It is not an implementation.

An ontology defines the fundamental kinds of entities that exist within our conceptual universe and the relationships between them.

Every model, design decision, engineering decision, AI behavior, and product feature should ultimately be explainable using the ontology defined here.

---

# Why Ontology Matters

Complex systems become coherent when they are built upon a consistent ontology.

Without one:

- concepts become overloaded
- terminology drifts
- different teams develop different mental models
- software reflects implementation details instead of reality

The purpose of this ontology is to provide a shared language for thinking.

---

# Our Objective

The Identity Operating System is not attempting to model all of reality.

It is attempting to model enough of reality to help humans better understand identity.

Our ontology should therefore contain the minimum number of concepts necessary to explain the domain.

Everything else should emerge from these concepts.

---

# Candidate Ontological Types

The current ontology consists of six kinds of things.

These are working models.

They should evolve as our understanding improves.

---

# 1. Objects

Objects are things that exist.

Objects have identity.

Objects possess properties.

Objects participate in relationships.

Examples:

- Person
- Identity
- Representation
- Evidence
- Organization
- Address
- Event

Question:

"What exists?"

---

# 2. Properties

Properties describe objects.

Properties do not exist independently.

They characterize objects.

Examples:

- Confidence
- Trust
- Freshness
- Accuracy
- Completeness
- Visibility

Question:

"What characteristics does this object possess?"

---

# 3. Relationships

Relationships connect objects.

Relationships create structure.

Relationships often provide more insight than objects alone.

Examples:

- Lives At
- Works For
- Parent Of
- Owns
- Connected To
- Represents

Question:

"How are these objects connected?"

---

# 4. Processes

Processes describe change.

Processes transform objects, properties, or relationships over time.

Examples:

- Understanding
- Learning
- Decision Making
- Monitoring
- Identity Resolution
- AI Reasoning

Question:

"What is happening?"

---

# 5. Dimensions

Dimensions provide context.

Dimensions are not objects.

They describe where or when objects and processes exist.

Examples:

- Time
- Location
- Context

Question:

"Under what conditions?"

---

# 6. Representations

Representations deserve special treatment.

A representation is itself an object.

However its purpose is unique.

Representations exist to help humans reason about reality.

Examples:

- Maps
- Identity Reports
- Timelines
- Dashboards
- Graphs
- AI Summaries

Representations connect reality with understanding.

---

# Initial Ontology

Reality
│
├── Objects
│
├── Properties
│
├── Relationships
│
├── Processes
│
├── Dimensions
│
└── Representations

---

# Identity Operating System

Our platform should reason about the world using these categories rather than through implementation details.

Example:

Instead of:

Address Table

Phone Table

Employment Table

The platform reasons about:

Objects

Relationships

Evidence

Properties

Processes

Representations

This distinction allows the architecture to evolve independently of storage.

---

# Evaluation

A proposed concept belongs in the ontology only if:

- It explains many downstream decisions.
- It cannot easily be derived from another concept.
- It remains useful independent of implementation.
- It improves reasoning across multiple domains.

If a concept only affects one screen or one feature, it probably does not belong in the ontology.

---

# Open Questions

Several important questions remain unresolved.

## Is Identity an object or a representation?

Current thinking:

Identity is an object whose purpose is to represent a person.

This distinction requires further exploration.

---

## Is Confidence a property of Evidence or Identity?

Current thinking:

Confidence may exist at multiple levels.

Further work required.

---

## Is Trust a property or an emergent process?

Current thinking:

Trust may be an emergent property resulting from accumulated evidence and consistent representations.

---

## Is Understanding a process or an outcome?

Current thinking:

Understanding may be the result of changes to a person's internal mental model rather than a process itself.

---

# Why This Matters

The ontology provides the intellectual foundation of the Identity Operating System.

Everything else—models, philosophy, design, engineering, AI, product, marketing, and implementation—should emerge from it.

A coherent ontology leads to coherent products.

A confused ontology inevitably produces confused software.
