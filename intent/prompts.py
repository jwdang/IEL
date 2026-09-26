"""Prompt material for the intent system.

Scene background (an e-commerce customer-service dialogue) may appear, to help the LLM
understand the notion of a "business intent", but it must not be written as an exhaustive
candidate list -- a candidate list would anchor the taxonomy to the list rather than letting it
grow out of real dialogues. The rules themselves remain structural, and examples must be
explicitly marked "illustrative only, not exhaustive".
"""

DECOMPOSE_RULES = """\
You are processing an e-commerce customer-service dialogue between a buyer and a
service agent. A business intent is a concrete request that the buyer wants the
agent to help complete, such as returning an item or changing a delivery address.

Decompose the user message into atomic business intents. Follow these rules:

1. One intent = one independently closable business goal. The test: it could stand
   as a ticket on its own, and it has its own terminal criterion.
2. An intent id has the form `object.action`: object is the business object this
   request acts on, action is what is done to it. The wording is yours to choose,
   but the same meaning must always reuse the same wording.
3. A slot is a parameter difference within one intent: the key is a parameter name,
   the value is what is extracted from the message, and it distinguishes handling
   branches without changing the tool sequence. To tell a new intent from a slot,
   ask whether the tool sequence changes:
   - changes which tools are called, or their order -> possibly a new intent
   - changes only tool arguments, call count, or a trigger condition -> a slot
4. If an item cannot be named without ambiguity, emit no intent for it and place it
   under non_transactional.
5. Reuse slots first: when the target intent already has a slot schema, prefer the
   keys and values already in it; when a genuinely new one is needed, emit it as usual.
6. Put an item in matched only when it is a certain match: the message contains text
   that directly supports it (a span you can fill in), it satisfies the intent's
   discriminators (if the taxonomy gives any), and it triggers none of the intent's
   negative_triggers. Anything that merely seems related, needs context you have to
   infer, or only holds under your own guess is not a match.
7. matched may be empty -- a turn with no certain match is a perfectly normal result.
   It may also contain several items -- one message can certainly match several
   intents at once. Do not stuff an uncertain match into matched just to fill it in,
   and do not move it into candidates either: candidates exist only to propose a
   genuinely new intent absent from the taxonomy, which is a different thing from
   "I am not sure about this existing intent". When you cannot tell, emit nothing
   rather than guess.
8. Every item in matched is used directly to look up and inject the corresponding
   handling experience for the service agent.
"""

DECOMPOSE_EXAMPLES = """\
Example A (one message containing several intents)
Message: "Please change my delivery address, and I'd also like to book an
installation service, order number 1234567890."
Emit two intents: `order.change_address` (change the address) and
`service.schedule_install` (book installation). They use different tools, and their
terminal criteria are independent of each other.

Example B (a modifier should be demoted to a slot, not made a new intent)
Message: "Change all three of these orders to expedited."
"Three" changes only how many times the same tool is called, not which tools are
called -> it is a slot, not a new "batch expedite" intent. Emit matched:
`order.expedite`, with slots `{"batch": "3"}`.

Message: "This garment has a quality problem, I want to return it."
Emit matched: `order.return`, with slots `{"reason": "quality problem"}`.

Example C (pure emotion emits no intent)
Message: "You people are so slow!"
There is no independently closable business goal -> put it under
non_transactional, and emit no intent.

Example D (vaguely related, but not enough evidence to be a certain match)
Message: "Isn't this a bit expensive? I should have waited for a sale."
The buyer is only expressing that the price feels high and that they bought too
early; there is no specific, actionable request such as "check for a coupon" or
"request a price guarantee", and no text that maps directly onto an existing
intent. In this case do not put it in matched, and do not push it into candidates
just to avoid coming back empty-handed either; if no clearer request can be found,
put it under non_transactional.
"""

DECOMPOSE_OUTPUT_SCHEMA = """\
Output JSON only, in this format:
{
  "matched": [
    {"id": "an intent id that already exists in the taxonomy",
     "slots": {"key": "value"},
     "span": "the verbatim span of the user message it comes from"}
  ],
  "candidates": [
    {"proposed_id": "object.action", "desc": "one-sentence description of this intent",
     "slots": {"key": "value"}, "span": "the verbatim span of the user message"}
  ],
  "non_transactional": ["description of a span that yielded no intent"]
}
matched may contain only ids that already exist in the taxonomy and that you are
certain about; anything absent from the taxonomy goes in candidates; anything you
are unsure about goes in neither list.
"""

ADJUDICATE_INTENT_RULES = """\
You are resolving, in an e-commerce customer-service setting, whether a candidate
intent should enter the taxonomy: the candidate comes from a buyer message, and the
question is whether it is a new request, distinct from the existing intents, that
the buyer wants the agent to complete.
There are three outlets:

- merge: no observable discriminating question can be asked against some neighbour
  intent -> fold it into that neighbour
- slot: the difference affects only tool arguments, call count, or a trigger
  condition -> make it a slot value on that neighbour
- new: the difference changes the tool sequence, and a discriminating question can
  be asked against every neighbour -> add a new intent

Every discriminating question must be answerable directly from dialogue content.
The default outlet is slot: choose new only when the tool sequence really changes.

Also decide: must this intent make one change to system state (create, modify,
cancel, submit, ...) in order to be complete? If it only retrieves information and
changes no state, answer false. When you cannot determine it, omit the field rather
than guess.
"""

ADJUDICATE_SLOT_RULES = """\
You are resolving, in an e-commerce customer-service setting, whether a candidate
slot should enter the target intent's schema: the question is whether this value is
a difference that genuinely affects how the agent handles the request.
There are two outlets:

- accept: this key/value really does distinguish different handling paths within
  the same intent
- reject: it is semantically duplicate with an existing key, or affects no handling
  difference, or is not part of a business intent relevant to the e-commerce setting

When rejecting because it is synonymous with an existing key, give the existing key
it should map to in the map_to field.
"""

DISTILL_RULES = """\
You distill experience for an e-commerce customer-service setting from several
execution trajectories of the same business intent, for the service agent to consult
when handling buyer requests. The input is a set of instances, each with its tool
sequence and its outcome.

The output must use one skill structure with progressive disclosure, in two parts:

1. The first line must be exactly `description: <one-sentence summary>`: it
   summarizes the handling path this experience covers. This line is the summary the
   taxonomy can see at matching time; the body below it is loaded in full only after
   this intent is matched, so do not write a description that only makes sense after
   reading the body.
2. After one blank line comes Markdown using only the following level-two headings,
   omitting any section that would be empty rather than leaving a bare heading:
   - `## Applicable scenarios`: one or two sentences describing the triggers or the
     typical user expressions.
   - `## Handling steps`: use the longest common subsequence of tool names across
     the successful instances as the backbone; express the differences as optional
     branches with their trigger conditions.
   - `## Common errors`: include only when both successful and failed instances
     exist; locate the divergence at a concrete step and state what omitting it
     causes to fail.

Do not invent experience when only failed instances exist; return empty. Tool names
must exactly match those observed in the input, never invent tools. The experience
must be quickly scannable, and must not restate anything that does not help
execution.
"""
