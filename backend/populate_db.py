from services.rag import load_and_index_docs

if __name__ == "__main__":

    doc_path = "data/Indian-Accounting-Standards-IND-AS.pdf"

    load_and_index_docs(doc_path)
