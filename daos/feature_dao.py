from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from database.tables import Feature

class FeatureDao:
    def __init__(self, session: Session):
        self.session = session

    def add_feature(self, feature: Feature):
        try:
            self.session.add(feature)
            self.session.commit()
            self.session.refresh(feature)
            return feature

        except SQLAlchemyError as error:
            print("Feature Creating Error: ", error)
            self.session.rollback()
            return None
        
    def get_feature(self, feature_id: int):
        return self.session.exec(select(Feature).
                                 where(Feature.id == feature_id)
                                 ).first()
    
    def delete_feature(self, feature: Feature):
        try:
            self.session.delete(feature)
            self.session.commit()
            return True
        except SQLAlchemyError as error:
            print("Feature Deleting Error: ", error)
            self.session.rollback()
            return False
        
    def get_features(self, project_id: int):
        return self.session.exec(select(Feature).
                                 where(Feature.id_project == project_id).
                                 order_by(Feature.id)
                                 ).all()
        