class PortfolioAlreadyExistsError(Exception):
    """Raised when trying to create a portfolio that already exists."""
    pass

class PortfolioCreationError(Exception):
    """Raised when an unexpected error occurs during portfolio creation."""
    pass
