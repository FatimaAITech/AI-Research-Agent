from brain.parser import BrainParser
from tools.llm import llm

from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent

# from memory.history import ResearchHistory
from state.agent_state import AgentState
from brain.reasoning import AgentBrain
# from brain.parser import parse_decision
from brain.reflection import ReflectionAgent
from brain.self_correct import SelfCorrectAgent
from tools.tool_registry import ToolRegistry
from tools.tool_dispatcher import ToolDispatcher

from tools.planner_tool import PlannerTool
from tools.search_tool import SearchTool
from tools.writer_tool import WriterTool
from tools.review_tool import ReviewTool
from tools.self_correct_tool import SelfCorrectTool
from tools.memory_tool import MemoryTool
from tools.metrics import Metrics
from memory.memory_search import MemorySearch
from memory.semantic_memory import SemanticMemory
from memory.long_term_memory import LongTermMemory
from memory.consolidation import MemoryConsolidator
from memory.memory_analytics import MemoryAnalytics
from agents.agent_bus import AgentBus

from agents.planner_agent import PlannerAgent as PlannerWrapper
from agents.research_agent import ResearchAgent as ResearchWrapper
from agents.writer_agent import WriterAgent as WriterWrapper
from agents.critic_agent import CriticAgent
from agents.memory_agent import MemoryAgent
from brain.autonomous_orchestrator import AutonomousOrchestrator
from agents.execution_trace import ExecutionTrace
from memory.memory_reuse_decision import MemoryReuseDecision


class ResearchOrchestrator:

    def __init__(self):

        self.planner = PlannerAgent(llm)
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.reviewer = ReviewerAgent(llm)

        

        self.brain = AgentBrain()
        self.reflector = ReflectionAgent()
        self.self_corrector = SelfCorrectAgent()

        self.registry = ToolRegistry()

        self.register_tools()

        self.dispatcher = ToolDispatcher(
            self.registry
    )

        # ---------------------------------
# Multi-Agent Layer
# ---------------------------------

        self.bus = AgentBus()

        self.planner_agent = PlannerWrapper(
            self.planner
        )

        self.research_agent = ResearchWrapper(
            self.researcher
        )

        self.writer_agent = WriterWrapper(
            self.writer
        )

        self.critic_agent = CriticAgent(
            self.reviewer,
            self.reflector
        )

        self.memory_agent = MemoryAgent()

        self.trace = ExecutionTrace()

        self.autonomous = AutonomousOrchestrator(self)
        
        # print("\n========== REGISTERED TOOLS ==========\n")

        # for tool in self.registry.tool_info():
        #     print(tool)
#         self.actions = {

#               "PLAN": self.planner.run,

#               "SEARCH": self.researcher.run,

#               "WRITE": self.writer.run,

#               "REVIEW": self.reviewer.run,

#              "SELF_CORRECT": self.self_corrector.run
# }

        
# -----------------------------
# Tool Registry
# -----------------------------
    def register_tools(self):

        self.registry.register(
            PlannerTool(self.planner)
        )

        self.registry.register(
            SearchTool(self.researcher)
        )

        self.registry.register(
            WriterTool(self.writer)
        )

        self.registry.register(
            ReviewTool(self.reviewer)
        )

        self.registry.register(
            SelfCorrectTool(self.self_corrector)
        )

        self.registry.register(
            MemoryTool()
        )
 


# -----------------------------
# Tool Dispatcher
# -----------------------------

        # self.dispatcher = ToolDispatcher(
        #       self.registry
        #     )     
    def execute_action(self, action, state):

        action = action.upper()

    # ---------------------------------
    # Agent Mapping
    # ---------------------------------

        agent_map = {

            "PLAN": self.planner_agent,

            "SEARCH": self.research_agent,

            "WRITE": self.writer_agent,

            "REVIEW": self.critic_agent,

            "MEMORY": self.memory_agent,

        }

    # ---------------------------------
    # Unknown Action
    # ---------------------------------

        if action not in agent_map:

           print(f"\n❌ Unknown Action : {action}")

           return state

        agent = agent_map[action]

    # ---------------------------------
    # Start Trace
    # ---------------------------------

        trace = self.trace.start(agent.name)

        try:

            print(f"\n🤖 Executing {agent.name}...\n")

            self.bus.publish(
                 sender="Orchestrator",
                 receiver=agent.name,
                 message=f"Execute {action}"
            )

            state = agent.run(state)

            self.bus.publish(
                sender=agent.name,
                receiver="Orchestrator",
                message="Completed"
            )

            self.trace.end(
                trace,
                success=True
            )

            return state

        except Exception as e:

            self.trace.end(
                 trace,
                 success=False
            )

            print(f"\n❌ {agent.name} failed")

            print(e)

            raise
     
    def run(self, topic):

        print("\n========== ORCHESTRATOR STARTED ==========\n")

        state = AgentState(topic)

        self.state = state

        print("\n========== MEMORY SEARCH ==========\n")

# ----------------------------
# Memory Intelligence
# ----------------------------

        matches = SemanticMemory.search(topic)

# Fallback: String Similarity Memory

        if not matches:

            matches = MemorySearch.search(topic)


# ----------------------------
# Display Retrieved Memories
# ----------------------------

        if matches:

           print("🧠 Similar topics found:\n")

           for i, item in enumerate(matches, start=1):

                confidence = round(
                    item["score"] * 100
                )

                print(
                      f"{i}. {item['topic']} "
                      f"(Confidence: {confidence}%)"
                )

        else:

            print("🧠 No relevant memories found.")


# ----------------------------
# Memory Reuse Decision
# ----------------------------

        reuse_decision = MemoryReuseDecision.decide(
              matches
        )

        print(
              "\n========== MEMORY REUSE DECISION ==========\n"
        )

        print(
               f"Decision   : "
               f"{reuse_decision['decision']}"
        )

        print(
               f"Confidence : "
               f"{round(reuse_decision['confidence'] * 100)}%"
        )

        print(
               f"Reason     : "
               f"{reuse_decision['reason']}"
        )


# ----------------------------
# High-Confidence Memory Reuse
# ----------------------------

        if reuse_decision["decision"] == "REUSE":

            best_match = reuse_decision["memory"]

            print(
                  "\n🧠 High-confidence memory reuse approved."
            )

            print(
                   f"Topic      : {best_match['topic']}"
            )

            print(
                  f"Confidence : "
                  f"{round(reuse_decision['confidence'] * 100)}%"
            )

            LongTermMemory.touch(
                 best_match["topic"]
            )

            state = AgentState(topic)

            self.state = state

            state.final_report = best_match["report"]

            print(
                   "\n✅ Report loaded from semantic memory."
            )

            print(
                  "🧠 Long-Term Memory updated."
            )

            return state


# ---------------------------------
# NOW autonomous execution
# ---------------------------------

        print(
               "\n========== AUTONOMOUS PRE-PLANNING ==========\n"
        )

        self.autonomous.run(topic)

        print(
               "\n========== AUTONOMOUS PRE-PLANNING COMPLETED ==========\n"
        )

# ---------------------------------
# NOW autonomous execution
# ---------------------------------

        # print(
        #       "\n========== AUTONOMOUS PRE-PLANNING ==========\n"
        # )

        # self.autonomous.run(topic)

        # print(
        #       "\n========== AUTONOMOUS PRE-PLANNING COMPLETED ==========\n"
        # )

# Fallback: String Similarity Memory
    #     if not matches:
    #        matches = MemorySearch.search(topic)

    #     if matches:

    #        print("🧠 Similar topics found:\n")

    #        for i, item in enumerate(matches, start=1):

    #           confidence = round(item["score"] * 100)

    #           print(
    #                f"{i}. {item['topic']} "
    #                f"(Confidence: {confidence}%)"
    #           )

    #        print()

    #        best_match = matches[0]

    # # Smart reuse only for very high confidence
    #        if best_match["score"] >= 0.95:

    #         confidence = round(best_match["score"] * 100)

    #         print("\n🧠 Very similar research already exists.")
    #         print(f"Topic      : {best_match['topic']}")
    #         print(f"Confidence : {confidence}%")

    #         choice = input("\nReuse this report? (y/n): ").strip().lower()

    #         if choice in ["y", "yes"]:

    # # Update Long-Term Memory statistics
    #            LongTermMemory.touch(best_match["topic"])

    #            state = AgentState(topic)

    #            self.state = state

                

            
    # # Direct reuse from semantic memory
    #            state.final_report = best_match["report"]

    #            print("\n✅ Loaded report from semantic memory.")
    #            print("🧠 Long-Term Memory updated.")

    #            return state
                       
        # state = AgentState(topic)
    # -----------------------------
    # Planner
    # -----------------------------

        print("\n========== PLANNER ==========\n")

        state = self.execute_action(
             "PLAN",
             state
        )
        while not state.finished and state.iteration < state.max_iterations:

           print(f"\n========== ITERATION {state.iteration + 1} ==========\n")

           print("\n========== BRAIN ==========\n")

           brain_output = self.brain.think(
               goal=state.topic,
               context=f"""
           Plan:
           {state.plan}

           Research:
           {state.research}

           Report:
           {state.report}
           """
           )
     

           print(brain_output)

           decision = BrainParser.parse(brain_output)

           print("\n========== PARSED DECISION ==========\n")
           print(decision)

           action = decision["action"]

           if action == "FINISH":
  
             state.finished = True
             break

           state = self.execute_action(action, state)

          #  state.iteration += 1

           print("\n========== REFLECTION ==========\n")

           reflection = self.reflector.reflect(
              goal=state.topic,
              observation=state.report or state.research
)
          #  reflection = reflection.strip().upper()

           print(reflection)

           reflection_action = reflection.strip().upper()

           if reflection_action == "FINISH":

              print("✅ Reflection approved the report.")
              state.finished = True

           else:

              state = self.execute_action(
                   reflection_action,
                   state
               )

# Prevent infinite loop
           state.iteration += 1
 
    # -----------------------------
    # Save Memory
    # -----------------------------

        print("\n========== MEMORY ==========\n")

        state = self.execute_action(
            "MEMORY",
             state
        )

        # -----------------------------
        # Memory Consolidation
        # -----------------------------
        print("\n========== MEMORY CONSOLIDATION ==========\n")

        MemoryConsolidator.consolidate()

        print("✅ Memory consolidation completed.")


        print("\n========== TOOL METRICS ==========\n")

        for tool, info in Metrics.report().items():

            print(f"\n{tool}")
            print(f"Calls       : {info['calls']}")
            print(f"Success     : {info['success']}")
            print(f"Failures    : {info['failures']}")
            print(f"Average Time: {info['avg_time']}s")


# ---------------------------------
# Memory Analytics
# ---------------------------------

        MemoryAnalytics.report()


        return state
    