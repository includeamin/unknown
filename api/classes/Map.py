from api.models.Map import WebMapRequestModel
from src.lib.Extractor import SingleLayer, S3MultiLayer
from src.lib.StorageManager import StorageManagement
from api.classes.LayerManager import LayerManger
from api.settings import storage_settings


class Map:
    @staticmethod
    async def request(request_model: WebMapRequestModel):
        results = []
        file_names = await LayerManger.Shared.get_layers_file_names(
            request_model.layer_list
        )
        storage = StorageManagement(layer_bucket=storage_settings.LAYER_BUCKET)
        for layer in file_names:
            storage.apply_forced_path(layer.file_name)
            try:
                result = (
                    await SingleLayer(
                        request_model.coordinate.latitude,
                        request_model.coordinate.longitude,
                        storage.get_storage_path(),
                    )
                    .apply_s3(storage)
                    .s3_extractor()
                )
                result.layer = None
                results.append({"layer": layer.code, "result": result})
            except (ValueError, IndexError) as ex:
                error = ""
                if isinstance(ex, IndexError):
                    error = "out of range"
                elif isinstance(ex, ValueError):
                    error = "no-data"
                results.append({"layer": layer.code, "result": error})

        return results
