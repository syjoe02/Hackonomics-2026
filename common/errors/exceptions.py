class BusinessException(Exception):
    def __init__(self, error_code):
        self.error_code = error_code
        super().__init__(str(error_code))
