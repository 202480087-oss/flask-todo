import unittest
import warnings
import json
from api import app, db, Todo


class TodoAPITests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        warnings.simplefilter("ignore", category=DeprecationWarning)

        with app.app_context():
            db.create_all()
            # seed one todo for read/update/delete tests
            seed = Todo(title="Sample Todo", complete=False)
            db.session.add(seed)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # ── GET /api/todos ─────────────────────────────────────────────────────────

    def test_get_all_todos(self):
        response = self.app.get("/api/todos")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Sample Todo")

    # ── GET /api/todos/<id> ────────────────────────────────────────────────────

    def test_get_todo_by_id(self):
        response = self.app.get("/api/todos/1")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["title"], "Sample Todo")
        self.assertFalse(data["complete"])

    def test_get_todo_not_found(self):
        response = self.app.get("/api/todos/999")
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    # ── POST /api/todos ────────────────────────────────────────────────────────

    def test_create_todo(self):
        payload = {"title": "New Task", "complete": False}
        response = self.app.post(
            "/api/todos",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Todo created successfully")
        self.assertEqual(data["todo"]["title"], "New Task")

    def test_create_todo_missing_title(self):
        payload = {"complete": False}
        response = self.app.post(
            "/api/todos",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_create_todo_no_body(self):
        response = self.app.post("/api/todos", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    # ── PUT /api/todos/<id> ────────────────────────────────────────────────────

    def test_update_todo(self):
        payload = {"title": "Updated Task", "complete": True}
        response = self.app.put(
            "/api/todos/1",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Todo updated successfully")
        self.assertEqual(data["todo"]["title"], "Updated Task")
        self.assertTrue(data["todo"]["complete"])

    def test_update_todo_not_found(self):
        payload = {"title": "Ghost Task"}
        response = self.app.put(
            "/api/todos/999",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_update_todo_no_body(self):
        response = self.app.put("/api/todos/1", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    # ── DELETE /api/todos/<id> ─────────────────────────────────────────────────

    def test_delete_todo(self):
        response = self.app.delete("/api/todos/1")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Todo deleted successfully")

    def test_delete_todo_not_found(self):
        response = self.app.delete("/api/todos/999")
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
