from strictyaml import Any, Map, MapPattern, Optional, Str


addon = Map(
    {
        "spec": Str(),
        Optional("install"): MapPattern(Str(), Any(), minimum_keys=1),
        "meta": Map({"name": Str(), "version": Str()}),
        Optional("config"): MapPattern(Str(), Any(), minimum_keys=1),
    }
)


application = Map(
    {
        "spec": Str(),
        Optional("meta"): Map(
            {Optional("name"): Str(), Optional("version"): Str()}
        ),
        Optional("services"): MapPattern(Str(), Map({"type": Str()})),
        Optional("addons"): MapPattern(
            Str(),
            Map(
                {
                    "manager": Str(),
                    "hash": Str(),
                    Optional("settings"): MapPattern(
                        Str(), Any(), minimum_keys=1
                    ),
                }
            ),
            minimum_keys=1,
        ),
        Optional("config"): MapPattern(Str(), Any(), minimum_keys=1),
    }
)
