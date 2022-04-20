import json
from flask import Flask,  jsonify
from database.postgresql.use_db import db
from classes import FoodType, Food


app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

@app.route('/init', methods=['GET'])
def init():
    db.create_all_tables()
    db.insert_test_data()


@app.route('/api/v1/foods/', methods=['GET'])
def index() -> 'json':
    # инстансы категорий
    food_types = [FoodType(*data) for data in db.get_food_types()]
    data = []
    for food_type in food_types:
        # инстансы блюд
        food_type.foods = [Food(*data) for data in db.get_foods_by_food_type_id(food_type.id)]
        food_data = []
        for food in food_type.foods:
            if food.is_publish:
                food_data.append({"internal_code": food.internal_code, "code": food.code, "name_ru": food.name_ru,
                              "description_ru": food.description_ru, "description_en": food.description_en,
                              "description_ch": food.description_ch, "is_vegan": food.is_vegan,
                              "is_special": food.is_special, "is_publish": food.is_publish,  "cost": food.cost,
                                  "additional": food.additional})

        if food_data:
            data.append({"id": food_type.id, "name_ru": food_type.name_ru, "name_en": food_type.name_en,
                     "name_ch": food_type.name_ch, "order_id": food_type.order_id, "foods": food_data })
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(debug=True)