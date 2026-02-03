from common.errors.error_codes import ErrorCode

# sorted by ascending HTTP status code
ERROR_MAP = {
    # === 400 BAD REQUEST ===
    ErrorCode.INVALID_PARAMETER.value: {
        "status": 400,
        "code": "InvalidParameter",
        "message": "Invalid request parameter",
    },
    ErrorCode.VALIDATION_FAILED.value: {
        "status": 400,
        "code": "ValidationFailed",
        "message": "Validation failed",
    },
    ErrorCode.MISSING_REQUIRED_FIELD.value: {
        "status": 400,
        "code": "MissingRequiredField",
        "message": "Required field is missing",
    },
    ErrorCode.PASSWORD_TOO_SHORT.value: {
        "status": 400,
        "code": "PasswordTooShort",
        "message": "Password is too short",
    },
    ErrorCode.PASSWORD_POLICY_VIOLATION.value: {
        "status": 400,
        "code": "PasswordPolicyViolation",
        "message": "Password does not satisfy security policy",
    },
    ErrorCode.GOOGLE_AUTH_CODE_MISSING.value: {
        "status": 400,
        "code": "GoogleAuthCodeMissing",
        "message": "Google authorization code is missing",
    },
    # === 401 UNAUTHORIZED ===
    ErrorCode.INVALID_CREDENTIALS.value: {
        "status": 401,
        "code": "InvalidCredentials",
        "message": "Invalid email or password",
    },
    ErrorCode.UNAUTHORIZED.value: {
        "status": 401,
        "code": "Unauthorized",
        "message": "Unauthorized",
    },
    ErrorCode.TOKEN_INVALID.value: {
        "status": 401,
        "code": "InvalidToken",
        "message": "Invalid token",
    },
    ErrorCode.TOKEN_EXPIRED.value: {
        "status": 401,
        "code": "TokenExpired",
        "message": "Token expired",
    },
    ErrorCode.REFRESH_TOKEN_MISSING.value: {
        "status": 401,
        "code": "RefreshTokenMissing",
        "message": "Refresh token is missing",
    },
    ErrorCode.REFRESH_TOKEN_INVALID.value: {
        "status": 401,
        "code": "RefreshTokenInvalid",
        "message": "Invalid refresh token",
    },
    ErrorCode.GOOGLE_AUTH_FAILED.value: {
        "status": 401,
        "code": "GoogleAuthFailed",
        "message": "Google authentication failed",
    },
    # === 403 FORBIDDEN ===
    ErrorCode.FORBIDDEN.value: {
        "status": 403,
        "code": "Forbidden",
        "message": "Access is forbidden",
    },
    ErrorCode.ACCESS_DENIED.value: {
        "status": 403,
        "code": "AccessDenied",
        "message": "You do not have permission",
    },
    ErrorCode.USER_BLOCKED.value: {
        "status": 403,
        "code": "UserBlocked",
        "message": "User is blocked",
    },
    ErrorCode.USER_SUSPENDED.value: {
        "status": 403,
        "code": "UserSuspended",
        "message": "User is suspended",
    },
    ErrorCode.USER_DELETED.value: {
        "status": 403,
        "code": "UserDeleted",
        "message": "User account is deleted",
    },
    # === 404 NOT FOUND ===
    ErrorCode.DATA_NOT_FOUND.value: {
        "status": 404,
        "code": "DataNotFound",
        "message": "Requested resource not found",
    },
    ErrorCode.USER_NOT_FOUND.value: {
        "status": 404,
        "code": "UserNotFound",
        "message": "User not found",
    },
    ErrorCode.FILE_NOT_FOUND.value: {
        "status": 404,
        "code": "FileNotFound",
        "message": "File not found",
    },
    ErrorCode.USER_CALENDAR_NOT_FOUND.value: {
        "status": 404,
        "code": "UserCalendarNotFound",
        "message": "User Calendar is not found",
    },
    # === 405 METHOD NOT ALLOWED ===
    ErrorCode.METHOD_NOT_ALLOWED.value: {
        "status": 405,
        "code": "MethodNotAllowed",
        "message": "HTTP method not allowed",
    },
    # === 409 CONFLICT ===
    ErrorCode.DUPLICATE_ENTRY.value: {
        "status": 409,
        "code": "DuplicateEntry",
        "message": "Resource already exists",
    },
    ErrorCode.DATA_INTEGRITY_VIOLATION.value: {
        "status": 409,
        "code": "DataIntegrityViolation",
        "message": "Data integrity violation",
    },
    # === 413 PAYLOAD TOO LARGE ===
    ErrorCode.FILE_TOO_LARGE.value: {
        "status": 413,
        "code": "FileTooLarge",
        "message": "Uploaded file is too large",
    },
    # === 415 UNSUPPORTED MEDIA TYPE ===
    ErrorCode.UNSUPPORTED_MEDIA_TYPE.value: {
        "status": 415,
        "code": "UnsupportedMediaType",
        "message": "Unsupported media type",
    },
    # === 500 INTERNAL SERVER ERROR ===
    ErrorCode.FILE_UPLOAD_FAILED.value: {
        "status": 500,
        "code": "FileUploadFailed",
        "message": "File upload failed",
    },
    ErrorCode.INTERNAL_ERROR.value: {
        "status": 500,
        "code": "InternalError",
        "message": "Internal server error",
    },
    # === 501 NOT IMPLEMENTED ===
    ErrorCode.NOT_IMPLEMENTED.value: {
        "status": 501,
        "code": "NotImplemented",
        "message": "Feature not implemented",
    },
    # === 502 BAD GATEWAY ===
    ErrorCode.EXTERNAL_API_FAILED.value: {
        "status": 502,
        "code": "ExternalApiFailed",
        "message": "External service failed",
    },
    ErrorCode.INVALID_RESPONSE.value: {
        "status": 502,
        "code": "InvalidResponse",
        "message": "Invalid response from external service",
    },
    ErrorCode.GOOGLE_USERINFO_FAILED.value: {
        "status": 502,
        "code": "GoogleUserinfoFailed",
        "message": "Failed to fetch user info from Google",
    },
    # === 503 SERVICE UNAVAILABLE ===
    ErrorCode.SERVICE_UNAVAILABLE.value: {
        "status": 503,
        "code": "ServiceUnavailable",
        "message": "Service temporarily unavailable",
    },
    # === 504 GATEWAY TIMEOUT ===
    ErrorCode.TIMEOUT.value: {
        "status": 504,
        "code": "Timeout",
        "message": "External service timeout",
    },
}
