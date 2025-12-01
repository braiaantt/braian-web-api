#------ Portfolio Exceptions ------
class PortfolioAlreadyExistsError(Exception):   
    pass

class PortfolioCreationError(Exception):
    pass

class PortfolioNotExists(Exception):
    pass

class PortfolioUpdatingError(Exception):
    pass

#------ Technology Exceptions ------

class TechnologyCreationError(Exception):
    pass

class TechnologyNotExists(Exception):
    pass

class TechnologyDeletingError(Exception):
    pass

class TechnologyUpdatingError(Exception):
    pass

#------ Project Exceptions ------

class ProjectNotExists(Exception):
    pass

class ProjectDeletingError(Exception):
    pass

class ProjectUpdatingError(Exception):
    pass

class ProjectCreationError(Exception):
    pass

#------ File Exceptions ------

class InvalidContentType(Exception):
    pass

#------ Entity Technology Exceptions ------

class EntityTechnologyCreationError(Exception):
    pass

class EntityTechnologyRelationNotExists(Exception):
    pass
    
#------ Entity Image Exceptions ------

class EntityImageCreationError(Exception):
    pass

class EntityImageNotFound(Exception):
    pass

class EntityImageDeletingError(Exception):
    pass