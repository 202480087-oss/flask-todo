from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "complete": self.complete,
        }


with app.app_context():
    db.create_all()


# ── GET all todos ──────────────────────────────────────────────────────────────
@app.route("/api/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return make_response(jsonify([t.to_dict() for t in todos]), 200)


# ── GET single todo by id ──────────────────────────────────────────────────────
@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return make_response(jsonify({"error": "Todo not found"}), 404)
    return make_response(jsonify(todo.to_dict()), 200)


# ── POST create a new todo ─────────────────────────────────────────────────────
@app.route("/api/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    if not data or not data.get("title"):
        return make_response(jsonify({"error": "Title is required"}), 400)

    new_todo = Todo(title=data["title"], complete=data.get("complete", False))
    db.session.add(new_todo)
    db.session.commit()
    return make_response(
        jsonify({"message": "Todo created successfully", "todo": new_todo.to_dict()}),
        201,
    )


# ── PUT update an existing todo ────────────────────────────────────────────────
@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return make_response(jsonify({"error": "Todo not found"}), 404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "No data provided"}), 400)

    if "title" in data:
        todo.title = data["title"]
    if "complete" in data:
        todo.complete = data["complete"]

    db.session.commit()
    return make_response(
        jsonify({"message": "Todo updated successfully", "todo": todo.to_dict()}),
        200,
    )


# ── DELETE a todo ──────────────────────────────────────────────────────────────
@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return make_response(jsonify({"error": "Todo not found"}), 404)

    db.session.delete(todo)
    db.session.commit()
    return make_response(
        jsonify({"message": "Todo deleted successfully"}),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
