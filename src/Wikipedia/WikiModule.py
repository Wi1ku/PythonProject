import requests
import wikipedia


def get_page_list(query):
    if query is not None:
        try:
            pages = wikipedia.search(query=query, results=5)
            pages_w_summaries = []
            for page in pages:

                summary = wikipedia.summary(page, sentences=2)
                pages_w_summaries.append((page, summary))
        except requests.exceptions.ConnectionError:
            raise ConnectionError
        except wikipedia.exceptions.PageError:
            pass
        except wikipedia.exceptions.WikipediaException:
            return None
        return pages_w_summaries
    else:
        return None

