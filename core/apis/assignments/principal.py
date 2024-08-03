# principal.py

from flask import Blueprint
from yourapp.decorators import authenticate_principal
from yourapp.models import Assignment, AssignmentSchema
from yourapp.responses import APIResponse

principal_resources = Blueprint('principal_resources', __name__)

@principal_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@authenticate_principal
def list_assignments(principal: dict) -> APIResponse:
    """Returns list of submitted and graded assignments"""
    try:
        assignments = Assignment.get_submitted_and_graded_assignments()
        assignments_dump = AssignmentSchema().dump(assignments, many=True)
        return APIResponse.respond(data=assignments_dump)
    except Exception as e:
        return APIResponse.error(message=str(e), status_code=500)
