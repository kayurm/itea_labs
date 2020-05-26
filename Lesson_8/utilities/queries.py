from Lesson_8.utilities import context_manager as cm


class Queries:

    @staticmethod
    def get_all_categories():
        sql = "SELECT * FROM category"
        with cm.MyDBManager("catalogue.db", "r") as db:
            db.execute(sql)
            return db.fetchall()

    @staticmethod
    def get_available_products_by_category(category):
        sql = "SELECT category.categ_name, products.prod_name FROM products " \
              "INNER JOIN category ON products.categ_id=category.categ_id " \
              "WHERE products.is_available = 1 AND category.categ_name = ?"
        with cm.MyDBManager("catalogue.db", "r") as db:
            db.execute(sql, [category])
            return db.fetchall()

    @staticmethod
    def get_product_details(category, product):
        sql = "SELECT products.prod_name, products.price, products.quantity " \
              "FROM products INNER JOIN category on products.categ_id=category.categ_id " \
              "WHERE category.categ_name= ? AND products.prod_name = ?"
        with cm.MyDBManager("catalogue.db", "r") as db:
            db.execute(sql, [category, product])
            return db.fetchall()

    # for ADMIN PAGE
    @staticmethod
    def add_new_category(new_category):
        sql = "INSERT INTO category ('categ_name') VALUES (?)"
        with cm.MyDBManager("catalogue.db", "w") as db:
            db.execute(sql, [new_category])
        success = True if new_category in dict(Queries.get_all_categories()).values() else False
        return success

    @staticmethod
    def add_new_product(pr_name, categ_name, pr_price, pr_qty, is_avail):
        sql = "INSERT INTO products ('prod_name', 'categ_id', 'is_available', 'quantity', 'price') VALUES (?,?,?,?,?)"
        sql_nested = "SELECT categ_id from category where categ_name=?"
        with cm.MyDBManager("catalogue.db", "w") as db:
            db.execute(sql_nested, [categ_name])
            categ_id = list(db.fetchall())[0][0]
            db.executemany(sql, [(pr_name, categ_id, is_avail, pr_qty, pr_price)])
        result = Queries.get_product_details(categ_name, pr_name)
        if pr_name == result[0][0] and pr_price == result[0][1] and pr_qty == result[0][2]:
            success = True
        else:
            success = False
        return success
