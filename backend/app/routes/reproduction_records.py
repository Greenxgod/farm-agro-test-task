from flask import Blueprint, request, jsonify
from app.services.reproduction_record_service import ReproductionRecordService
from app.schemas.reproduction_record import ReproductionRecordCreateSchema, ReproductionRecordSchema
from app.errors import AppError
from marshmallow import ValidationError

records_bp = Blueprint('reproduction_records', __name__)

@records_bp.route('/', methods=['GET'])
def get_records():
    """
    Get reproduction records with filters and pagination
    ---
    tags:
      - Records
    parameters:
      - name: farm_id
        in: query
        type: integer
        required: false
        description: Filter by farm ID
      - name: date_from
        in: query
        type: string
        format: date
        required: false
        description: Filter records from this date
      - name: date_to
        in: query
        type: string
        format: date
        required: false
        description: Filter records to this date
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number for pagination
      - name: limit
        in: query
        type: integer
        default: 20
        description: Number of records per page
      - name: sort
        in: query
        type: string
        enum: [date, farm_name]
        default: date
        description: Sort field
      - name: order
        in: query
        type: string
        enum: [asc, desc]
        default: desc
        description: Sort order
    responses:
      200:
        description: List of records with pagination
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  farm_id:
                    type: integer
                  farm_name:
                    type: string
                  date:
                    type: string
                    format: date
                  abort:
                    type: integer
                  bulls_from_cows:
                    type: integer
                  bulls_from_heifers:
                    type: integer
                  conception_cows:
                    type: integer
                  conception_heifers:
                    type: integer
                  cows_from_cows:
                    type: integer
                  cows_from_heifers:
                    type: integer
                  dead_bulls:
                    type: integer
                  dead_heifers:
                    type: integer
                  preg_rate_cows:
                    type: number
                  preg_rate_heifers:
                    type: number
                  reproduction_cows:
                    type: integer
                  reproduction_heifers:
                    type: integer
            pagination:
              type: object
              properties:
                page:
                  type: integer
                limit:
                  type: integer
                total:
                  type: integer
                pages:
                  type: integer
    """
    farm_id = request.args.get('farm_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    sort = request.args.get('sort', 'date')
    order = request.args.get('order', 'desc')
    
    result = ReproductionRecordService.get_records(
        farm_id=farm_id,
        date_from=date_from,
        date_to=date_to,
        sort=sort,
        order=order,
        page=page,
        limit=limit
    )
    return jsonify(result)

@records_bp.route('/<int:record_id>', methods=['GET'])
def get_record(record_id):
    """
    Get reproduction record by ID
    ---
    tags:
      - Records
    parameters:
      - name: record_id
        in: path
        type: integer
        required: true
        description: Record ID
    responses:
      200:
        description: Record details
        schema:
          type: object
          properties:
            id:
              type: integer
            farm_id:
              type: integer
            farm_name:
              type: string
            date:
              type: string
              format: date
            abort:
              type: integer
            bulls_from_cows:
              type: integer
            bulls_from_heifers:
              type: integer
            conception_cows:
              type: integer
            conception_heifers:
              type: integer
            cows_from_cows:
              type: integer
            cows_from_heifers:
              type: integer
            dead_bulls:
              type: integer
            dead_heifers:
              type: integer
            preg_rate_cows:
              type: number
            preg_rate_heifers:
              type: number
            reproduction_cows:
              type: integer
            reproduction_heifers:
              type: integer
            created_at:
              type: string
            updated_at:
              type: string
      404:
        description: Record not found
        schema:
          type: object
          properties:
            message:
              type: string
            errors:
              type: object
    """
    record = ReproductionRecordService.get_record_by_id(record_id)
    return jsonify(record.to_dict())

@records_bp.route('/', methods=['POST'])
def create_record():
    """
    Create a new reproduction record
    ---
    tags:
      - Records
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - farm_id
            - date
          properties:
            farm_id:
              type: integer
              description: ID of the farm
              example: 1
            date:
              type: string
              format: date
              description: Date of the record
              example: "2026-06-28"
            abort:
              type: integer
              default: 0
              minimum: 0
              description: Number of abortions
            bulls_from_cows:
              type: integer
              default: 0
              minimum: 0
            bulls_from_heifers:
              type: integer
              default: 0
              minimum: 0
            conception_cows:
              type: integer
              default: 0
              minimum: 0
            conception_heifers:
              type: integer
              default: 0
              minimum: 0
            cows_from_cows:
              type: integer
              default: 0
              minimum: 0
            cows_from_heifers:
              type: integer
              default: 0
              minimum: 0
            dead_bulls:
              type: integer
              default: 0
              minimum: 0
            dead_heifers:
              type: integer
              default: 0
              minimum: 0
            preg_rate_cows:
              type: number
              default: 0
              minimum: 0
              maximum: 100
              description: Pregnancy rate for cows (0-100)
            preg_rate_heifers:
              type: number
              default: 0
              minimum: 0
              maximum: 100
              description: Pregnancy rate for heifers (0-100)
            reproduction_cows:
              type: integer
              default: 0
              minimum: 0
            reproduction_heifers:
              type: integer
              default: 0
              minimum: 0
    responses:
      201:
        description: Record created
        schema:
          type: object
          properties:
            id:
              type: integer
            farm_id:
              type: integer
            farm_name:
              type: string
            date:
              type: string
              format: date
            abort:
              type: integer
            bulls_from_cows:
              type: integer
            bulls_from_heifers:
              type: integer
            conception_cows:
              type: integer
            conception_heifers:
              type: integer
            cows_from_cows:
              type: integer
            cows_from_heifers:
              type: integer
            dead_bulls:
              type: integer
            dead_heifers:
              type: integer
            preg_rate_cows:
              type: number
            preg_rate_heifers:
              type: number
            reproduction_cows:
              type: integer
            reproduction_heifers:
              type: integer
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
                date: ["Record for this farm and date already exists"]
    """
    try:
        schema = ReproductionRecordCreateSchema()
        data = schema.load(request.json)
        record = ReproductionRecordService.create_record(data)
        return jsonify(record.to_dict()), 201
    except ValidationError as e:
        raise AppError('Validation error', 400, e.messages)
    except ValueError as e:
        raise AppError('Invalid request', 400)

@records_bp.route('/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    """
    Update a reproduction record
    ---
    tags:
      - Records
    parameters:
      - name: record_id
        in: path
        type: integer
        required: true
        description: Record ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            farm_id:
              type: integer
              description: ID of the farm
            date:
              type: string
              format: date
              description: Date of the record
            abort:
              type: integer
              minimum: 0
            bulls_from_cows:
              type: integer
              minimum: 0
            bulls_from_heifers:
              type: integer
              minimum: 0
            conception_cows:
              type: integer
              minimum: 0
            conception_heifers:
              type: integer
              minimum: 0
            cows_from_cows:
              type: integer
              minimum: 0
            cows_from_heifers:
              type: integer
              minimum: 0
            dead_bulls:
              type: integer
              minimum: 0
            dead_heifers:
              type: integer
              minimum: 0
            preg_rate_cows:
              type: number
              minimum: 0
              maximum: 100
            preg_rate_heifers:
              type: number
              minimum: 0
              maximum: 100
            reproduction_cows:
              type: integer
              minimum: 0
            reproduction_heifers:
              type: integer
              minimum: 0
    responses:
      200:
        description: Record updated
        schema:
          type: object
          properties:
            id:
              type: integer
            farm_id:
              type: integer
            farm_name:
              type: string
            date:
              type: string
              format: date
            abort:
              type: integer
            bulls_from_cows:
              type: integer
            bulls_from_heifers:
              type: integer
            conception_cows:
              type: integer
            conception_heifers:
              type: integer
            cows_from_cows:
              type: integer
            cows_from_heifers:
              type: integer
            dead_bulls:
              type: integer
            dead_heifers:
              type: integer
            preg_rate_cows:
              type: number
            preg_rate_heifers:
              type: number
            reproduction_cows:
              type: integer
            reproduction_heifers:
              type: integer
            created_at:
              type: string
            updated_at:
              type: string
      400:
        description: Validation error
      404:
        description: Record not found
    """
    try:
        schema = ReproductionRecordSchema()
        data = schema.load(request.json, partial=True)
        record = ReproductionRecordService.update_record(record_id, data)
        return jsonify(record.to_dict())
    except ValidationError as e:
        raise AppError('Validation error', 400, e.messages)
    except ValueError as e:
        raise AppError('Invalid request', 400)

@records_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """
    Delete a reproduction record
    ---
    tags:
      - Records
    parameters:
      - name: record_id
        in: path
        type: integer
        required: true
        description: Record ID
    responses:
      204:
        description: Record deleted
      404:
        description: Record not found
        schema:
          type: object
          properties:
            message:
              type: string
            errors:
              type: object
    """
    ReproductionRecordService.delete_record(record_id)
    return '', 204

@records_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """
    Get aggregated statistics
    ---
    tags:
      - Statistics
    parameters:
      - name: farm_id
        in: query
        type: integer
        required: false
        description: Filter statistics by farm ID
      - name: date_from
        in: query
        type: string
        format: date
        required: false
        description: Filter statistics from this date
      - name: date_to
        in: query
        type: string
        format: date
        required: false
        description: Filter statistics to this date
    responses:
      200:
        description: Aggregated statistics
        schema:
          type: object
          properties:
            total_records:
              type: integer
              description: Total number of records
            total_abort:
              type: integer
              description: Total abortions
            total_dead_bulls:
              type: integer
              description: Total dead bulls
            total_dead_heifers:
              type: integer
              description: Total dead heifers
            avg_preg_rate_cows:
              type: number
              description: Average pregnancy rate for cows
            avg_preg_rate_heifers:
              type: number
              description: Average pregnancy rate for heifers
            total_bulls_from_cows:
              type: integer
              description: Total bulls from cows
            total_bulls_from_heifers:
              type: integer
              description: Total bulls from heifers
            total_cows_from_cows:
              type: integer
              description: Total cows from cows
            total_cows_from_heifers:
              type: integer
              description: Total cows from heifers
    """
    farm_id = request.args.get('farm_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    stats = ReproductionRecordService.get_statistics(
        farm_id=farm_id,
        date_from=date_from,
        date_to=date_to
    )
    return jsonify(stats)