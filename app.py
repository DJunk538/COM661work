from flask import Flask, jsonify, make_response, request
import uuid, random

app = Flask(__name__)

businesses = {}
def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast',
             'Lisburn', 'Ballymena', 'Derry', 'Newry',
             'Enniskillen', 'Omagh', 'Ballymoney']
    business_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = "Biz " + str(i)
        town = towns[random.randint(0, len(towns)-1)]
        rating = random.randint(1, 5)
        business_dict[id] = {
            "name" : name,
            "town" : town,
            "rating" : rating,
            "reviews" : []
        }
    return business_dict

businesses = generate_dummy_data()

@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get('pn'):
        page_num = int(request.args.get('pn'))
    if request.args.get('ps'):
        page_size = int(request.args.get('ps'))
    page_start = (page_size * (page_num - 1))
    businesses_list = [ {k : v} for k,v in businesses.items() ]
    data_to_return = businesses_list[page_start:page_start + page_size ]
    return make_response( jsonify( data_to_return ), 200 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["GET"])
def show_one_business(id):
    if id in businesses:
        return make_response( jsonify(  businesses[id] ), 200 )
    else:
        return make_response( jsonify( \
            { "error" : "Invalid business ID" } ), 404 )

@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    if "name" in request.form and"town" in request.form and"rating" in request.form:
        next_id = str(uuid.uuid1())
        new_business = {
            "id": next_id,
            "name": request.form["name"],
            "town": request.form["town"],
            "rating": request.form["rating"],
            "reviews": []
        }
        businesses[next_id] = new_business
        return make_response( jsonify( {next_id : new_business} ), 201 )
    else:
        return make_response( jsonify(
            { "error" : "Missing form data" } ), 404 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if id not in businesses:
        return make_response( jsonify(
            { "error" : "Invalid business ID" } ), 404 )
    else:
        fields_updated = False
        for field in ("name", "town", "rating"):
            if field in request.form:
                businesses[id][field] = request.form[field]
                fields_updated = True

        if fields_updated:
            return make_response( \
                jsonify( { id : businesses[id] } ), 200 )
        else:
            return make_response( jsonify({ "error" : "Missing form data" } ), 404 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    del businesses[id]
    return make_response( jsonify( {} ), 204)

@app.route("/api/v1.0/businesses/<string:id>/reviews",
           methods=["GET"])
def fetch_all_reviews(id):
    business = businesses[id]
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))

    page_start = page_size * (page_num - 1)
    reviews_to_return = business["reviews"][page_start:page_start + page_size]
    return make_response(jsonify(reviews_to_return), 200)

@app.route("/api/v1.0/businesses/<string:b_id>/reviews",
          methods=["POST"])
def add_new_review(b_id):
    business = businesses[b_id]
    new_review_id = str(uuid.uuid1())
    new_review = {
        "id": new_review_id,
        "username": request.form["username"],
        "comment": request.form["comment"],
        "stars": request.form["stars"]
    }
    business["reviews"].append(new_review)
    return make_response( jsonify( new_review ), 201 )

@app.route( \
        "/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>",
    methods=["GET"])
def fetch_one_review(b_id, r_id):
    business = businesses[b_id]
    review = next(review for review in business["reviews"]
                  if review["id"] == r_id)
    return make_response( jsonify( review ), 200)

@app.route(
    "/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>",
    methods=["PUT"])
def edit_review(b_id, r_id):
    business = businesses[b_id]
    review = next(review for review in business["reviews"]
                  if review["id"] == r_id)
    review["username"] = request.form["username"]
    review["comment"] = request.form["comment"]
    review["stars"] = request.form["stars"]
    return make_response( jsonify( review ), 200)
@app.route(
    "/api/v1.0/businesses/<string:b_id>/reviews/<string:r_id>",
    methods=["DELETE"])
def delete_review(b_id, r_id):
    business = businesses[b_id]
    review = next(review for review in business["reviews"]
                  if review["id"] == r_id)
    business["reviews"].remove(review)
    return make_response( jsonify( {} ), 200)

if __name__ == "__main__":
    businesses = generate_dummy_data()

if __name__ == "__main__":
    app.run(debug=True)
