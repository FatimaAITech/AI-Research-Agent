from tools.llm import ask
from prompts.writer_prompt import writer_prompt


class WriterAgent:

    def write(self, topic, plan, research):

        print("\n📝 Writing Professional Report...")

        prompt = writer_prompt(
            topic=topic,
            plan=plan,
            research=research
        )

        report = ask(prompt)

        return report
    
    def run(self, state):

        print("\n📝 Writing Report...\n")

        report = self.write(
            topic=state.topic,
            plan=state.plan,
            research=state.research
        )

        state.report = report
        state.final_report = report

        return state