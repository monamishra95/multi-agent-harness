# Adapter: Claude Fable 5 (adapter_version: fable-1.0)

Model-specific layer, loaded on top of any agent's core `agent.md` when running on Fable-class models. Sources: "Prompting Claude Fable 5" + "Building an ADE with Fable" guides (July 2026). Only Fable-specific behavior belongs here.

## Defaults

- Build mode: `one-shot`. Effort: high (xhigh for Verifier fact audits on T2).
- Dispatch parallel subagents freely for independent subtasks; prefer async check-ins over blocking on the slowest subagent; keep long-lived subagents alive across subtasks for cache reuse.

## Steering (include in system prompts)

- **Act, don't overplan:** "When you have enough information to act, act. Do not re-derive facts already established, re-litigate decided questions, or narrate options you will not pursue. If weighing a choice, give a recommendation, not a survey."
- **No unrequested scope (Builder especially):** "Don't add features, refactor, or introduce abstractions beyond what the task requires. Do the simplest thing that works well. Only validate at system boundaries."
- **Grounded progress:** "Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if not yet verified, say so explicitly."
- **Checkpoint policy:** "Pause for the user only when the work genuinely requires them: a destructive/irreversible action, a real scope change, or input only they can provide."
- **Autonomous runs:** append the anti-early-stopping reminder — "You are operating autonomously… before ending your turn, check your last paragraph; if it is a plan, a question, or a promise about undone work, do that work now with tool calls."
- **Self-verification interval (long builds):** "Establish a method for checking your own work as you build; run it at [interval], verifying against the specification with fresh subagents."

## Cautions

- Do NOT instruct Fable to echo or transcribe its reasoning in output — triggers `reasoning_extraction` refusals. Read thinking blocks instead if visibility is needed.
- Avoid surfacing context-budget countdowns; if unavoidable, add the ample-context reassurance.
- Skills/prompts written for older models are often too prescriptive for Fable and degrade output — when a core brain rule exists only to babysit a weaker model, flag it to Librarian for demotion rather than carrying it here.
