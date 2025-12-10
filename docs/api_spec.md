# API Specification for Frontend

## Authentication
### POST /auth/token
- **Input:** `username`, `password`
- **Output:** `{ "access_token": "...", "token_type": "bearer" }`
- **Frontend Action:** Store token in `localStorage`.

## Dashboard Data (BFF Pattern)
### GET /dashboard/{ticker}
- **Auth:** Required (Bearer Token).
- **Response Structure:**
```json
{
  "ticker": "AAPL",
  "current_price": 150.50,
  "signal": "BUY",          // "BUY" | "IGNORE"
  "primary_signal": "BUY",  // Raw model output
  "meta_confidence": 0.83,  // Float 0-1
  "history": [
    { "timestamp": "2025-12-01T10:00:00", "close": 148.00 },
    { "timestamp": "2025-12-01T11:00:00", "close": 149.50 }
    // ... last 100 points
  ]
}