from hashlib import new
from turtle import update
from xml.dom.minidom import parseString
from flask import Flask, jsonify, json, request
from flask_sqlalchemy import SQLAlchemy
import numpy as np

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///exercise.db"
db = SQLAlchemy(app)


# create the database model -> you will need to change this

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f'{self.id} {self.content}'


def todo_serializer(todo):
    return {
        'id': todo.id,
        'content': todo.content
    }


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mastery_SPrS = db.Column(db.Float)
    mastery_SPrP = db.Column(db.Float)
    mastery_SPaS = db.Column(db.Float)
    mastery_SPaP = db.Column(db.Float)
    mastery_verb = db.Column(db.Float)
    student_answers = db.Column(db.Text)
    exercises_made = db.Column(db.Text)

    def __str__(self):
        return f'{self.id} {self.mastery_SPrS} {self.mastery_SPrP} {self.mastery_SPaS} {self.mastery_SPaP} {self.mastery_verb} {self.student_answers} {self.exercises_made}'


def student_serializer(student):
    return {
        'id': student.id,
        'mastery_SPrS': student.mastery_SPrS,
        'mastery_SPrP': student.mastery_SPrP,
        'mastery_SPaS': student.mastery_SPaS,
        'mastery_SPaP': student.mastery_SPaP,
        'mastery_verb': student.mastery_verb,
        'student_answers': student.student_answers,
        'exercises_made': student.exercises_made
    }


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verb = db.Column(db.Text)
    instruction = db.Column(db.Text)
    exerciseContent_P1 = db.Column(db.Text)
    exerciseContent_P2 = db.Column(db.Text)
    exerciseContent_P3 = db.Column(db.Text)
    exerciseContent_P4 = db.Column(db.Text)
    exerciseContent_P5 = db.Column(db.Text)
    nbOfSkillsTested = db.Column(db.Integer)
    skill_A1 = db.Column(db.Text)
    skill_A2 = db.Column(db.Text)
    skill_A3 = db.Column(db.Text)
    skill_A4 = db.Column(db.Text)
    exerciseType = db.Column(db.Text)
    modelAnswer_A1 = db.Column(db.Text)
    modelAnswer_A2 = db.Column(db.Text)
    modelAnswer_A3 = db.Column(db.Text)
    modelAnswer_A4 = db.Column(db.Text)
    priorValue = db.Column(db.Float)

    def __str__(self):
        return f'{self.id} {self.verb} {self.instruction} {self.exerciseContent_P1} {self.exerciseContent_P2} {self.exerciseContent_P3} {self.exerciseContent_P4} {self.exerciseContent_P5} {self.nbOfSkillsTested} {self.skill_A1} {self.skill_A2} {self.skill_A3} {self.skill_A4} {self.exerciseType} {self.modelAnswer_A1} {self.modelAnswer_A2} {self.modelAnswer_A3} {self.modelAnswer_A4} {self.priorValue}'


def exercise_serializer(exercise):
    return {
        'id': exercise.id,
        'verb': exercise.verb,
        'instruction': exercise.instruction,
        'exerciseContent_P1': exercise.exerciseContent_P1,
        'exerciseContent_P2': exercise.exerciseContent_P2,
        'exerciseContent_P3': exercise.exerciseContent_P3,
        'exerciseContent_P4': exercise.exerciseContent_P4,
        'exerciseContent_P5': exercise.exerciseContent_P5,
        'nbOfSkillsTested': exercise.nbOfSkillsTested,
        'skill_A1': exercise.skill_A1,
        'skill_A2': exercise.skill_A2,
        'skill_A3': exercise.skill_A3,
        'skill_A4': exercise.skill_A4,
        'exerciseType': exercise.exerciseType,
        'modelAnswer_A1': exercise.modelAnswer_A1,
        'modelAnswer_A2': exercise.modelAnswer_A2,
        'modelAnswer_A3': exercise.modelAnswer_A3,
        'modelAnswer_A4': exercise.modelAnswer_A4,
        'priorValue': exercise.priorValue
    }


def answer_serializer(answer):
    print('wat we binnekrijgen in de serializer', answer)
    return {
        'exercise': answer.exercise
    }


@app.route('/api', methods=['GET'])
def index():
    # todo = Todo.query.all()
    return jsonify([*map(todo_serializer, Todo.query.all())])


@app.route('/studentInfo', methods=['GET'])
def students():
    # todo = Todo.query.all()
    return jsonify([*map(student_serializer, Student.query.all())])


@app.route('/exercises', methods=['GET'])
def showExercises():
    return jsonify([*map(exercise_serializer, Exercise.query.all())])


@app.route('/exercises/<int:targetID>', methods=['GET'])
def showSpecificExercise(targetID):
    # completeList = jsonify([*map(exercise_serializer,Exercise.query.all())])
    completeList = Exercise.query.all()
    result = None
    for exercise in completeList:
        print(exercise.id)
        if exercise.id == targetID:
            result = exercise
    return jsonify(exercise_serializer(result))


# include making the studentAnswer list empty

@app.route('/answers', methods=['POST'])
def updateAnswers():
    request_data = request.data
    print(request_data)
    return jsonify(request_data)


@app.route('/studentInfo', methods=['PUT'])
def redirectToFunction():
    content = json.loads(request.data)['content']
    TRSon = json.loads(request.data)['recommender']
    print('content= ', content)
    print('TRSon=', TRSon)
    if (content == 'initialization' and TRSon == True):
        print('reset student model for AFRS')
        initializeStudentInfo_AFRS()
        res = 'student initialization finished'
    elif (content == 'initialization' and TRSon == False):
        print('reset student model for TRS')
        initializeStudentInfo_TRS()
        res = 'student initialization finished'
    else:
        print('student answers received and next ex id is being calculated...')
        res = int(updateStudentWithAnswers(TRSon))

    return jsonify(answer=res)


def initializeStudentInfo_AFRS():
    student = Student.query.filter_by(id=1).first()
    student.student_answers = ""
    student.exercises_made = "4"
    student.mastery_SPaP = 0.5
    student.mastery_SPaS = 0.5
    student.mastery_SPrP = 0.5
    student.mastery_SPrS = 0.5
    student.mastery_verb = 0.5
    db.session.commit()
    print('student initialization finished')


def initializeStudentInfo_TRS():
    student = Student.query.filter_by(id=1).first()
    student.student_answers = ""
    student.exercises_made = "16"
    student.mastery_SPaP = 0.5
    student.mastery_SPaS = 0.5
    student.mastery_SPrP = 0.5
    student.mastery_SPrS = 0.5
    student.mastery_verb = 0.5
    db.session.commit()
    print('student initialization finished')


def updateStudentWithAnswers(TRSon):
    latest_answer = listToStr(json.loads(request.data)['content'])
    student = Student.query.filter_by(id=1).first()
    student.student_answers = latest_answer
    print('student answer part should be updated now to: ', student.student_answers)
    db.session.commit()
    if TRSon == False:
        nextExerciseID = calculateNextExercise_withAFRS(student)
    else:
        nextExerciseID = calculateNextExercise_withTRS(student)
    # calculate next exercise here and pass in body back to the front-end
    print('comitted')
    # answer_dct = {'exercise': nextExerciseID}
    # print('wat we uit het put request doorgeven', answer_dct)
    return nextExerciseID


def calculateNextExercise_withAFRS(student):
    print('################### CALCULATE NEXT EXERCISE STARTED WITH AFRS ################\n')
    print('1. SELECT ID FROM LAST EXERCISE \n')
    id_last_ex = selectIdLastExercise(student)
    print('The id from the last exercise =   ', id_last_ex, "\n")
    print('2. EXTRACT MODEL ANSWERS AND SKILLS FROM LAST EXERCISE \n')
    model_answers_ex = extractModelAnswers(id_last_ex)
    print('model_answers from this last exercise are =', model_answers_ex, "\n")
    skills_ex = extractSkills(id_last_ex)
    print('skills from this last exercise are =', skills_ex)
    # [True, False, True] -> [1,0,1]
    print('3. CHECK STUDENT ANSWERS\n')
    answers_checked = check_answers(model_answers_ex, student.student_answers)
    print('checked student answers are:', answers_checked)
    upd_student = updateSkillLevels(
        student, id_last_ex, answers_checked, skills_ex)
    mastered_subskills, unmastered_subskills = extractMasteryOfSubskills(
        upd_student)
    print("\n4. EXAMINATION OF STUDENT MASTERY\n")
    print('the mastered subskills from the student are = ', mastered_subskills)
    print('the unmastered subskills from the student are = ', unmastered_subskills)
    recommendation_type, selected_skill, scope = extractRecommendationScope_AFRS(
        mastered_subskills, unmastered_subskills)
    print('the type of exercise the RS will recommmend is = ', recommendation_type)
    print('the selected skill targeted to improve is', selected_skill)
    print('the scope of allowed skills for the next exercise are', scope, "\n")
    print('5.ID NEXT EXERCISE CALCULATION\n')
    id_next_ex = calculatePossibleIDWithinScope_AFRS(
        scope, recommendation_type, upd_student, selected_skill)
    print('\n6.UPDATE STUDENT ANSWER LIST\n')
    new_list_ex_made = upd_student.exercises_made + "," + str(id_next_ex)
    print('new list of exercises made is ', new_list_ex_made)
    student.exercises_made = new_list_ex_made
    # line below still needs to be uncommented
    db.session.commit()
    print(id_next_ex)
    return id_next_ex


def calculateNextExercise_withTRS(student):
    print('################### CALCULATE NEXT EXERCISE STARTED WITH TRS ################\n')
    print('1. SELECT ID FROM LAST EXERCISE \n')
    id_last_ex = selectIdLastExercise(student)
    print('The id from the last exercise =   ', id_last_ex, "\n")
    print('2. EXTRACT MODEL ANSWERS AND SKILLS FROM LAST EXERCISE \n')
    model_answers_ex = extractModelAnswers(id_last_ex)
    print('model_answers from this last exercise are =', model_answers_ex, "\n")
    skills_ex = extractSkills(id_last_ex)
    print('skills from this last exercise are =', skills_ex)
    print('3. CHECK STUDENT ANSWERS\n')
    answers_checked = check_answers(model_answers_ex, student.student_answers)
    print('checked student answers are:', answers_checked)
    upd_student = updateSkillLevels(
        student, id_last_ex, answers_checked, skills_ex)
    mastered_subskills, unmastered_subskills = extractMasteryOfSubskills(
        upd_student)
    print("\n4. EXAMINATION OF STUDENT MASTERY\n")
    print('the mastered subskills from the student are = ', mastered_subskills)
    print('the unmastered subskills from the student are = ', unmastered_subskills)
    all_mastered = checkAllSubskillsMastered(
        mastered_subskills, unmastered_subskills)
    if all_mastered == False:
        selected_skill, scope = extractRecommendationScope_TRS(
            mastered_subskills, unmastered_subskills)
        print('selected skill = ', selected_skill)
        id_next_ex = calculatePossibleIDWithinScope_notAllMastered_TRS(
            scope, upd_student, selected_skill)
    else:
        id_next_ex = calculatePossibleIDWithinScope_AllMastered_TRS(
            upd_student)
    print('\n6.UPDATE STUDENT ANSWER LIST\n')
    new_list_ex_made = upd_student.exercises_made + "," + str(id_next_ex)
    print('new list of exercises made is ', new_list_ex_made)
    student.exercises_made = new_list_ex_made
    # line below still needs to be uncommented
    db.session.commit()
    print(id_next_ex)
    return id_next_ex


def calculatePossibleIDWithinScope_AFRS(scope, recommendation_type, student, selected_skill):
    if recommendation_type == "example":
        possible_ID_list = recommendExample_AFRS(
            scope, student, recommendation_type, selected_skill)

        perm_list = np.random.permutation(possible_ID_list)
        id_next = perm_list[0]
        print('id_next = ', id_next)
    else:
        possible_ID_list = recommendProblem(student)
        perm_list = np.random.permutation(possible_ID_list)
        id_next = perm_list[0]
    return id_next


def calculatePossibleIDWithinScope_notAllMastered_TRS(scope, student, selected_skill):
    possible_ID_list = recommendForSkillLearning(
        scope, student, selected_skill)
    perm_list = np.random.permutation(possible_ID_list)
    id_next = perm_list[0]
    print('id_next = ', id_next)
    return id_next


def recommendForSkillLearning(scope, student, selected_skill):
    # 1. select all exercises with verb = to be en type example and make dictionary
    ids_verb_skills_dict = extractExercisesMatchingVerbAndType_TRS()

    # 2.remove id's from which the skills are out of scope
    ids_in_scope_list = removeExercisesOutOfScope(
        ids_verb_skills_dict, scope, selected_skill)

    # 3.remove id's from which the key is in already made exercises
    list_in_scope_not_made = removeExercisesAlreadyMade(
        ids_in_scope_list, strToList(student.exercises_made))

    return list_in_scope_not_made


def recommendExample_AFRS(scope, student, recommendation_type, selected_skill):
    # 1. select all exercises with verb = to be en type example and make dictionary
    #  with as key the id and as value a list of skills -> might be better to place this outside the function bcs
    # it is always the same and otherwise not scalable
    ids_verb_skills_dict = extractExercisesMatchingVerbAndType_AFRS(
        recommendation_type)
    # 2. remove id's from which the skills are out of scope
    ids_in_scope_list = removeExercisesOutOfScope(
        ids_verb_skills_dict, scope, selected_skill)

    # 3.remove id's from which the key is in already made exercises
    list_in_scope_not_made = removeExercisesAlreadyMade(
        ids_in_scope_list, strToList(student.exercises_made))

    return list_in_scope_not_made


def recommendProblem(student):
    list_problem_ids = extractProblemIDs()
    print('the list of IDS from the database with type problem are= ', list_problem_ids)
    not_made_list_problem_ids = removeExercisesAlreadyMade(
        list_problem_ids, strToList(student.exercises_made))
    print('the list of problem IDS not made by the student are= ',
          not_made_list_problem_ids)
    return not_made_list_problem_ids


def calculatePossibleIDWithinScope_AllMastered_TRS(student):
    list_ids_to_have = extractAllIDs()
    print('the list of IDS from the database are= ', list_ids_to_have)
    not_made_list_problem_ids = removeExercisesAlreadyMade(
        list_ids_to_have, strToList(student.exercises_made))
    print('the list of problem IDS not made by the student are= ',
          not_made_list_problem_ids)
    perm_list = np.random.permutation(not_made_list_problem_ids)
    id_next = perm_list[0]
    print('id_next = ', id_next)
    return id_next


def extractAllIDs():
    id_list = []
    complete_list = Exercise.query.all()
    for exercise in complete_list:
        if (exercise.verb == 'to have'):
            id_list.append(exercise.id)
    return id_list


def extractProblemIDs():
    id_list = []
    complete_list = Exercise.query.all()
    for exercise in complete_list:
        if (exercise.exerciseType == 'problem' and exercise.verb == 'to be'):
            id_list.append(exercise.id)
    return id_list


def removeExercisesAlreadyMade(proposal_list, already_made_list):
    print('exercises already made = ', already_made_list)
    not_made_list = []
    for i in range(0, len(proposal_list)):
        if str(proposal_list[i]) not in already_made_list:
            not_made_list.append(proposal_list[i])
    print('exercises not yet made = ', not_made_list)
    return not_made_list


def removeExercisesOutOfScope(all_dict, scope, selected_skill):
    removal_list = []
    for id in all_dict:
        skills = all_dict.get(id)
        if checkOutOfScope(scope, skills, selected_skill) == True:
            print('exercise with scope = ', scope, "and skills = ",
                  skills, "are not in scope of eachother")
            removal_list.append(id)

    for i in removal_list:
        del all_dict[i]
    print("dictionary after removing out of scope=", list(all_dict.keys()))
    return list(all_dict.keys())


def checkOutOfScope(scope, skills, selected_skill):
    boolOutOfScope = False
    for skill in skills:
        if skill not in scope:
            boolOutOfScope = True
    if selected_skill not in skills:
        boolOutOfScope = True
    return boolOutOfScope


def extractExercisesMatchingVerbAndType_AFRS(recommendation_type):
    result_dict = {}
    complete_list = Exercise.query.all()
    for exercise in complete_list:
        if (exercise.exerciseType == recommendation_type and exercise.verb == 'to be'):
            skill_set = extractSkills(exercise.id)
            result_dict.update({exercise.id: skill_set})
    print('the resulting dictionary will be= ', result_dict.items())
    return result_dict


def extractExercisesMatchingVerbAndType_TRS():
    result_dict = {}
    complete_list = Exercise.query.all()
    for exercise in complete_list:
        if (exercise.verb == 'to have'):
            skill_set = extractSkills(exercise.id)
            result_dict.update({exercise.id: skill_set})
    print('the resulting dictionary will be= ', result_dict.items())
    return result_dict


def extractRecommendationScope_AFRS(mastered_subskills, unmastered_subskills):
    """ 
    This method is used to extract the scope of the next recommended exercise. This includes the type of exercise the student needs to make,
    the selected skill to be tested and the skills that are allowed to be in the next recommended exercise.
    """
    if len(unmastered_subskills) == 0:
        type = "problem"
        skill = "mastery_verb"
        scope = mastered_subskills + [skill]
    else:
        type = "example"
        skill = unmastered_subskills[0]
        scope = mastered_subskills + [skill]
    return type, skill, scope


def extractRecommendationScope_TRS(mastered_subskills, unmastered_subskills):
    skill = unmastered_subskills[0]
    scope = mastered_subskills + [skill]
    return skill, scope


def checkAllSubskillsMastered(mastered_subskills, unmastered_subskills):
    if len(unmastered_subskills) == 0:
        all_mastered = True
    else:
        all_mastered = False
    return all_mastered


def extractMasteryOfSubskills(upd_student, exp_mastery_level=0.7):
    result_mastered_subskills = []
    result_unmastered_subskills = []
    # mastery of SPrS
    if upd_student.mastery_SPrS > 0.7:
        result_mastered_subskills.append('mastery_SPrS')
    else:
        result_unmastered_subskills.append('mastery_SPrS')

    # mastery of SPrP
    if upd_student.mastery_SPrP > 0.7:
        result_mastered_subskills.append('mastery_SPrP')
    else:
        result_unmastered_subskills.append('mastery_SPrP')

    # mastery of SPaS
    if upd_student.mastery_SPaS > 0.7:
        result_mastered_subskills.append('mastery_SPaS')
    else:
        result_unmastered_subskills.append('mastery_SPaS')

    # mastery of SPaP
    if upd_student.mastery_SPaP > 0.7:
        result_mastered_subskills.append('mastery_SPaP')
    else:
        result_unmastered_subskills.append('mastery_SPaP')

    return result_mastered_subskills, result_unmastered_subskills


# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     mastery_SPrS = db.Column(db.Float)
#     mastery_SPrP = db.Column(db.Float)
#     mastery_SPaS = db.Column(db.Float)
#     mastery_SPaP = db.Column(db.Float)
#     mastery_verb = db.Column(db.Float)
#     student_answers = db.Column(db.Text)
#     exercises_made = db.Column(db.Text)

def updateSkillLevels(student, ex_id, results, skills_list, update_rate=0.05):
    ex_type = extractExerciseType(ex_id)
    if ex_type == 'example':
        print('we are going to update with the example procedure')
        student = updateSubskills(student, results, skills_list, update_rate)
    else:
        print('we are going to update with the problem procedure')
        student = updateSubskills(student, results, skills_list, update_rate)
        student = updateSkill(student, results, update_rate)
    return student


def updateSubskills(student, results, skills_list, update_rate):
    for i in range(0, len(results)):
        if results[i] == 0:
            if skills_list[i] == 'mastery_SPrS':
                student = decrease_mastery_SPrS(student, update_rate)
            elif skills_list[i] == 'mastery_SPrP':
                student = decrease_mastery_SPrP(student, update_rate)
            elif skills_list[i] == 'mastery_SPaS':
                student = decrease_mastery_SPaS(student, update_rate)
            else:
                student = decrease_mastery_SPaP(student, update_rate)
        else:
            if skills_list[i] == 'mastery_SPrS':
                student = increase_mastery_SPrS(student, update_rate)
            elif skills_list[i] == 'mastery_SPrP':
                student = increase_mastery_SPrP(student, update_rate)
            elif skills_list[i] == 'mastery_SPaS':
                student = increase_mastery_SPaS(student, update_rate)
            else:
                student = increase_mastery_SPaP(student, update_rate)
    return student


def updateSkill(student, results, update_rate):
    allCorrect = checkAllCorrect(results)
    if allCorrect == True:
        print("all questions are answered correctly")
        student = increase_mastery_verb(student, update_rate)
    else:
        student = decrease_mastery_verb(student, update_rate)
    return student


def checkAllCorrect(ans_list):
    boolAllCorrect = True
    for i in range(0, len(ans_list)):
        if ans_list[i] == 0:
            boolAllCorrect = False
    return boolAllCorrect


def increase_mastery_verb(student, update_rate):
    prev_mastery = student.mastery_verb
    new_mastery = min(1, prev_mastery + update_rate)
    student.mastery_verb = new_mastery
    print("skill : mastery_verb increased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def decrease_mastery_verb(student, update_rate):
    prev_mastery = student.mastery_verb
    new_mastery = min(1, prev_mastery - update_rate)
    student.mastery_verb = new_mastery
    print("skill : mastery_verb decreased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def increase_mastery_SPrS(student, update_rate):
    prev_mastery = student.mastery_SPrS
    new_mastery = min(1, prev_mastery + update_rate)
    student.mastery_SPrS = new_mastery
    print("skill : mastery_SPrS increased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def decrease_mastery_SPrS(student, update_rate):
    prev_mastery = student.mastery_SPrS
    new_mastery = min(1, prev_mastery - update_rate)
    student.mastery_SPrS = new_mastery
    print("skill : mastery_SPrS decreased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def increase_mastery_SPrP(student, update_rate):
    prev_mastery = student.mastery_SPrP
    new_mastery = min(1, prev_mastery + update_rate)
    student.mastery_SPrP = new_mastery
    print("skill : mastery_SPrP increased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def decrease_mastery_SPrP(student, update_rate):
    prev_mastery = student.mastery_SPrP
    new_mastery = min(1, prev_mastery - update_rate)
    student.mastery_SPrP = new_mastery
    print("skill : mastery_SPrP decreased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def increase_mastery_SPaS(student, update_rate):
    prev_mastery = student.mastery_SPaS
    new_mastery = min(1, prev_mastery + update_rate)
    student.mastery_SPaS = new_mastery
    print("skill : mastery_SPaS increased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def decrease_mastery_SPaS(student, update_rate):
    prev_mastery = student.mastery_SPaS
    new_mastery = min(1, prev_mastery - update_rate)
    student.mastery_SPaS = new_mastery
    print("skill : mastery_SPaS decreased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def increase_mastery_SPaP(student, update_rate):
    prev_mastery = student.mastery_SPaP
    new_mastery = min(1, prev_mastery + update_rate)
    student.mastery_SPaP = new_mastery
    print("skill : mastery_SPaP increased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def decrease_mastery_SPaP(student, update_rate):
    prev_mastery = student.mastery_SPaP
    new_mastery = min(1, prev_mastery - update_rate)
    student.mastery_SPaP = new_mastery
    print("skill : mastery_SPaP decreased from" +
          str(prev_mastery) + "to" + str(new_mastery))
    db.session.commit()
    return student


def extractExerciseType(id):
    inv_exercise = Exercise.query.filter_by(id=id).first()
    exercise_type = inv_exercise.exerciseType.strip()
    print("the type of the exercise with id = " +
          str(id) + "is " + exercise_type + "\n")
    return exercise_type


def strToList(student_ans):
    res_splitted = student_ans.split(",")
    return res_splitted


def check_answers(model_ans, student_ans):
    student_ans_list = removeWhitespaces(
        list(filter(None, strToList(student_ans))))
    result = []
    # print('len student answers', len(student_ans_list))
    print('student answers are ', student_ans_list)

    for i in range(0, len(student_ans_list)):
        # print('now checking index= ', i)
        if model_ans[i] == student_ans_list[i]:
            # print('added 1')
            result.append(1)
        else:
            # print('added 0')
            result.append(0)
    return result


def selectIdLastExercise(student):
    str_stud_ex_made = student.exercises_made
    list_stud_ex_made = removeWhitespaces(str_stud_ex_made.split(","))
    print('complete list from all exercises made by the student= ', list_stud_ex_made)
    id_last_exercise = int(list_stud_ex_made.pop())
    return id_last_exercise


def removeWhitespaces(list):
    for i in range(0, len(list)):
        inv_value = list[i]
        # print("investigated value", inv_value)
        new_val = inv_value.strip()
        # print('new value=', new_val)
        list[i] = new_val
    return list


def extractModelAnswers(id):
    inv_exercise = Exercise.query.filter_by(id=id).first()
    model_answer_1 = inv_exercise.modelAnswer_A1
    model_answer_2 = inv_exercise.modelAnswer_A2
    model_answer_3 = inv_exercise.modelAnswer_A3
    model_answer_4 = inv_exercise.modelAnswer_A4
    result = [model_answer_1, model_answer_2, model_answer_3, model_answer_4]
    # result = ['test', 'tset', '', '']
    # print('resutling list= ', result)
    # print('type of resutling list= ', type(result))
    adj_res = removeWhitespaces(list(filter(None, result)))
    return adj_res


def extractSkills(id):
    inv_exercise = Exercise.query.filter_by(id=id).first()
    skill_answer_1 = inv_exercise.skill_A1
    skill_answer_2 = inv_exercise.skill_A2
    skill_answer_3 = inv_exercise.skill_A3
    skill_answer_4 = inv_exercise.skill_A4
    result = [skill_answer_1, skill_answer_2, skill_answer_3, skill_answer_4]
    adj_res = removeWhitespaces(list(filter(None, result)))
    return adj_res


def listToStr(list):
    """
    SQL Alchemy is not accepting lists in as type TEXT, so therefore lists need to be reformatted.
    """
    result = list[0] + "," + list[1] + "," + list[2] + "," + list[3]
    return result


if __name__ == '__main__':
    app.run(debug=True)
