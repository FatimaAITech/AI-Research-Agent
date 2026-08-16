from collections import defaultdict


class AgentBus:
    """
    Industry-Level Event Bus

    Responsible for

    • Agent Communication
    • Broadcast
    • Message Queue
    • Execution Events
    """

    def __init__(self):

        self.messages = defaultdict(list)

    # ---------------------------------
    # Send
    # ---------------------------------

    def publish(
        self,
        sender,
        receiver,
        message
    ):

        self.messages[receiver].append({

            "from": sender,

            "message": message

        })

    # ---------------------------------
    # Receive
    # ---------------------------------

    def consume(self, receiver):

        data = self.messages.get(receiver, [])

        self.messages[receiver] = []

        return data

    # ---------------------------------
    # Broadcast
    # ---------------------------------

    def broadcast(
        self,
        sender,
        message
    ):

        for receiver in self.messages.keys():

            self.publish(
                sender,
                receiver,
                message
            )

    # ---------------------------------
    # Pending
    # ---------------------------------

    def pending(self, receiver):

        return len(
            self.messages.get(receiver, [])
        )

    # ---------------------------------
    # Clear
    # ---------------------------------

    def clear(self):

        self.messages.clear()

    # ---------------------------------
    # Debug
    # ---------------------------------

    def stats(self):

        return {

            key: len(value)

            for key, value

            in self.messages.items()

        }