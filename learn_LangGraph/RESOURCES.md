# LangGraph and LangSmith Resources

## Knowledge

- [State updates and reducers](https://docs.langchain.com/oss/python/langgraph/graph-api#reducers)
  Official state update rules. Use for: Lesson 8’s replacement of passage, source, attempt count, and check result during a retrieval loop.

- [Trace LangGraph applications](https://docs.langchain.com/langsmith/trace-with-langgraph)
  Official tracing integration and trace viewer guide. Use for: enabling graph traces and inspecting node inputs and outputs.
- [Create an account and API key](https://docs.langchain.com/langsmith/create-account-api-key)
  Official key setup, endpoints, and workspace selection. Use for: configuring authentication for the learner's own tracing session.

- [Retrieval guide](https://docs.langchain.com/oss/python/deepagents/retrieval)
  Official guide to retrieving evidence for document questions. Use for: connecting retrieval and answer generation; defer advanced architectures until the basic workflow is understood.

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
  Official introduction to stateful workflow orchestration. Use for: understanding LangGraph's role and running a minimal graph.
- [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api)
  Official guide to state, nodes, edges, and graph execution. Use for: building and reasoning about a first workflow.
- [Conditional edges](https://docs.langchain.com/oss/python/langgraph/graph-api#conditional-edges)
  Official routing guide. Use for: Lessons 6–10's choice between generation, fallback, and a bounded retrieval retry; routers read updated state and return destinations.
- [LangSmith tracing quickstart](https://docs.langchain.com/langsmith/observability-quickstart)
  Official setup and tracing walkthrough with Python and TypeScript examples. Use for: inspecting inputs, outputs, and nested execution steps.

- [Evaluation types](https://docs.langchain.com/langsmith/evaluation-types)
  Official offline evaluation overview. Use for: checking saved cases against expected behavior in Lesson 18.
- [Code evaluators](https://docs.langchain.com/langsmith/code-evaluator-sdk)
  Official guide to scoring application outputs with code.

- [Build a knowledge base](https://docs.langchain.com/oss/python/langchain/knowledge-base)
  Official document-loading, splitting, and retrieval tutorial. Use for: Lessons 19–21, moving from local text files to retrieved context.

- [Gemini generateContent API](https://ai.google.dev/api/generate-content)
  Official Python text generation API. Use for: Lesson 23.
- [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)
  Free-tier model availability and pricing; keep billing disabled for these lessons.
- [LangSmith wrappers](https://reference.langchain.com/python/langsmith/wrappers)
  SDK wrapping, including wrap_gemini, for model tracing.

- [Define a code evaluator](https://docs.langchain.com/langsmith/code-evaluator-sdk)
  Official output-versus-reference evaluator guide. Use for: Lesson 24’s local workflow evaluation.

- [Inspect a trace](https://docs.langchain.com/langsmith/observability-quickstart#4-view-your-trace)
  Official node-tree and input/output inspection walkthrough. Use for: Lesson 26 project diagnosis.

## Wisdom (Communities)

- [LangChain Forum](https://forum.langchain.com/)
  Community linked from the official documentation. Use for: implementation questions and discussing practical workflow tradeoffs.

## Gaps

- Application: answering questions from documents. Learner reports beginner experience with prior exposure and prefers Python. Select a model integration when the first live generation exercise requires it.
