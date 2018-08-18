from answer.common.Data import qst
import difflib


def answer_query(question):
    question_temp = question;
    result = []
    result = dict(result)
    question = str(question[0]['itemstring']).replace('单选题:', '')
    for item in qst:
        apd = item, difflib.SequenceMatcher(a=question, b=item[0].replace('单选题：', '')).quick_ratio()
        if apd[1] > 0.8:
            for a in question_temp:
                aad = a, difflib.SequenceMatcher(a=apd[0][1], b=a['itemstring']).quick_ratio()
                if aad[1] > 0.8:
                    result['answer'] = aad[0]
                    break
                else:
                    continue
            break
        else:
            continue
    result['btn'] = question_temp[len(question_temp) - 1]
    return result
