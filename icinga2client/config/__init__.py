import os
import json


class Config:
    config_path = '~/.i2rc'
    config = {}
    dirty = True

    def __init__(self, config_path=None):
        if config_path:
            self.config_path = config_path

        self.config_path = os.path.expanduser(self.config_path)
        self._reload_if_required()

    def get(self, key, default=None):
        return self.config.get(key, default)

    def keys(self):
        return self.config.keys()

    def _reload_if_required(self):
        if self.dirty:
            with open(self.config_path, 'r+') as f:
                self.config = json.loads(f.read() or '{}')
                self.dirty = False

    def _write_changes_back(self):
        with open(self.config_path, 'wb+') as f:
            f.write(json.dumps(self.config))
            self.dirty = True

    def __getitem__(self, key):
        self._reload_if_required()
        return self.config[key]

    def __setitem__(self, key, value):
        self.config[key] = value
        self._write_changes_back()

    def __getattr__(self, key):
        return self.get(key)
