#source activate yolo5_5
python3 val.py --weights weights/PersonCar_all_new_20220424.pt --data data/person_car.yaml --img 640 --iou 0.6 --batch-size 32 --device 0 --workers 0 --min-size 10

# python3 val.py --weights weights/CityManage_City_20220125.pt --data data/city_manage.yaml --img 640 --iou 0.6