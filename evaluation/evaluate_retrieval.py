# Retrieval Evaluation Helper
from src.retrieval.retrieve_history import HistoricalRetriever

if __name__ == '__main__':
    retriever = HistoricalRetriever()
    retriever.load_index()
    print('Retrieval vector index loaded successfully.')
