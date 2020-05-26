import versions
reload(versions)

renamer = versions.MakeVersions()
renamer.versionUP("roboto", "A")