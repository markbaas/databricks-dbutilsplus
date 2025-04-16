import json
import logging
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
from databricks.sdk import WorkspaceClient
from databricks.sdk._widgets.ipywidgets_utils import DbUtilsWidget
from databricks.sdk.dbutils import FileInfo
from ipywidgets.widgets import widget_string

w = WorkspaceClient()


class Widgets:
    def _register(self, name, widget, label=None):
        label = label if label is not None else name
        widget = DbUtilsWidget(label, widget)

        if name in w.dbutils.widgets._widgets:
            self.remove(name)

        w.dbutils.widgets._widgets[name] = widget

    def _refreshParameters(self):
        with open(".params.json", "r") as f:
            for k, v in json.load(f).items():
                self._register(k, widget_string.Text(v))

    def getAll(self):
        self._refreshParameters()
        return {x: y.value for x, y in w.dbutils.widgets._widgets.items()}

    def getArgument(self, *args, **kwargs):
        self._refreshParameters()
        w.dbutils.widgets.getArgument(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._refreshParameters()
        w.dbutils.widgets.get(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(w.dbutils.widgets, name)


class Credentials:
    def getServiceCredentialsProvider(self, *args, **kwargs):
        logging.warning(
            "getServiceCredentialsProvider is not supported remotely. Using DefaultAzureCredential instead."
        )
        return DefaultAzureCredential()

    def __getattr__(self, name):
        return getattr(w.dbutils.credentials, name)


class Fs:
    def _convert_abfss_to_adls_uri(self, abfss_uri):
        parts = abfss_uri.split("@")
        container = parts[0].replace("abfss://", "")
        account_name = parts[1].split(".")[0]
        path = "/".join(parts[1].split("/")[1:])
        return f"https://{account_name}.dfs.core.windows.net/", container, path

    def ls_adls(self, input_path):
        # Authenticate and list files
        adls_uri, container, path = self._convert_abfss_to_adls_uri(input_path)
        service_client = DataLakeServiceClient(
            account_url=adls_uri, credential=DefaultAzureCredential()
        )
        file_system_client = service_client.get_file_system_client(file_system=container)

        # List files
        paths = file_system_client.get_paths(path=path, recursive=False)
        for path in paths:
            yield FileInfo(
                path.name,
                Path(path.name).name,
                path.content_length,
                int(path.last_modified.timestamp() * 1000),
            )

    def ls(self, path):
        try:
            return w.dbutils.fs.ls(path)
        except Exception as e:
            if 'unsupported scheme "abfss"' in str(e):
                return self.ls_adls(path)
            else:
                raise e

    def __getattr__(self, name):
        return getattr(w.dbutils.fs, name)


class DbUtils:
    def __init__(self):
        self.widgets = Widgets()
        self.credentials = Credentials()
        self.fs = Fs()

    def __getattr__(self, name):
        return getattr(w.dbutils, name)


dbutils = DbUtils()
