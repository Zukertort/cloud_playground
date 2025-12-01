import xgboost as xgb
import os

class ModelLoader:
    def __init__(self, model_dir="../pipeline/data/models"):
        self.model_dir = model_dir
        self._cache = {} # Cache: a dict living in RAM

    def get_model(self, ticker):
        if ticker in self._cache:
            return self._cache[ticker]
        
        # Security check: prevent ".." directory traversal attacks
        safe_ticker = os.path.basename(ticker)
        model_path = os.path.join(self.model_dir, f"{safe_ticker}_xgb.json")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found {safe_ticker}")
        
        print(f"Loading model for {safe_ticker}...")
        model = xgb.XGBClassifier()
        model.load_model(model_path)

        self._cache[ticker] = model
        return model
    
# THE SINGLETON INSTANCE
# We create it once here. Everyone else imports this variable.
global_model_loader = ModelLoader()