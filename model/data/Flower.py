from config import *

from model.data.BaseData import *
from model.data.Watering import *

from datetime import date

from sqlalchemy import and_

class Flower(db.Model, BaseData):
    
    name = db.Column(db.Text, unique=False, nullable=False)
    info = db.Column(db.Text, unique=False)
    image = db.Column(db.Text, unique=False)
    interval = db.Column(db.Integer, unique=False, nullable=False)
    
    waterings = db.relationship('Watering', backref='post')
    
    def __init__(self, 
                 name:str, info:str, img:str, interval:int = None):
        
        self.name = name
        self.info = info
        self.image = img
        if interval:
            self.interval = interval
        else:
            self.interval = 2
        
        db.Model.__init__(self)
        BaseData.__init__(self, self.id)
        
    def waterToday(self):
        watering =  Watering(date.today(), self.id)
        watering.save()
        
    
    def getWateringsInLastDays(self, daysCount)->"Watering":
        lastDay = d.today() - timedelta(days = daysCount)
        return Watering.query.filter(and_(Watering.date>=lastDay, Watering.flowerId==self.id)).all()
    
    def getLastWatering(self):
        return Watering.query.filter(Watering.flowerId==self.id).order_by(Watering.date.desc()).first()
    
    def getStatus(self):
        today = date.today()
        lastWatering=self.getLastWatering()
        status='😵'
        if lastWatering:    
            if today - lastWatering.date < timedelta(days = self.interval):
                status='😊'
            elif timedelta(days = self.interval) <= today - lastWatering.date < timedelta(days = self.interval+1):
                status='💧'
            else:
                status='💀'
        
        return status
    
    
    @classmethod
    def getOrderedByNames(cls):
        return cls.query.order_by(cls.name).all()