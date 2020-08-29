from api.models.Map import WebMapRequestModel
from src.lib.Extractor import SingleLayer, S3MultiLayer
from src.lib.StorageManager import StorageManagement


class Map:
    @staticmethod
    async def request(request_model: WebMapRequestModel):
        results = []
        for layer in request_model.layer_list:
            result = await S3MultiLayer(
                request_model.coordinate.latitude,
                request_model.coordinate.longitude,
                layer.name,
                StorageManagement(),
            ).extract()
            results.append({"layer": layer.name, "result": result})
        return results

    @staticmethod
    async def valid_layers(base_name: str):
        pass