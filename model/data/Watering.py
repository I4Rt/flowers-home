from config import *

from model.data.BaseData import *
from datetime import date as d
from datetime import timedelta


class Watering(db.Model, BaseData):
    
    date = db.Column(db.Date(), nullable=False)
    flowerId = db.Column(db.Integer, db.ForeignKey('flower.id'), nullable=False)
    
    
    __table_args__ = (
        db.UniqueConstraint('flowerId', 'date', name='_datetime_unique'),
    )
    
    def __init__(self, 
                 date:d, flowerId=flowerId):
        
        self.date = date
        self.flowerId = flowerId
        
        
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        
        
    @classmethod
    def deleteByFlower(cls, flowerId):
        waterings = Watering.query.filter(Watering.flowerId==flowerId)
        waterings.delete(synchronize_session=False)
        
    