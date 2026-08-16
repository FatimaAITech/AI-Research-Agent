import uuid
from datetime import datetime


class ExecutionTrace:
    """
    Industry-Level Execution Trace

    Tracks:
    - Trace ID
    - Action
    - Agent
    - Status
    - Start Time
    - End Time
    - Duration
    - Retry Count
    - Error
    """

    def __init__(self):

        self.records = []

    # ---------------------------------
    # Start Trace
    # ---------------------------------

    def start(self, action, agent=None):

        trace = {

            "trace_id": str(uuid.uuid4()),

            "action": action,

            "agent": agent or action,

            "status": "RUNNING",

            "start": datetime.now(),

            "end": None,

            "duration": None,

            "retry_count": 0,

            "error": None

        }

        return trace

    # ---------------------------------
    # Success
    # ---------------------------------

    def success(self, trace):

        self.end(trace, success=True)

    # ---------------------------------
    # Fail
    # ---------------------------------

    def fail(self, trace, error):

        trace["error"] = error

        self.end(trace, success=False)

    # ---------------------------------
    # End Trace
    # ---------------------------------

    def end(self, trace, success=True):

        end_time = datetime.now()

        trace["end"] = end_time

        trace["duration"] = round(

            (end_time - trace["start"]).total_seconds(),

            3

        )

        trace["status"] = (

            "SUCCESS"

            if success

            else "FAILED"

        )

        self.records.append(trace)

    # ---------------------------------
    # Report
    # ---------------------------------

    def report(self):

        print("\n========== EXECUTION TRACE ==========\n")

        if not self.records:

            print("No execution records found.\n")

            return

        for record in self.records:

            print(f"Trace ID : {record['trace_id']}")

            print(f"Action   : {record['action']}")

            print(f"Agent    : {record['agent']}")

            print(f"Status   : {record['status']}")

            print(f"Duration : {record['duration']} sec")

            print(f"Retries  : {record['retry_count']}")

            print(f"Error    : {record['error']}")

            print("-" * 50)

    # ---------------------------------
    # Clear
    # ---------------------------------

    def clear(self):

        self.records.clear()