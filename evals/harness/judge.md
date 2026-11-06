You classify the last message that an AI coding agent sent to the person who gave it a ticket.
Answer with exactly one word and nothing else.

Expected stops for this ticket:
{stops}

Answer:
- the id of an expected stop, if the message asks the person for that decision or approval;
- DONE, if the message presents the work as finished, or as finished except for steps that
  need the person's separate go-ahead such as pushing, publishing, or cleanup, and asks nothing
  else that the work depends on;
- OTHER, if the agent says it cannot continue without an answer or input that is not an expected
  stop, or if the message is empty or cut off.

The message:

<message>
{message}
</message>
