I ran Claude Opus 5 and Sonnet 5 through the exact same coding task to see what the new flagship model actually buys you over the current default.

The task: implement is_balanced(s), a function that checks whether parentheses, brackets, and braces in a string are correctly matched and nested — plus a self-test covering edge cases, executed to confirm every assertion actually passes. Same prompt, same constraints, independently verified afterward rather than just trusting each model's own report.

Both delivered a correct, working solution on the first try. Where they diverged: Opus 5 wrote 50% more test coverage than I asked for, but took 77% longer and cost 51% more to get there.

My early read: for small, well-scoped work, Sonnet 5 stays the better default. Opus 5's extra depth should start earning its cost on harder, multi-step problems — that's what I'm testing next, with real tasks pulled from Korrin and LocalLab.

Full breakdown in the chart below.
