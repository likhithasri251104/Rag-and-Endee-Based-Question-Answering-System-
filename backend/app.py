from fastapi import FastAPI, HTTPException
from backend.agent import agent_answer

app = FastAPI()

@app.get("/ask")
def ask(question: str):
    try:
        answer = agent_answer(question)
        return {
            "question": question,
            "answer": answer
        }
    except ConnectionError as e:
        raise HTTPException(
            status_code=503,
            detail="Endee database is not reachable. Ensure Docker is running: docker-compose up -d"
        ) from e
    except RuntimeError as e:
        if "Endee" in str(e) or "search failed" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail=f"Database error: {e}. Ensure Endee is running and documents are ingested."
            ) from e
        raise HTTPException(status_code=500, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        ) from e
