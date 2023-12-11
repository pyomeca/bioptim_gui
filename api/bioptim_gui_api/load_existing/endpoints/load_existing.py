import pickle as pkl
from typing import List

import numpy as np
from fastapi import UploadFile, APIRouter, HTTPException

from bioptim_gui_api.load_existing.endpoints.load_existing_responses import LoadExistingResponse

router = APIRouter(
    prefix="/load_existing",
    tags=["load_existing"],
    responses={404: {"description": "Not found"}},
)


async def handle_pkl(file: UploadFile) -> (bool, float):
    """
    Handle a pickle file to check if it has to be discarded by user and return discard choice and the cost of the
    solution

    A pickle file has to be discarded if the integrated states and the solution states diverge by more than 1 degree.

    Parameters
    ----------
    file: UploadFile
        The pickle file to handle

    Returns
    -------
    bool
        True if the pickle file has to be discarded, False otherwise
    float
        The cost of the solution

    Raises
    ------
    HTTPException
        If the file is not a pickle file
    HTTPException
        If the pickle file doesn't contain the right data (integrated_states and solution)
    """
    if file.content_type != "application/octet-stream":
        raise HTTPException(400, "File must be a pickle file")

    pickle_data = await file.read()
    loaded_data = pkl.loads(pickle_data)

    try:
        integrated_state = loaded_data["integrated_states"][-1]["q"][:, -1]
        sol_states = loaded_data["solution"].states[-1]["q"][:, -1]
    except KeyError:
        raise HTTPException(400, f"Pickle doesn't contain the right data")

    to_discard = False
    cost = loaded_data["solution"].cost

    if np.any(abs(integrated_state - sol_states) > np.deg2rad(1)):
        to_discard = True

    return to_discard, cost


@router.post("/load", response_model=LoadExistingResponse)
async def load_pickle(files: List[UploadFile] = []):
    """
    Load a pickles file and return the best one to use and the one to discard
    The pickles are received as a list of UploadFile, instead of a list of filepath, to allow the api to be hosted on a
    remote server.

    Parameters
    ----------
    files: List[UploadFile]
        The pickle files to load

    Returns
    -------
    LoadExistingResponse
        The best (lowest) cost pickle file to use and the one to discard
    """
    min_cost = float("inf")
    to_discard = []
    best = None

    for file in files:
        discard, cost = await handle_pkl(file)
        if discard:
            to_discard.append(file.filename)
        elif cost < min_cost:
            min_cost = cost
            best = file.filename

    return LoadExistingResponse(to_discard=to_discard, best=best)
