# Routing from retrieval output

The learner correctly described the warranty question taking fallback when retrieval returned an empty string and generation after they added the warranty document; the code contains that addition. They also correctly predicted that a nonempty irrelevant passage still reaches generation. This supports introducing a separate evidence-check node whose decision is stored in state and then used by the router.
