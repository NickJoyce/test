class FoodType:
    def __init__(self, id_, name_ru, name_en, name_ch, order_id):
        self.id = id_
        self.name_ru = name_ru
        self.name_en = name_en
        self.name_ch = name_ch
        self.order_id = order_id
        self.foods = []

class Food:
    def __init__(self, id_, internal_code, code, name_ru, description_ru, description_en, description_ch, is_vegan,
                 is_special, is_publish, cost):
        self.id = id_
        self.internal_code = internal_code
        self.code = code
        self.name_ru = name_ru
        self.description_ru = description_ru
        self.description_en = description_en
        self.description_ch = description_ch
        self.is_vegan = is_vegan
        self.is_special = is_special
        self.is_publish = is_publish
        self.cost = cost
        self.additional = []


if __name__ == "__main__":
    category1 =FoodType(1, 'Напитки', None, None, 10)
    category2 = FoodType(2, 'Выпечка', None, None, 20)

    tea = Food(100, 1, 'Чай', 'Чай 100 гр.', None, None, False, False, True, 123.10)

