from logging import info
import os


class PathManager:
    @staticmethod
    def create_out_put(tif: str, base: str = "./out"):
        dirs = tif.split("/")[1:]
        dirs_list = [base]
        dirs_list.extend(dirs[:-1])
        new_path = os.path.join(*dirs_list)
        info(f"new path has been created: {new_path}")
        tif_path = os.path.join(new_path, dirs[-1])
        # Check is path exist or not
        if os.path.exists(tif_path):
            return tif_path
        if os.path.isdir(new_path):
            return tif_path
        os.makedirs(new_path)
        return tif_path
