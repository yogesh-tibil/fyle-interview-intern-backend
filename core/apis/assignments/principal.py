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
        
@principal_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(principal: dict) -> APIResponse:
    """Returns list of teachers"""
    try:
        teachers = Teacher.get_all_teachers()
        teachers_dump = TeacherSchema().dump(teachers, many=True)
        return APIResponse.respond(data=teachers_dump)
    except Exception as e:
        return APIResponse.error(message=str(e), status_code=500)

@principal_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(principal: dict, incoming_payload: dict) -> APIResponse:
    """Grade or re-grade an assignment"""
    try:
        assignment_id = incoming_payload['id']
        grade = incoming_payload['grade']
        assignment = Assignment.get_assignment_by_id(assignment_id)
        if assignment:
            assignment.grade = grade
            db.session.commit()
            assignment_dump = AssignmentSchema().dump(assignment)
            return APIResponse.respond(data=assignment_dump)
        else:
            return APIResponse.error(message='Assignment not found', status_code=404)
    except Exception as e:
        return APIResponse.error(message=str(e), status_code=500)
