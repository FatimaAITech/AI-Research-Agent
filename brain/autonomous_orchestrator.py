from brain.goal_analyzer import GoalAnalyzer
from brain.decision_engine import DecisionEngine
from brain.task_generator import DynamicTaskGenerator
from brain.scheduler import AutonomousScheduler
from brain.retry_manager import RetryManager

# from agents.communication import AgentCommunication
from agents.parallel_executor import ParallelExecutor
from tools.metrics import Metrics
import time
from agents.execution_trace import ExecutionTrace



class AutonomousOrchestrator:
    """
    Production-Level Autonomous Orchestrator

    Pipeline

    Goal
        ↓
    Goal Analyzer
        ↓
    Decision Engine
        ↓
    Task Generator
        ↓
    Scheduler
        ↓
    Execute Tasks
    """

    def __init__(self, research_orchestrator):

        self.orchestrator = research_orchestrator

        self.scheduler = AutonomousScheduler()

        self.retry = RetryManager()

        # self.communication = AgentCommunication()

        self.parallel = ParallelExecutor()

        self.trace = ExecutionTrace()

    # ---------------------------------------------------
    # Execute
    # ---------------------------------------------------

    def run(self, topic):

        print("\n========== AUTONOMOUS ORCHESTRATOR ==========\n")

        # -----------------------------------------
        # Analyze Goal
        # -----------------------------------------

        analysis = GoalAnalyzer.analyze(topic)

        print("Goal Analysis")
        print("--------------------------------")

        print(f"Goal       : {analysis.goal}")
        print(f"Complexity : {analysis.complexity}")
        print(f"Research   : {analysis.requires_research}")
        print(f"Review     : {analysis.requires_review}")
        print(f"Memory     : {analysis.requires_memory}")

        # -----------------------------------------
        # Decision Engine
        # -----------------------------------------

        strategy = DecisionEngine.decide(topic)

        print("\nExecution Strategy")
        print("--------------------------------")

        for key, value in strategy.items():

            if key != "analysis":

                print(f"{key}: {value}")

        # -----------------------------------------
        # Generate Tasks
        # -----------------------------------------

        tasks = DynamicTaskGenerator.generate(
            analysis
        )

        print("\nGenerated Tasks")
        print("--------------------------------")

        for task in tasks:

            print(
                f"{task.id}. "
                f"{task.name} "
                f"→ {task.assigned_agent}"
            )

        # -----------------------------------------
        # Scheduler
        # -----------------------------------------

        if strategy["parallel_execution"]:

           print("\n⚡ Parallel Mode Enabled\n")

        else:

           print("\n➡ Sequential Mode Enabled\n")

        self.scheduler.load_tasks(tasks)

        print("\nStarting Execution...\n")

        # -----------------------------------------
# Execution Mode
# -----------------------------------------

        parallel_mode = strategy["parallel_execution"] 

        while self.scheduler.has_tasks():

            task = self.scheduler.pop() 

            if parallel_mode:

                print("⚡ Running in Parallel Mode")

            else:

               print("➡ Running in Sequential Mode")

            start = time.time()

            print(f"\n🚀 Executing Task: {task.name}")

            

            print(f"👤 Assigned Agent : {task.assigned_agent}")

            trace = self.trace.start(task.assigned_agent)

            start = time.time()

            try:

                self.orchestrator.bus.publish(
                    sender="Scheduler",
                    receiver=task.assigned_agent,
                    message=f"Execute Task: {task.name}"
                )

                agent_map = {

                    "PlannerAgent": "PLAN",
                    "ResearchAgent": "SEARCH",
                    "WriterAgent": "WRITE",
                    "CriticAgent": "REVIEW",
                    "MemoryAgent": "MEMORY"

                }

                action = agent_map.get(task.assigned_agent)

                if action:

                   self.orchestrator.execute_action(
                       action,
                       self.orchestrator.state
                    )

                Metrics.record(
                    tool=task.assigned_agent,
                    success=True,
                    execution_time=round(
                        time.time() - start,
                        3
                    )
                )

            except Exception as e:

                Metrics.record(
                    tool=task.assigned_agent,
                    success=False,
                    execution_time=round(
                       time.time() - start,
                       3
                    )
                )

                self.trace.end(trace, success=False)

                raise e

            elapsed = round(time.time() - start, 3)

            trace["execution_time"] = elapsed

            self.trace.end(trace, success=True)

        print("📋 Status : Planned")

        print("\n✅ Autonomous Planning Completed.\n")

        stats = self.scheduler.statistics()

        print("\nScheduler Stats")

        print("----------------")

        print(f"Remaining : {stats['remaining']}")

        print(f"Queued    : {stats['queued']}")

        self.trace.report()

        print("\n========== AUTONOMOUS EXECUTION SUMMARY ==========\n")

        stats = self.scheduler.statistics()

        print(f"Goal              : {topic}")

        print(f"Tasks Executed    : {len(tasks)}")

        print(f"Remaining Tasks   : {stats['remaining']}")

        print(f"Parallel Mode     : {parallel_mode}")

        print(f"Retry Enabled     : {strategy['retry_enabled']}")

        print(f"Memory Enabled    : {strategy['use_memory']}")

        print(f"Review Enabled    : {strategy['review_output']}")

        print("\n===============================================\n")

        return {

            "strategy": strategy,

            "analysis": analysis,

            "tasks": tasks,

            "scheduler": self.scheduler.statistics()

        }