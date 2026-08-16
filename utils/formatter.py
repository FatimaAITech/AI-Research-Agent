class SearchFormatter:

    @staticmethod
    def format_results(search_results):

        formatted_text = ""

        results = search_results.get("results", [])

        for index, result in enumerate(results, start=1):

            title = result.get("title", "No Title")
            content = result.get("content", "No Content")
            url = result.get("url", "No URL")

            formatted_text += f"""
Result {index}

Title:
{title}

Content:
{content}

Source:
{url}

------------------------------------

"""

        return formatted_text