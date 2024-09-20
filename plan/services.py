
from plan.models import Memorize, Plan, memorizeDAO, planDAO
from word.models import Word, wordDAO
import db
@db.transactional
def create_plan(user_id, book_id, strategy, amount_per_day, phonetic):
    plan = Plan()
    plan.user_id = user_id
    plan.book_id = book_id
    plan.strategy = strategy
    plan.amount_per_day = amount_per_day
    plan.phonetic = phonetic
    default_plan = get_user_default_plan(user_id)
    if default_plan is None:
        plan.default = 1
    plan_id = planDAO.save(**plan.__dict__)
    return plan_id


def get_user_default_plan(user_id: int) -> Plan:
    _p = planDAO.find_default_by_user(user_id)
    if _p is not None:
        return Plan.from_db(*_p)

@db.transactional
def create_memorize(plan_id, word_id, familiarity) -> id:
    m = Memorize()
    m.plan_id = plan_id
    m.word_id = word_id
    m.familiarity = familiarity
    return memorizeDAO.save(**m.unbox())


def get_last_memorize(plan_id: int) -> Memorize:
    _m = memorizeDAO.find_last_by_plan(plan_id)
    if _m is not None:
        return Plan.from_db(*_m)


def get_familiar_set(user_id: int):
    plan = get_user_default_plan(user_id)
    book_guid = plan.book_id
    un = wordDAO.find_by_familiar(plan.id)
    data = list()
    amount_per_day = plan.amount_per_day
    if len(un) > 0:
        data.extend([Word.from_db(item) for item in data])
        start_index = un[-1][0]
    else:
        first = wordDAO.find_by_book_first(book_guid)
        word = Word.from_db(*first)
        start_index = word.id
    new_words = wordDAO.find_by_book_with_start(
        book_guid, start_index, amount_per_day)
    data.extend([Word.from_db(*item) for item in new_words])
    return data
