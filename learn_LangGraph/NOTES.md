# Teaching preferences

- Use Python for runnable LangGraph and LangSmith examples.
- Learner describes themselves as a beginner with prior exposure to these topics.
- Explain state propagation with numbered before-and-after examples; the learner requested a clearer explanation of Lesson 02's initial recall question.

- Prefer a small results table plus one focused question at the end of lessons; avoid long fill-in-the-blank narrative recaps. Learner selected this format after Lesson 12.
- Lesson 13 saves responses directly into `lessons/0013-retry-the-draft.html`, in the JSON script with id `saved-lesson-answers`. When asked to check saved answers, read that block and compare with the runnable example. Earlier text exports may still exist, but prefer the embedded responses when available.

- Use Gemini’s free tier for live-model lessons and the final project; the learner does not want to purchase OpenAI API credits. Save GEMINI_API_KEY once in the project .env and keep billing disabled.

- Final project starts in Lesson 25 using fictional shop policies, as selected by the learner. Lesson 26 diagnoses project cases in LangSmith; Lesson 27 adds a simple interface.

- Lessons 26 and 27 are created; learner has not submitted their answers yet. Lesson 27 adds a terminal chat interface, with fixtures by default and explicit --live for Gemini. Do not infer completion from lesson creation.
