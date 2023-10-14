from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    """
    Represents an access token used for authentication.

    Parameters
    ----------
    access_token : str
        The access token string.
    token_type : str
        The type of token (e.g. "bearer").
    
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


