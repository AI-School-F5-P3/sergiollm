import arxiv

def fetch_arxiv_papers(query, max_results=5):
    """Busca artículos en arXiv basados en una consulta."""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id
        })
    return papers


if __name__ == "__main__":
    query = "inteligencia artificial"
    papers = fetch_arxiv_papers(query)
    for paper in papers:
        print(paper["title"], paper["url"])
