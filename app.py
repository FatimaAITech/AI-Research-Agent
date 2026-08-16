# from agents.orchestrator import ResearchOrchestrator
# from utils.file_handler import FileHandler


# def main():
#     orchestrator = ResearchOrchestrator()

#     topic = input("Enter Research Topic: ")

#     # Run complete AI Agent
#     state = orchestrator.run(topic)

#     # Get final report
#     report = state.final_report or state.report

#     print("\n========== FINAL REPORT ==========\n")
#     print(report)

#     # Save report once
#     path = FileHandler.save_report(
#         state.topic,
#         report
#     )

#     print("\n✅ Report Saved Successfully!")
#     print(f"Location: {path}")


# if __name__ == "__main__":
#     main()



from agents.orchestrator import ResearchOrchestrator
from utils.file_handler import FileHandler


def main():
    try:
        orchestrator = ResearchOrchestrator()

        topic = input("Enter Research Topic: ").strip()

        # Validate user input
        if not topic:
            print("\n❌ Research topic cannot be empty.")
            return

        print("\n🚀 Starting AI Research Agent...\n")

        # Run complete AI Agent
        state = orchestrator.run(topic)

        # Get final report
        report = state.final_report or state.report

        if not report:
            print("\n❌ Research completed but no report was generated.")
            return

        print("\n========== FINAL REPORT ==========\n")
        print(report)

        # Save report
        path = FileHandler.save_report(
            state.topic,
            report
        )

        print("\n✅ Report Saved Successfully!")
        print(f"Location: {path}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Research cancelled by user.")

    except Exception as e:
        print("\n❌ Agent execution failed.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()