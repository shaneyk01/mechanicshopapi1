from flask import jsonify, request
from marshmallow import ValidationError  # type: ignore
from sqlalchemy import select
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema, return_ticket_schema, edit_ticket_schema
from app.blueprints.mechanics.schemas import mechanic_schema
from app.models import ServiceTickets, Mechanic, db

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTickets(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = db.session.execute(select(ServiceTickets)).scalars().all()
    return jsonify(service_tickets_schema.dump(tickets)), 200

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['PUT'])
def edit_service_tickets(service_ticket_id):
    try:
        ticket_edits = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    query =select(ServiceTickets).where(ServiceTickets.id== service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    if not service_ticket:
        return jsonify({'message': 'Service ticket not found'}), 404

    # add mechanics
    for mechanic_id in ticket_edits['add_mechanic_ids']:
        m_query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(m_query).scalars().first()
        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)
    
    # remove mechanics
    for mechanic_id in ticket_edits['remove_mechanic_ids']:
        m_query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(m_query).scalars().first()
        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
    db.session.commit()
    return return_ticket_schema.jsonify(service_ticket),200

@service_tickets_bp.route('/<int:service_ticket_id>', methods=['DELETE'])
def delete_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTickets, service_ticket_id)
    if not service_ticket:
        return jsonify({'message': 'Service ticket not found'}), 404
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({'message': f'Service ticket id:{service_ticket_id} was deleted successfully'}), 200


