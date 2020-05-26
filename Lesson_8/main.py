"""
Kate Yurmanovych
Lesson 8

1) Создать базу данных товаров, у товара есть: Категория (связанная
таблица), название, есть ли товар в продаже или на складе, цена, кол-во
единиц.Создать html страницу. На первой странице выводить ссылки на все
категории, при переходе на категорию получать список всех товаров в
наличии ссылками, при клике на товар выводить его цену, полное описание и
кол-во единиц в наличии.
2) Создать страницу для администратора, через которую он может добавлять
новые товары и категории.
"""

from flask import Flask, request
from flask import render_template
from Lesson_8.utilities import queries as q

app = Flask(__name__)


@app.route('/')
def show_categories():
    categories = dict(q.Queries.get_all_categories()).values()
    return render_template('main_page.html', categories=categories)


@app.route('/<category>')
def show_available_products_by_category(category):
    products = dict(q.Queries.get_available_products_by_category(category)).values()
    return render_template('products_by_category_page.html', products=products, category=category)


@app.route('/<category>/<product>')
def show_product_details(category, product):
    product = q.Queries.get_product_details(category, product)
    return render_template('product_page.html',
                           prod_name=product[0][0],
                           prod_price=product[0][1],
                           prod_qty=product[0][2])


# ADMIN MODULE
@app.route('/admin')
def admin_main():
    categories = dict(q.Queries.get_all_categories()).values()
    return render_template('admin_page.html', categories=categories)


@app.route('/admin/category', methods=["GET", "POST"])
def admin_category():
    if request.method == "GET":
        return render_template('admin_add_category.html')
    else:
        new_category = request.form["new_category"]
        query_ = q.Queries.add_new_category(new_category)
        return render_template('admin_add_category.html', new_category=new_category, is_success=query_)


@app.route('/admin/product', methods=["GET", "POST"])
def admin_add_product():
    if request.method == "GET":
        categories = dict(q.Queries.get_all_categories()).values()
        return render_template('admin_add_product.html', categories=categories)
    else:
        pr_name = request.form["pr_name"]
        categ_name = request.form["categ_name"]
        pr_price = float(request.form["pr_price"])
        pr_qty = int(request.form["pr_qty"])
        is_avail = 1 if pr_qty > 0 else 0
        query_ = q.Queries.add_new_product(pr_name, categ_name, pr_price, pr_qty, is_avail)
        return render_template('admin_add_product.html', new_product=pr_name, is_success=query_)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
