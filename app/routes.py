from flask import Blueprint, request, jsonify, make_response
from app.models.board import Board
from app.models.card import Card
from app import db

board_bp = Blueprint('board_bp', __name__)


@board_bp.route('/')
def index():
    return {
        "name": "Simon Del Rosaasfasdfrio",
        "message": "Hi instructors! :)"
    }


@board_bp.route('/boards', methods=['GET'])
def get_boards():
    boards = Board.query.all()
    results = []
    for board in boards:
        results.append({
            "board_id": board.board_id,
            "title": board.title,
            "owner": board.owner
        })
    return jsonify(results)


@board_bp.route('/boards', methods=['POST'])
def create_boards():
    body = request.get_json()
    if ("title" in body) and ("owner" in body):
        new_board = Board(
            title=body["title"],
            owner=body["owner"])

        db.session.add(new_board)
        db.session.commit()

        return make_response({"board": {
            "board_id": new_board.board_id,
            "title": new_board.title,
            "owner": new_board.owner
        }}, 201)


@board_bp.route('/boards/<board_id>/cards', methods=['GET'])
def get_cards_for_board(board_id):
    print("HERE 1", board_id)
    board = Board.query.get_or_404(board_id)
    print("HERE 2", board)
    print("HERE 3", board.title)
    print("HERE 3", board.cards)
    cards = []

    for card in board.cards:
        cards.append({
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
        })

    return jsonify(cards)


@board_bp.route('/boards/<board_id>/cards', methods=['POST'])
def create_card_for_board(board_id):
    board = Board.query.get_or_404(board_id)

    body = request.get_json()
    if "message" not in body:
        return make_response(jsonify({
            "error": "Missing Message"
        }), 400)

    new_card = Card(message=body["message"], likes_count=0)
    db.session.add(new_card)
    board.cards.append(new_card)
    db.session.commit()

    return make_response({"card": {
        "card_id": new_card.card_id,
        "board_id": new_card.board_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count
    }}, 201)


@board_bp.route('/cards/<card_id>', methods=['DELETE'])
def delete_card_for_board(card_id):
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return {"details": f'Card {card.card_id} "{card.message}" successfully deleted'}


@board_bp.route('/cards/<card_id>/like', methods=['PUT'])
def plus_one_card_for_board(card_id):
    card = Card.query.get_or_404(card_id)
    if card.likes_count == None:
        card.likes_count = 0
    card.likes_count = card.likes_count + 1
    db.session.commit()
    return {"details": f'Card {card.card_id} "{card.message}" successfully deleted'}


@board_bp.route('/destroy_all', methods=['DELETE'])
def destroy_all_boards_and_cards():
    Card.query.delete()
    Board.query.delete()

    card_a = Card(message="You're like a cup of tea: green! 😍", likes_count=3)
    card_b = Card(
        message="You're strong and you have good taste in computers. 🐶🎉", likes_count=5)
    card_c = Card(message="Effort won't betray you. 💖", likes_count=3)
    card_d = Card(
        message="⭐️✨ Live, laugh, love, Lord of the Rings ⭐️✨", likes_count=0)
    card_e = Card(
        message="Did it hurt when you fell? Here's a band-aid and water, and don't forget to check-in and ask for help.",
        likes_count=1)

    new_board = Board(title="Pick-me-up Quotes", owner="Ada L.")
    new_board.cards = [card_a, card_b, card_c, card_d, card_e]
    db.session.add_all([card_a, card_b, card_c, card_d, card_e, new_board])
    db.session.commit()
    return {
        "details": f'All boards and cards successfully deleted',
        "default_board": {
            "board_id": new_board.board_id,
            "title": new_board.title,
            "owner": new_board.owner
        }
    }
