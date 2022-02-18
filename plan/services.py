

from plan.models import Plan, planDAO 

def create_plan():
    plan = Plan()
    plan.user_id = user_id
    plan.book_id = book_id
    planDAO.save(plan)