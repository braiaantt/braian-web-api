class RefreshTokenCreationError(Exception):
    pass

class RefreshTokenRevoked(Exception):
    pass

class RefreshTokenRevokingError(Exception):
    pass

class RefreshTokenExpired(Exception):
    pass