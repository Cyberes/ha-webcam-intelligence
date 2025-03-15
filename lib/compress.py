from typing import Union

import base91
import brotli


def compress_to_base91(data: Union[str, bytes]) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')
    compressed = brotli.compress(data, quality=11)
    encoded = base91.encode(compressed)
    return encoded
