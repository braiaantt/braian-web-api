from sqlmodel import Session
from models.feature import FeatureCreate
from daos.feature_dao import FeatureDao
from database.tables import Feature
from exceptions.exceptions import FeatureCreationError, FeatureDeletingError, FeatureNotFound

class FeatureService:
    def __init__(self, session: Session):
        self.feature_dao = FeatureDao(session)

    def add_feature(self, data: FeatureCreate):
        feature = Feature(id_project=data.id_project,
                          feat=data.feat)
        
        feature_created = self.feature_dao.add_feature(feature)
        if not feature_created:
            raise FeatureCreationError()
        
        return feature_created
    
    def delete_feature(self, feature_id: int):
        feature = self.feature_dao.get_feature(feature_id)
        if not feature:
            raise FeatureNotFound()
        
        deleted = self.feature_dao.delete_feature(feature)
        if not deleted:
            raise FeatureDeletingError()
        
        return
    
    def get_features(self, project_id: int):
        return self.feature_dao.get_features(project_id)