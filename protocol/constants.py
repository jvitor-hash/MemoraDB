# Front-end -> Back-end

QUERY     = b"Q"
PARSE     = b"P"
BIND      = b"B"
DESCRIBE  = b"D"
EXECUTE   = b"E"
SYNC      = b"S"
TERMINATE = b"X"

# Back-end -> Front-end

AUTHENTICATION   = b"R"
PARAMETER_STATUS = b"S"
READY_FOR_QUERY  = b"Z"
ROW_DESCRIPTION  = b"T"
DATA_ROW         = b"D"
COMMAND_COMPLETE = b"C"
ERROR_RESPONSE   = b"E"
NOTICE_RESPONSE  = b"N"