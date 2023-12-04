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
    if file.content_type != "application/octet-stream":
        raise HTTPException(400, "File must be a pickle file")

    pickle_data = await file.read()
    loaded_data = pkl.loads(pickle_data)

    integrated_state = loaded_data["integrated_states"][-1]["q"][:, -1]
    sol_states = loaded_data["solution"].states[-1]["q"][:, -1]

    to_discard = False
    cost = loaded_data["solution"].cost

    if np.any(abs(integrated_state - sol_states) > np.deg2rad(1)):
        to_discard = True

    return to_discard, cost


@router.post("/load", response_model=LoadExistingResponse)
async def load_pickle(files: List[UploadFile] = []):
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
