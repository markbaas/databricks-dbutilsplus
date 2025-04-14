from databricks.sdk import WorkspaceClient
import json
from ipywidgets.widgets import widget_string
from databricks.sdk._widgets.ipywidgets_utils import DbUtilsWidget

class Widgets:
    def __init__(self, _widgets):
        self._widgets = _widgets

    def _register(
        self,
        name,
        widget,
        label = None,
    ):
        label = label if label is not None else name
        w = DbUtilsWidget(label, widget)

        if name in self._widgets._widgets:
            self.remove(name)

        self._widgets._widgets[name] = w

    def _refreshParameters(self):
        with open('.params.json', 'r') as f:
            for k, v in json.load(f).items():
                self._register(k, widget_string.Text(v))

    def getAll(self):
        self._refreshParameters()
        return {x: y.value for x, y in self._widgets._widgets.items()}

    def getArgument(self, *args, **kwargs):
        self._refreshParameters()
        self._widgets.getArgument(*args, **kwargs)

    def get(self, *args, **kwargs):
        self._refreshParameters()
        self._widgets.get(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._widgets, name)



class DbUtils:
    def __init__(self):
        self.w = WorkspaceClient()
        self.widgets = Widgets(self.w.dbutils.widgets)

    def __getattr__(self, name):
        return getattr(self.w.dbutils, name)


dbutils = DbUtils()