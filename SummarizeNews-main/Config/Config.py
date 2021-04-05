import logging
import os
import sys


class Config(object):
    DEFAULTS = {

        "LOGGING_LEVEL_CONSOLE": logging.INFO,
        "IP_CONNECTION_HOST": "localhost",  # IP Module address when using direct IP Connection
        "IP_CONNECTION_PORT": (
            5672,
            int,
            (1, 5673),
        ),
        "IP_CONNECTION_QUEUE_INGEST": (
            "news_ingest",
            [str, type(None)],
        ),
        "IP_CONNECTION_QUEUE_PROCESSED": (
            "news_processed",
            [str, type(None)],
        ),
        "IP_CONNECTION_USER": (
            "user",
            [str, type(None)],
        ),
        "IP_CONNECTION_PASSWORD": (
            "bitnami",
            [str, type(None)],
        ),
        "SUMMARIZE": (
            "http://localhost:5007/summarize",
            [str, type(None)],
        ),
        "SENTIMENT": (
            "http://localhost:5006/sentiment",
            [str, type(None)],
        ),
        "NER": (
            "http://localhost:5005/ner",
            [str, type(None)],
        ),
        "ELASTIC_INDEX": (
            "processed_news_final",
            [str, type(None)],
        ),
        "ELASTIC_IP": (
            "http://localhost:9200",
            [str, type(None)],
        )
    }

    CONFIG_LOADED = False
    CONFIG_FILE_LOCATION = (None,)

    def __dir__(self):
        return (
            list(self.DEFAULTS.keys())
            + list(self.__class__.__dict__)
            + dir(super(Config, self))
        )

    def load(self, alt_location=None):
        self.CONFIG_LOADED = False

        env_config_path = os.environ.get("PAI_CONFIG_FILE")

        if alt_location is not None:
            locations = [alt_location]
        elif env_config_path:
            locations = [env_config_path]
        else:
            filenames = ["/Folder/connector.conf"]
            locations = [
                os.path.join(dir, filename)
                for dir in [
                    os.path.realpath(os.getcwd())
                ]
                for filename in filenames
            ]

        for location in locations:
            location = os.path.expanduser(location)
            if os.path.exists(location) and os.path.isfile(location):
                self.CONFIG_FILE_LOCATION = location
                break
        else:
            err = f"ERROR: Could not find configuration file. Tried: {locations}"
            sys.stderr.write(err + "\n")
            raise (Exception(err))

        sys.stdout.write(
            "Attempting to load configuration from %s\n" % self.CONFIG_FILE_LOCATION
        )

        entries = {}
        conf_extension = os.path.splitext(self.CONFIG_FILE_LOCATION)[1]
        if conf_extension in [".conf", ".py"]:
            with open(self.CONFIG_FILE_LOCATION) as f:
                exec(f.read(), None, entries)
        elif conf_extension in [".json"]:
            import json

            with open(self.CONFIG_FILE_LOCATION) as f:
                entries = json.load(f)
        elif conf_extension in [".yaml"]:
            import yaml

            with open(self.CONFIG_FILE_LOCATION) as f:
                entries = yaml.safe_load(f)
        else:
            err = "ERROR: Unsupported configuration file type"
            sys.stderr.write(err + "\n")
            raise (Exception(err))

        # Updates values from env variables
        for args in os.environ:
            if not args.startswith("PAI_") or len(args) < 5:
                continue
            opt = args[4:]
            if opt in self.DEFAULTS:
                v = os.environ[args]
                if v.isdigit():
                    v = int(v)

                entries[opt] = v

        # Reset defaults
        for k, v in self.DEFAULTS.items():
            if isinstance(v, tuple):
                v = v[0]

            setattr(self, k, v)

        # Set values
        for k, v in entries.items():
            if k[0].isupper() and k in self.DEFAULTS:
                default = self.DEFAULTS.get(k)

                if isinstance(default, tuple) and 2 <= len(default) <= 3:
                    default_type = default[1]

                    if not isinstance(default_type, list):
                        default_type = [default_type]

                else:
                    default_type = [type(default)]

                if float in default_type and not int in default_type:
                    default_type.append(int)
                if int in default_type and not float in default_type:
                    default_type.append(float)

                if type(v) in default_type:
                    setattr(self, k, v)
                else:
                    err = "Error parsing configuration: Invalid value type {} for pai.conf argument {}. Allowed are: {}".format(
                        type(v), k, default_type
                    )
                    sys.stderr.write(err + "\n")
                    raise (Exception(err))

                if isinstance(default, tuple) and len(default) == 3:
                    expected_value = default[2]
                    valid = False

                    if isinstance(v, int):
                        if expected_value[0] <= v <= expected_value[1]:
                            valid = True
                    elif isinstance(v, str):
                        if v in expected_value:
                            valid = True
                    else:
                        valid = True

                    if valid:
                        setattr(self, k, v)
                    else:
                        err = "Error parsing configuration value: Invalid value for pai.conf argument {}. Allowed are: {}".format(
                            type(v), k, expected_value
                        )
                        sys.stderr.write(err + "\n")
                        raise (Exception(err))

        self.CONFIG_LOADED = True


config = Config()
config.load()
