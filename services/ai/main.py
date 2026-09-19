from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="BANOMA AI Service", version="0.1.0")


class RecommendRequest(BaseModel):
    talent_skills: List[str]
    opportunity_description: str


class RecommendResponse(BaseModel):
    score: float
    matched_skills: List[str]


class SummarizeRequest(BaseModel):
    text: str
    max_words: int = 60


class SummarizeResponse(BaseModel):
    summary: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    """Scoring simple par correspondance de mots-clés (baseline MVP).
    À remplacer par des embeddings (sentence-transformers) une fois le volume de données suffisant."""
    text = req.opportunity_description.lower()
    matched = [s for s in req.talent_skills if s.lower() in text]
    score = len(matched) / max(len(req.talent_skills), 1)
    return RecommendResponse(score=round(score, 2), matched_skills=matched)


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    """Résumé extractif basique (baseline MVP, à remplacer par un vrai modèle)."""
    words = req.text.split()
    summary = " ".join(words[: req.max_words])
    if len(words) > req.max_words:
        summary += "…"
    return SummarizeResponse(summary=summary)
