# in app/models/__init__.py

# Import all models from their respective files.
# This makes them available under the `app.models` namespace.
from .user_model import User, UserCreate, UserPublic # Add any other user models
from .post_model import Post, PostCreate, PostPublic, PostPublicWithUser # Add any other post models
from .strategy_model import Strategy
from .trade_model import Trade

# Call model_rebuild() on all models that have forward references.
User.model_rebuild()
Post.model_rebuild()
PostPublicWithUser.model_rebuild()
Strategy.model_rebuild()
Trade.model_rebuild()

__all__ = [
    "User",
    "UserCreate",
    "UserPublic",
    "Post",
    "PostCreate",
    "PostPublic",
    "PostPublicWithUser",
    "Strategy",
    "Trade"
]