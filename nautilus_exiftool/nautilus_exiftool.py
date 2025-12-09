try:
    from gi.repository import Nautilus as FileManager
except ImportError:
    try:
        from gi.repository import Caja as FileManager
    except ImportError as e:
        raise ImportError("can't import Nautilus/Caja file manager...") from e

import json
import subprocess
from urllib.parse import unquote

from gi.repository import Gio, GObject


class ExifToolPropertiesModelProvider(
    GObject.GObject, FileManager.PropertiesModelProvider
):
    def get_models(
        self, files: list[FileManager.FileInfo]
    ) -> list[FileManager.PropertiesModel]:
        if len(files) != 1:
            return []

        file = files[0]
        if file.get_uri_scheme() != "file" or file.is_directory():
            return []

        filename = unquote(file.get_uri()[7:]).encode("utf-8")

        model_list = Gio.ListStore.new(item_type=FileManager.PropertiesItem)

        results = subprocess.run(
            ["exiftool", "-json", filename], capture_output=True, text=True
        )
        data = json.loads(results.stdout)[0]

        # remove exif version
        data.pop("ExifToolVersion", None)

        for name, value in sorted(data.items(), key=lambda k: k[0].lower()):
            model_list.append(
                FileManager.PropertiesItem(name=name, value=value)
            )

        return [FileManager.PropertiesModel(title="Exif", model=model_list)]
