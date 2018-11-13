# Joseph Reidell
# Project 5: RESTful API
# CS 1520

from flask import Flask, render_template, redirect, url_for, request, json, jsonify, abort, make_response

app = Flask(__name__)

budget = [
    {
        'cat': 1,
        'type': 'None',
        'limit': 0.00,
        'spent': 0.00
    }
]

purchase = [
    {
        'id': 0,
        'cat_id': 0,
        'object': 'No Object Purchased',
        'date': '2018-01-01',
        'spent': 0
    }
]

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/cats', methods=['GET'])
def get_bud_categories():
    return jsonify({'budget': budget})

@app.route('/cats', methods=['POST'])
def post_categories():
    if not request.json or not 'type' in request.json:
        abort(404)
    
    invalid_cat = [category for category in budget if category['type'] == request.json['type']]

    if invalid_cat:
        abort(409, 'Category name already in use!')
    else:
        new_cat = {
            'cat': budget[-1]['cat'] + 1,
            'type': request.json['type'],
            'limit': request.json['limit'],
            'spent': 0
        }
    budget.append(new_cat)
    return jsonify({'new_cat': new_cat}), 201

@app.route('/cats/<int:cat_id>', methods=['GET'])
def get_categories(cat_id):
    category = get_id(cat_id)

    if len(category) == 0:
        abort(404)
    else:
        return jsonify({'category': category[0]})

@app.route('/purchases', methods=['GET'])
def get_all_purchases():
    return jsonify({'purchase': purchase})

@app.route('/purchases', methods=['PUT'])
def put_purchases():
     if not request.json or not 'cat_id' in request.json:
        abort(400)
     else:
        new_purchase = {
            'id': purchase[-1]['id'] + 1,
            'cat_id': request.json['cat_id'],
            'object': request.json['object'],
            'date': request.json['date'],
            'spent': float(request.json['spent'])
        }

        for category in budget:
            if category['cat'] == new_purchase['cat_id']:
                category['spent'] += new_purchase['spent']

        purchase.append(new_purchase)
        return jsonify({'new_purchase': new_purchase}), 201

@app.route('/purchases/<int:purchase_id>', methods=['GET'])
def get_purchases(purchase_id):
    purchases = [purchases for purchases in purchase if purchases['id'] == purchase_id]

    if len(purchases) == 0:
        abort(404)
    else:
        return jsonify({'purchases': purchases[0]})

@app.route('/cats/<int:cat_id>', methods=['DELETE'])
def delete_categories(cat_id):
    delete_cat = [delete_cat for delete_cat in budget if delete_cat['cat'] == cat_id]

    if len(delete_cat) == 0:
        abort(404)
    else:
        for purchases in purchase:
            if purchases['cat_id'] == int(cat_id):
                purchases['cat_id'] = 1
                update_cat = get_id(1)
                update_cat['spent'] += purchases['spent']
        delete_purch = jsonify({'delete': delete_cat[0]['type']})
        budget.remove(delete_cat[0])
        return delete_purch

# Helper Function
def get_id(category_id):
    return next(category for category in budget if category['cat'] == int(category_id))

# Error Functions
@app.errorhandler(400)
def custom400(error):
    response = jsonify({
        'message': error.description['message'],
        'status_code': 400,
        'status': 'Bad Request'
    })
    return response, 400

if __name__ == "__main__":
	app.run()