from flask import Blueprint, request, jsonify
from app.services.farm_service import FarmService
from app.schemas.farm import FarmCreateSchema, FarmUpdateSchema
from app.errors import AppError
from marshmallow import ValidationError

farms_bp = Blueprint('farms', __name__)

@farms_bp.route('', methods=['GET'], strict_slashes=False)
def get_farms():
    """
    Get all farms
    ---
    tags:
      - Farms
    responses:
      200:
        description: List of all farms
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              created_at:
                type: string
              updated_at:
                type: string
    """
    farms = FarmService.get_all_farms()
    return jsonify([farm.to_dict() for farm in farms])

@farms_bp.route('/<int:farm_id>', methods=['GET'], strict_slashes=False)
def get_farm(farm_id):
    """
    Get farm by ID
    ---
    tags:
      - Farms
    parameters:
      - name: farm_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Farm details
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Farm not found
        schema:
          type: object
          properties:
            message:
              type: string
            errors:
              type: object
    """
    farm = FarmService.get_farm_by_id(farm_id)
    return jsonify(farm.to_dict())

@farms_bp.route('', methods=['POST'], strict_slashes=False)
def create_farm():
    """
    Create a new farm
    ---
    tags:
      - Farms
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              example: "Ферма 6"
    responses:
      201:
        description: Farm created
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            created_at:
              type: string
            updated_at:
              type: string
      400:
        description: Validation error
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Validation error"
            errors:
              type: object
              example:
                name: ["Farm with this name already exists"]
    """
    try:
        schema = FarmCreateSchema()
        data = schema.load(request.json)
        farm = FarmService.create_farm(data['name'])
        return jsonify(farm.to_dict()), 201
    except ValidationError as e:
        raise AppError('Validation error', 400, e.messages)
    except ValueError as e:
        raise AppError('Invalid request', 400)

@farms_bp.route('/<int:farm_id>', methods=['PUT'], strict_slashes=False)
def update_farm(farm_id):
    """
    Update a farm
    ---
    tags:
      - Farms
    parameters:
      - name: farm_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Новое название фермы"
    responses:
      200:
        description: Farm updated
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            created_at:
              type: string
            updated_at:
              type: string
      400:
        description: Validation error
        schema:
          type: object
          properties:
            message:
              type: string
            errors:
              type: object
      404:
        description: Farm not found
        schema:
          type: object
          properties:
            message:
              type: string
            errors:
              type: object
    """
    try:
        schema = FarmUpdateSchema()
        data = schema.load(request.json)
        farm = FarmService.update_farm(farm_id, data['name'])
        return jsonify(farm.to_dict())
    except ValidationError as e:
        raise AppError('Validation error', 400, e.messages)
    except ValueError as e:
        raise AppError('Invalid request', 400)

@farms_bp.route('/<int:farm_id>', methods=['DELETE'], strict_slashes=False)
def delete_farm(farm_id):
    """
    Delete a farm
    ---
    tags:
      - Farms
    parameters:
      - name: farm_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Farm deleted
      404:
        description: Farm not found
        schema:
          type: object
          properties:
            message:
              type: string
            errors:
              type: object
    """
    FarmService.delete_farm(farm_id)
    return '', 204