from services.research_service import ResearchService
from utils.file_handler import FileHandler


def main():
    try:
        # -------------------------------------------------
        # Research Service
        # -------------------------------------------------

        research_service = ResearchService()

        topic = input("Enter Research Topic: ").strip()

        # -------------------------------------------------
        # Validate user input
        # -------------------------------------------------

        if not topic:
            print("\n❌ Research topic cannot be empty.")
            return

        print("\n🚀 Starting AI Research Agent...\n")

        # -------------------------------------------------
        # Run research through Service Layer
        # -------------------------------------------------

        state = research_service.run(topic)

        # -------------------------------------------------
        # Get final report
        # -------------------------------------------------

        report = state.final_report or state.report

        if not report:
            print(
                "\n❌ Research completed but no report was generated."
            )
            return

        print("\n========== FINAL REPORT ==========\n")
        print(report)

        # -------------------------------------------------
        # Save report
        # -------------------------------------------------

        path = FileHandler.save_report(
            state.topic,
            report
        )

        print("\n✅ Report Saved Successfully!")
        print(f"Location: {path}")

    except KeyboardInterrupt:

        print("\n\n⚠️ Research cancelled by user.")

    except ValueError as e:

        print("\n❌ Invalid research request.")
        print(f"Error: {e}")

    except Exception as e:

        print("\n❌ Agent execution failed.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()