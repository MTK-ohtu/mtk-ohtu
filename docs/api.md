# API definition


## API1

## API2

## API3
The API for getting basic info about the available logistics contractors for a delivery between a customer and a sidestream source.

Info supplied to the API:
* ID of the listing / posting / item / sidestream source / etc.
* Address of the user

Info supplied by the API to the caller:
* The distance between the supplied address and the location of the listing
* The number of available logistics contractors
* The link to the logistics page with more info

#### Technical specification
API endpoint: `/api/logistics_info`

HTTP method: `GET`

MIME type: `application/json`

Expected request JSON:
```json
{
    "listing": int (ID),
    "location": str (address)
}
```
Returned JSON:
```json
{
    "distance": (float) in kilometers,
    "num_providers": (int),
    "link": (str) a full URL, not relative
}
```

Flask route: [api/routes.py](../src/mtk_ohtu/api/routes.py)