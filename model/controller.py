from config import *
from model.data.Flower import *

from model.tools.FileUtil import *
from model.tools.WordsTool import *

from flask import request, url_for, redirect, render_template

import cv2
import numpy as np

from datetime import date, timedelta

from werkzeug.exceptions import *
from sqlalchemy.exc import DatabaseError

def exceptionProcessing(foo):
    global index
    def inner(*args, **kwargs):
        try:
            return foo(*args, **kwargs)
        except HTTPException as httpe:
            return render_template('message.html', title='Возникла ошибка', text=str({request.path.split('/')[-1]: False, 'data': {'description': 'HTTP error'}}))
        except DatabaseError as de:
            return render_template('message.html', title='Возникла ошибка', text=str({request.path.split('/')[-1]: False, 'data': {'description': 'Identy error, such outerId already exist'}}))
        except KeyError as jsone:
            return render_template('message.html', title='Возникла ошибка', text=str({request.path.split('/')[-1]: False, 'data': {'description': f'Json error, lost {str(jsone.args[0]).upper()} param', 'param': jsone.args[0]}}))
        except Exception as e:
            print(e)
            return render_template('message.html', title='Возникла ошибка', text=str({request.path.split('/')[-1]: False, 'data': {'description': 'Unmatched error', "error": type(e).__name__}}))
    inner.__name__ = foo.__name__
    return inner



@app.route('/saveFlower', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def savePost(): 
    bData = None
    name = request.form.get('name')
    info = request.form.get('info')
    interval=request.form.get('interval')
    
    id = request.form.get('id')
    print(id, type(id))
    
    
    if name:
        if len(name) == 0:
            name = None
        
    for file in request.files:
        img = cv2.imdecode(np.fromstring(request.files[file].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (200,300))
        bData = FileUtil.convertImageToBytes(img)

    if id != 'None':
        flower = Flower.getByID(int(id))
        flower.name = name
        flower.info = info
        flower.interval = interval
        if bData:
            flower.image = bData
    else:
        flower=Flower(name, info, bData, interval)
    flower.save()
    
    return {"saveFlower":True, "setId":flower.id}



@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def redirectMain(): 
    return redirect('/main')

@app.route('/main', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def main(): 
    
    return render_template('main.html', flowers=Flower.getOrderedByNames())


@app.route('/info', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def info(): 
    return render_template('info.html')


@app.route('/flower', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def getFlower(): 
    id=request.args.get('id')
    flower = Flower.getByID(id)
    
    if flower:
        today = date.today()
        waterings = flower.getWateringsInLastDays(8)
        waterings = list(map(lambda w:w.date.day, waterings))
        
        marks = [{'day':(today- timedelta(days = i)).day, 'class':'watered' if (today- timedelta(days = i)).day in waterings else ''} for i in range(8)]
        marks.reverse()
        marks[-1]['class'] += ' today' 
        status=flower.getStatus()
        return render_template('flower.html', flower=flower,marks=marks, word=getDayWord(flower.interval),status=status)
    return render_template('message.html', title='Возникла ошибка', text='Такого ID нет в системе')

@app.route('/newFlower', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def newFlower(): 
    flower = Flower('', '', '')
    return render_template('edit_flower.html', flower=flower)
        

@app.route('/editFlower', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def editFlower(): 
    id=request.args.get('id')
    flower = Flower.getByID(id)
    if flower:
        return render_template('edit_flower.html', flower=flower)
    return render_template('message.html', title='Возникла ошибка', text='Такого ID нет в системе')


@app.route('/waterFlower', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def waterFlower(): 
    id=request.args.get('id')
    flower = Flower.getByID(id)
    
    if flower:
        try:
            flower.waterToday()
        except Exception as e:
            print(e)
        return redirect(url_for('getFlower', id=id))
    return render_template('message.html', title='Возникла ошибка', text='Такого ID нет в системе')
    
    
@app.route('/deleteFlower', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def deleteFlower(): 
    
    id=request.args.get('id')
    silance=request.args.get('silance')
    
    flower = Flower.getByID(id)
    if flower:
        try:
            Watering.deleteByFlower(flower.id)
            flower.delete()
        except Exception as e:
            print(e)
            raise e
        
        if silance:
            return redirect('/main')
        return render_template('message.html', title="Подтверждение", text='Запись была удалена')
    return render_template('message.html', title='Возникла ошибка', text='Такого ID нет в системе')

@app.route('/game', methods=['GET', 'POST', 'OPTIONS'])
@exceptionProcessing
def getGame(): 
    return render_template('game.html')