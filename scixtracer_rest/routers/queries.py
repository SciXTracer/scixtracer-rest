from fastapi import APIRouter

import scixtracer as sx

router = APIRouter()


@router.get("/datasets/{uri}/annotations")
async def query_annotations(uri: str):
    dataset = sx.get_dataset(sx.uri(uri))
    loc_an = sx.query_location_annotation(dataset)
    data_ann = sx.query_data_annotation(dataset)
    return {"locations": loc_an, "data": data_ann}


@router.post("/datasets/{uri}/locations")
async def locations(uri: str, annotations: dict[str, str | float | int | bool]):
    dataset = sx.get_dataset(sx.uri(uri))
    locs = sx.query_location(dataset, annotations)
    out = []
    for loc in locs:
        out.append(loc.uuid)
    return out


@router.get("/datasets/{uri}/view_locations")
async def view_locations(uri: str):
    dataset = sx.get_dataset(sx.uri(uri))
    view = sx.view_locations(dataset)
    return view.to_dict('records')


@router.post("/datasets/{uri}/query_data")
async def query_data(uri: str,
                     annotations: dict[str, str | float | int | bool],
                     query_type: sx.DataQueryType = sx.DataQueryType.SINGLE):
    dataset = sx.get_dataset(sx.uri(uri))
    data_info = sx.query_data(dataset, annotations, query_type)
    return data_info


@router.post("/datasets/{uri}/query_data_at")
async def query_data(uri: str,
                     locations_id: list[int]):
    dataset = sx.get_dataset(sx.uri(uri))
    locations_in = []
    for location_id in locations_id:
        locations_in.append(sx.Location(dataset=dataset, uuid=location_id))
    data_info = sx.query_data_at(dataset, locations_in)
    return data_info
