from prompts.review_prompt import review_prompt


class ReviewerAgent:

    def __init__(self, llm):
        self.llm = llm

    def review(self, report):

        print("\n📝 Reviewing Report...\n")

        prompt = review_prompt(report)

        response = self.llm.invoke(prompt)

        return response.content

    def run(self, state):

        print("\n✅ Reviewing Report...\n")

        review = self.review(state.report)

        state.review = review

        if review.startswith("APPROVED"):
            state.final_report = state.report
        else:
            state.final_report = None

        return state