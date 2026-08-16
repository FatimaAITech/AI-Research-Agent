class Metrics:

    _stats = {}

    @classmethod
    def record(cls, tool, success, execution_time):

        if tool not in cls._stats:

           cls._stats[tool] = {

                "calls": 0,

                "success": 0,

                "failures": 0,

                "total_time": 0
            }

        stat = cls._stats[tool]

        stat["calls"] += 1

        if success:

           stat["success"] += 1

        else:

           stat["failures"] += 1

        stat["total_time"] += execution_time

    @classmethod
    def report(cls):

        report = {}

        for tool, stat in cls._stats.items():

            avg = 0

            if stat["calls"] > 0:
                avg = stat["total_time"] / stat["calls"]

            report[tool] = {
                "calls": stat["calls"],
                "success": stat["success"],
                "failures": stat["failures"],
                "avg_time": round(avg, 2)
            }

        return report