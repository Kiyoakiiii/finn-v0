# Finn v0 Design Doc

## Goal

Finn is fini's first-version AI wellness bot. The v0 should be useful for common wellness questions, safe around medical boundaries, explainable to users, and simple enough for the team to ship and learn from quickly.

The assignment asks for a 2-3 hour take-home, so this project optimizes for a clear architecture, runnable code, and realistic product tradeoffs rather than a large AI stack.

## Scope

Finn can answer basic wellness questions about:

- Sleep habits
- Hydration
- Stress management
- Movement and activity
- Nutrition basics
- Habit formation

Finn cannot:

- Diagnose symptoms
- Recommend medication or supplement dosage
- Replace a doctor, therapist, emergency service, or crisis line
- Answer unrelated questions such as investing, coding, or general trivia

## v0 Architecture

```text
Streamlit UI
  -> FinnAgent
      -> SafetyRouter
      -> LocalKnowledgeRetriever
      -> UserContext
      -> ResponseComposer
```

### 1. Safety Router

The safety router runs before retrieval. It catches:

- Emergency and crisis language
- Diagnostic requests
- Medication and dosage requests
- Clearly unrelated questions

This creates predictable behavior for high-risk cases before any generation step. In production, this should become a layered approach with rules, a classifier, red-team tests, and human escalation rules.

### 2. Knowledge Retriever

The v0 uses a local markdown knowledge base and a small lexical retriever. This keeps the prototype dependency-light and reviewable. The retriever returns the most relevant entries and source snippets.

Production path:

- Store approved wellness content in a CMS or database.
- Chunk and embed content.
- Use Chroma, Qdrant, Weaviate, or pgvector for retrieval.
- Track content versions so answers can be audited.

### 3. User Context

The sample app context includes:

- User goal
- Average sleep
- Stress level
- Hydration
- Activity level
- Preferences

Finn uses this context to make responses more relevant, but only within a wellness-support boundary. For example, Finn can say "since your average sleep is below your target..." but should not infer a diagnosis from that data.

Production path:

- Use explicit consent for each data source.
- Let users view, edit, export, and delete stored memory.
- Separate short-term session context from long-term profile context.
- Use data minimization: only store what helps the product.

### 4. Response Composer

The v0 response composer is deterministic. It combines:

- The top retrieved knowledge base entry
- A relevant personalization note
- One small next step
- A non-medical disclaimer
- Source titles

Production path:

- Add a model adapter around an open-source LLM.
- Ground generation in retrieved sources.
- Enforce a structured output schema.
- Run safety checks before and after model generation.

## Why Not Start With a Large Agent Framework?

For an initial launch, the biggest risks are trust, safety, correctness, and privacy. A smaller architecture is easier to evaluate and debug. Agent frameworks can be useful later for multi-step workflows, but v0 mostly needs retrieval, context, routing, and careful response generation.

## Open-Source Tooling Preference

Possible stack for a production-ready open-source path:

- UI: React Native, Expo, or web app frontend
- API: FastAPI
- Retrieval: Chroma, Qdrant, Weaviate, or pgvector
- Embeddings: sentence-transformers
- LLM serving: Ollama, vLLM, or llama.cpp
- Models: Llama, Mistral, Phi, or other appropriate open-weight model
- Observability: OpenTelemetry plus privacy-aware application logs
- Testing: pytest, promptfoo or custom eval harness

## Safety and Security

### User Safety

- Crisis and emergency messages should redirect to emergency services.
- Medication, supplement dosage, and diagnosis requests should be declined.
- Finn should use warm language without creating false authority.
- Every answer should stay grounded in approved wellness content.

### Data Security

Production controls should include:

- Encryption in transit and at rest
- Role-based access control for internal tools
- Audit logs for sensitive data access
- Short retention windows for raw chat logs
- Redaction of personal data in logs
- Secrets management for API keys
- Explicit consent before using wearable or third-party data
- User controls for deleting profile data

### Compliance Considerations

If Finn handles regulated health information, the team should evaluate HIPAA and other applicable requirements early. Even when the product is "wellness" rather than clinical care, users may share sensitive information, so the system should be designed as if privacy matters from day one.

## Evaluation Plan

I would evaluate Finn with a small test set before launch:

- In-scope answer quality: Does Finn answer common wellness questions clearly?
- Grounding: Are responses supported by the knowledge base?
- Refusals: Does Finn decline diagnosis, dosage, and unrelated questions?
- Crisis handling: Does Finn route emergency cases correctly?
- Personalization: Does Finn use app data helpfully without overreaching?
- Tone: Does Finn feel supportive and concise?
- Privacy: Does Finn avoid exposing or inventing sensitive data?

Example metrics:

- Retrieval hit rate
- Safe refusal accuracy
- Source-grounded answer rate
- User thumbs-up/down
- Escalation rate
- Reported confusion rate

## Future Roadmap

### Phase 1: Launchable v0

- Approved content library
- Safety router
- Retrieval-grounded responses
- Basic user context
- Simple feedback collection

### Phase 2: Context-Aware Finn

- Goal tracking
- Habit reminders
- Wearable integrations
- User-editable memory
- Personalized check-ins

### Phase 3: Scalable AI Platform

- Model adapter layer
- Vector database
- Eval pipeline
- Observability dashboard
- Human escalation and review tooling
- Internationalization and accessibility support

## Key Product Principle

Finn should feel helpful without pretending to be a clinician. The best v0 is not the most complex bot; it is the one users can trust, the team can debug, and the company can safely improve over time.
