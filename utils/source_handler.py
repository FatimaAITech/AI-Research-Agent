class SourceHandler:

    @staticmethod
    def get_sources(search_results):

        sources = []

        results = search_results.get("results", [])

        for result in results:

            url = result.get("url")

            if url:
                sources.append(url)

        return sources