from flask import Flask, jsonify, request
from todoItem import TodoItem
from todoDao import TodoDao

app = Flask(__name__)
todo_dao = TodoDao('todo_example.db')


@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    new_item = TodoItem(None, data['title'], data['is_completed'])
    todo_dao.add_item(new_item)
    return jsonify({"message": "Todo item created"}), 201


@app.route('/todos', methods=['GET'])
def get_all_todos():
    items = todo_dao.get_all_items()
    return jsonify([item.__dict__ for item in items]), 200


@app.route('/todos/<int:item_id>', methods=['GET'])
def get_todo(item_id):
    item = todo_dao.get_item(item_id)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({"message": "Item not found"}), 404


@app.route('/todos/<int:item_id>', methods=['PUT'])
def update_todo(item_id):
    data = request.get_json()
    updated_item = TodoItem(item_id, data['title'], data['is_completed'])
    if todo_dao.update_item(updated_item):
        return jsonify({"message": "Item updated"}), 200
    else:
        return jsonify({"message": "Item not found or not updated"}), 404


@app.route('/todos/<int:item_id>', methods=['DELETE'])
def delete_todo(item_id):
    if todo_dao.delete_item(item_id):
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"message": "Item not found or not deleted"}), 404


if __name__ == '__main__':
    # Generate todo items
    todo_dao.create_table()
    todo_dao.add_item(TodoItem(1, 'Buy milk', False))
    todo_dao.add_item(TodoItem(2, 'Buy eggs', False))
    todo_dao.add_item(TodoItem(3, 'Buy bread', False))
    todo_dao.add_item(TodoItem(4, 'Buy butter', False))

    app.run()
