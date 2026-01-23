from common.errors.error_codes import ErrorCode
from common.errors.error_map import ERROR_MAP

missing = set(e.value for e in ErrorCode) - set(ERROR_MAP.keys())
if missing:
    raise RuntimeError(f"Missing error codes in ERROR_MAP: {missing}")
