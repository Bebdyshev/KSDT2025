import serial
import threading
from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import app, db
from models import DataSet, GroundBuoy, GroundStation
from datetime import datetime
import json
import random
import time
import os

def generate_random_data():
    while True:
        try:
            with app.app_context():
                # Генерация данных для буя 1
                current_time = datetime.now()
                new_data = DataSet(
                    buoy_id=1,
                    time=current_time,
                    height=random.uniform(100, 900),  # Высота от 0 до 40
                    latitude=49.791284 + random.uniform(-0.001, 0.001),
                    longitude=73.148163 + random.uniform(-0.001, 0.001),
                    pressure=random.uniform(980, 1020),  # Давление
                    temp=random.uniform(20, 30),  # Температура
                    density=random.uniform(1.0, 1.5),  # Плотность
                    ph=random.uniform(6.5, 8.5),  # pH
                    velocity=random.uniform(0, 10),  # Скорость
                    pitch=random.uniform(-45, 45),  # Тангаж
                    roll=random.uniform(-45, 45),  # Крен
                    yaw=random.uniform(0, 360)  # Рыскание
                )
                db.session.add(new_data)

                # Генерация данных для буя 2
                ground_data = GroundBuoy(
                    buoy_id=2,
                    time=current_time,
                    above=random.uniform(0, 30),  # Уровень воды сверху
                    under=random.uniform(0, 30)  # Уровень воды снизу
                )
                db.session.add(ground_data)
                
                db.session.commit()
                print(f"Generated data at {current_time}")

        except Exception as e:
            print(f"Error generating data: {e}")
        
        time.sleep(1)  # Генерируем новые данные каждую секунду

def process_serial_data(data_line):
    try:
        with app.app_context():
            data_parts = data_line.split(';')
            buoy_id = int(data_parts[0])
            current_time = datetime.now()
            print(data_parts)
            if buoy_id == 1:
                ph = float(data_parts[2])
                height = float(data_parts[3])
                latitude = 49.791284 
                longitude = 73.148163
                temp = float(data_parts[6])
                density = float(data_parts[7])
                velocity = float(data_parts[8])
                pressure = float(data_parts[9])
                pitch = float(data_parts[10])
                roll = float(data_parts[11])
                yaw = float(data_parts[12])

                new_data = DataSet(
                    buoy_id=buoy_id,
                    time=current_time,
                    height=height,
                    latitude=latitude,
                    longitude=longitude,
                    pressure=pressure,
                    temp=temp,
                    density=density,
                    ph=ph,
                    velocity=velocity,
                    pitch=pitch,
                    roll=roll,
                    yaw=yaw
                )

            elif buoy_id == 2:
                above = float(data_parts[2])
                under = float(data_parts[3])

                new_data = GroundBuoy(
                    buoy_id=buoy_id,
                    time=current_time,
                    above=above,
                    under=under,
                )
            
            db.session.add(new_data)
            db.session.commit()
    except Exception as e:
        print(f"Data processing error: {e}")

@app.route('/data', methods=['GET'])
def get_data():
    try:
        dataSet = DataSet.query.all()
        json_dataSet = [data.to_json() for data in dataSet]
        return jsonify({"data": json_dataSet})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/data_ground', methods=['GET'])
def get_data_ground():
    try:
        groundBuoyData = GroundBuoy.query.all()
        json_groundBuoyData = [data.to_json() for data in groundBuoyData]
        return jsonify({"data": json_groundBuoyData})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/data_ground_station', methods=['GET'])
def get_data_ground_station():
    try:
        groundStationData = GroundStation.query.all()
        json_groundStationData = [data.to_json() for data in groundStationData]
        return jsonify({"data": json_groundStationData})
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/create_data', methods=['POST'])
def create_data():
    try:
        data = request.json
        buoy_id = int(data['buoy_id'])
        current_time = datetime.now()

        if buoy_id == 1:
            new_data = DataSet(
                buoy_id=buoy_id,
                time=current_time,
                height=float(data['height']),
                latitude=float(data['latitude']),
                longitude=float(data['longitude']),
                pressure=float(data['pressure']),
                temp=float(data['temp']),
                density=float(data['density']),
                ph=float(data['ph']),
                velocity=float(data['velocity']),
                pitch=float(data['pitch']),
                roll=float(data['roll']),
                yaw=float(data['yaw'])
            )

        elif buoy_id == 2:
            new_data = GroundBuoy(
                buoy_id=buoy_id,
                time=current_time,
                above=float(data['above']),
                under=float(data['under']),
            )

        else:
            return jsonify({"message": "Invalid buoy_id"}), 400

        db.session.add(new_data)
        db.session.commit()

        return jsonify({"message": "Data added successfully"}), 201

    except Exception as e:
        return jsonify({"message": f"Data creation error: {str(e)}"}), 500


@app.route('/delete_all_data', methods=['DELETE'])
def delete_all_data():
    try:
        with app.app_context():
            num_rows_deleted = db.session.query(DataSet).delete()
            num_rows_deleted2 = db.session.query(GroundBuoy).delete()
            db.session.commit()
            return jsonify({"message": f"Deleted {num_rows_deleted} rows from DataSet table."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Запускаем генератор случайных данных вместо serial_reader
    data_generator_thread = threading.Thread(target=generate_random_data)
    data_generator_thread.daemon = True  # Поток завершится вместе с основной программой
    data_generator_thread.start()

    app.run(debug=True)
