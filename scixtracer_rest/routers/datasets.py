from fastapi import APIRouter

import scixtracer as sx

router = APIRouter()


@router.get("/datasets")
async def datasets():
    value = sx.datasets()
    return value.to_dict('records')


@router.get("/datasets/{uri}")
async def datasets(uri: str):
    dataset = sx.get_dataset(sx.uri(uri))
    return dataset
