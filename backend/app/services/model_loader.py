import xgboost as xgb
import os
from app.settings import settings

class ModelLoader:
    def __init__(self, model_dir=settings.MODEL_DIR):
        self.model_dir = model_dir
        self._cache = {}
        print(f"DEBUG: ModelLoader initialized with dir: {self.model_dir}")

    def get_model(self, ticker):
        if ticker in self._cache:
            return self._cache[ticker]
        
        safe_ticker = os.path.basename(ticker)
        model_path = os.path.join(self.model_dir, f"{safe_ticker}_primary.json")
        meta_model_path = os.path.join(self.model_dir, f"{safe_ticker}_meta.json")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found {safe_ticker} at {model_path}")
        
        if not os.path.exists(meta_model_path):
            raise FileNotFoundError(f"Meta model not found {safe_ticker} at {meta_model_path}")
        
        print(f"Loading model for {safe_ticker}...")
        model = xgb.Booster()
        model.load_model(model_path)
        
        print(f"Loading meta model for {safe_ticker}...")
        meta_model = xgb.Booster()
        meta_model.load_model(meta_model_path)

        model_bundle = {"model": model, "meta_model": meta_model}
        self._cache[ticker] = model_bundle
        return model_bundle
    
global_model_loader = ModelLoader()