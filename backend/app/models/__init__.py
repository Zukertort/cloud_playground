# in app/models/__init__.py

# Import all your models from their respective files.
# This makes them available under the `app.models` namespace.
from .user_model import User, UserCreate, UserPublic # Add any other user models
from .post_model import Post, PostCreate, PostPublic, PostPublicWithUser # Add any other post models

# Now that every model class has been imported and is defined,
# call model_rebuild() on all models that have forward references.
# This is the perfect place because the scope is guaranteed to contain
# all necessary model definitions.
User.model_rebuild()
Post.model_rebuild()
PostPublicWithUser.model_rebuild()

# Any other models with forward refs, e.g. a potential UserWithPosts
# UserWithPosts.model_rebuild()

# This is also a great place to define what is exported when someone
# does `from app.models import *`
__all__ = [
    "User",
    "UserCreate",
    "UserPublic",
    "Post",
    "PostCreate",
    "PostPublic",
    "PostPublicWithUser",
]