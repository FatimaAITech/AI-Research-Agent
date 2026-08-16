from tools.llm import ask


class SelfCorrectAgent:

    def correct(self, report, review):

        print("\n🔄 Self Correcting Report...\n")

        prompt = f"""
You are an Expert AI Research Editor.

You have:

1. Original Report

{report}

2. Review Feedback

{review}

Your task:

- Fix every issue mentioned in the review.
- Improve clarity.
- Improve structure.
- Improve grammar.
- Improve formatting.
- Keep all useful information.
- Add missing information if necessary.
- Return ONLY the improved report.

Do not explain anything.
"""


        improved_report = ask(prompt)

        return improved_report
    
    def run(self, state):

        print("\n🛠 Self Correcting...\n")

        improved_report = self.correct(
            report=state.report,
            review=state.review
    )

        state.report = improved_report
        state.final_report = improved_report

        return state