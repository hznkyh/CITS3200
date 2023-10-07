from typing import Annotated
from fastapi import Header, HTTPException


async def get_token_header(x_token: Annotated[str, Header()]):
    """
    Check if the provided X-Token header is valid.

    Parameters
    ----------
    x_token : str
        The value of the X-Token header.

    Raises
    ------
    HTTPException
        If the X-Token header is not equal to "fake-super-secret-token".

    Returns
    -------
    None
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
