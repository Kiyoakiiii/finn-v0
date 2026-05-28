# Finn v0 - AI Wellness Bot

Finn is a small, runnable take-home prototype for fini's AI Agent Engineer internship assignment. It demonstrates how I would structure a first launch version of a wellness assistant that answers basic health and wellness questions, uses a small local knowledge base, handles out-of-scope or medical-risk requests safely, and leaves a clear path to scale.

The v0 is intentionally lightweight: it runs locally, uses no paid APIs, and keeps user data in local sample files. This makes the demo easy to review while still showing the core product and engineering decisions.

## Features

- Answers basic wellness questions using a local knowledge base.
- Personalizes responses with sample app data such as sleep average, stress level, hydration, activity level, and user goals.
- Routes urgent, diagnostic, medication, and unrelated questions to safer fallback responses.
- Shows source snippets from the knowledge base so the response is explainable.
- Includes tests for safety routing and core agent behavior.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local Streamlit URL printed in your terminal.

## Try These Prompts

```text
I have been sleeping around 5 hours. What can I do?
How can I feel less stressed at work?
How much water should I drink?
What is a simple way to start exercising again?
Should I take 10mg melatonin every night?
Can you diagnose my chest pain?
What stock should I buy today?
```

## Project Structure

```text
finn-v0/
  app.py
  requirements.txt
  README.md
  DESIGN.md
  data/
    knowledge_base.md
    sample_user_profile.json
  finn/
    agent.py
    retriever.py
    safety.py
    user_context.py
  tests/
    test_agent.py
    test_safety.py
```

## How Finn Works

```text
User message
  -> Safety router
  -> Knowledge base retriever
  -> User context builder
  -> Response composer
  -> UI response with source snippets
```

The first version uses deterministic retrieval and response composition instead of a hosted LLM. In a production version, the response composer can be replaced with an open-source LLM running behind a guarded API, while the safety router, context builder, and retrieval layer remain reusable.

## Privacy and Safety Choices

- Finn does not diagnose conditions, prescribe medication, or provide dosing advice.
- Urgent health or self-harm language is redirected to emergency resources.
- The sample user profile contains only minimal wellness context needed for personalization.
- The prototype avoids storing chat logs by default.
- Production data should be encrypted, access-controlled, audited, and retained only as long as needed.

## Future Scaling Path

- Replace the markdown knowledge base with a versioned content CMS plus embeddings in Chroma, Qdrant, Weaviate, or pgvector.
- Add app and wearable integrations with explicit user consent.
- Add user-controlled memory for goals, preferences, and check-ins.
- Add an LLM generation adapter using open-source models such as Llama, Mistral, or Phi via Ollama, vLLM, or llama.cpp.
- Add automated evals for source grounding, refusal quality, response tone, and privacy leakage.
- Add human escalation for clinical, crisis, or account-support workflows.

## Running Tests

```bash
pytest
```

## Notes

This is a v0 product prototype, not medical software. The goal is to show a practical structure for a safe wellness assistant that can launch quickly and evolve without throwing away the core architecture.
