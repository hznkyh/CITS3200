from pydantic import BaseModel

class User(BaseModel):
    """
    A class representing a user.

    Parameters
    ----------
    uuid : str
        The unique identifier for the user.
    """
    uuid: str

