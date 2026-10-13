import re
import sys

from cfabric.utils import files as cf_files
import cfabric.core.fabric as cf_fabric


_DRIVE_RE = re.compile(r"^[A-Za-z]:([/\\\\]|$)")


def patched_expand_dir(obj, dir_name):
    """Preserve absolute Windows paths instead of prefixing the current cwd."""
    normalized = cf_files.normpath(dir_name)

    if _DRIVE_RE.match(normalized) or normalized.startswith("//"):
        return normalized
    if normalized.startswith("~"):
        normalized = normalized.replace("~", obj.homeDir, 1)
    elif normalized.startswith(".."):
        normalized = normalized.replace("..", obj.parentDir, 1)
    elif normalized.startswith("./"):
        normalized = obj.curDir + normalized[1:]
    elif normalized == ".":
        normalized = obj.curDir
    elif not normalized.startswith("/"):
        normalized = obj.curDir + "/" + normalized

    return cf_files.normpath(normalized)


cf_files.expandDir = patched_expand_dir
cf_fabric.expandDir = patched_expand_dir


from cfabric_mcp.server import main


if __name__ == "__main__":
    sys.exit(main())
