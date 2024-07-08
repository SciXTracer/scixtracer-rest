from fastapi import APIRouter
from fastapi import Response

import numpy as np
from PIL import Image
import io

import scixtracer as sx

router = APIRouter()


@router.get("/datasets/{uri}/data/{data_uri:path}")
async def read_data(uri: str, data_uri: str, convert: str = None):
    dataset = sx.get_dataset(sx.uri(uri))
    data_info = sx.get_data_info(dataset, sx.uri(data_uri))
    value = sx.read_data(data_info)
    return format_data(value, data_info.storage_type, convert)


def format_data(value: sx.DataInstance,
                data_type: sx.StorageTypes,
                convert: str = None):
    if data_type == sx.StorageTypes.ARRAY:
        return format_array(value, convert)
    elif data_type == sx.StorageTypes.TABLE:
        return format_table(value, convert)
    return value


def format_array(value: np.array, convert: str = None):
    if convert is None:
        return value.tolist()
    elif convert == "image":
        im = Image.fromarray(value)

        with io.BytesIO() as buf:
            im.save(buf, format='PNG')
            im_bytes = buf.getvalue()

        headers = {'Content-Disposition': 'inline; filename="test.png"'}
        return Response(im_bytes, headers=headers, media_type='image/png')


def format_table(value, convert):
    return value.to_dict()