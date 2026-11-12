"""Educational demo service. No brokerage orders are sent."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Stock Quant Trader - DEMO", version="0.1.0")
CANDIDATES = [
    {"code": "DEMO001", "name": "가상종목 A", "momentum": 90, "volume": 80, "trend": 85, "fundamental": 70, "safety": 75},
    {"code": "DEMO002", "name": "가상종목 B", "momentum": 77, "volume": 93, "trend": 78, "fundamental": 88, "safety": 82},
    {"code": "DEMO003", "name": "가상종목 C", "momentum": 65, "volume": 60, "trend": 72, "fundamental": 80, "safety": 45},
]
approved_codes: set[str] = set()
selection_mode = "approval"

def quant_score(stock: dict) -> float:
    return round(
        .30 * stock["momentum"] + .20 * stock["volume"] +
        .20 * stock["trend"] + .20 * stock["fundamental"] +
        .10 * stock["safety"], 2
    )

class ApproveRequest(BaseModel):
    codes: list[str] = Field(default_factory=list)
    mode: str = "approval"

@app.get("/health")
def health():
    return {"status": "ok", "service": "stock-quant-trader", "orders_enabled": False}

@app.get("/api/candidates")
def candidates():
    return sorted(
        [{**stock, "score": quant_score(stock)} for stock in CANDIDATES],
        key=lambda x: x["score"], reverse=True
    )

@app.post("/api/selection")
def select_stocks(req: ApproveRequest):
    global selection_mode
    if req.mode not in {"auto", "approval"}:
        raise HTTPException(status_code=400, detail="mode must be auto or approval")
    known_codes = {stock["code"] for stock in CANDIDATES}
    if req.mode == "auto":
        codes = {s["code"] for s in CANDIDATES if quant_score(s) >= 80}
    else:
        codes = set(req.codes)
        if not codes.issubset(known_codes):
            raise HTTPException(status_code=400, detail="unknown code")
    approved_codes.clear()
    approved_codes.update(codes)
    selection_mode = req.mode
    return {"mode": selection_mode, "selected_codes": sorted(approved_codes),
            "orders_enabled": False, "note": "demo selection only; never sends orders"}

@app.get("/api/selection")
def get_selection():
    return {"mode": selection_mode, "selected_codes": sorted(approved_codes),
            "orders_enabled": False}
