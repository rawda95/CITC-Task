import random


def chpter_init(questions):
    rd = []
    ud = []
    cd = []
    rs = []
    us = []
    cs = []
    for q in questions:

        if q.difficulty == 'D':

            if q.objective == 'R':
                rd.append(q)
            elif q.objective == 'U':
                ud.append(q)
            elif q.objective == 'C':
                cd.append(q)
        elif q.difficulty == 'S':
            if q.objective == 'R':
                rs.append(q)
            elif q.objective == 'U':
                us.append(q)
            elif q.objective == 'C':
                cs.append(q)
    d = [rd, ud, cd]
    s = [rs, us, cs]
    return [d, s]


def gen_exam(questions, num_of_objective):
    # make list for question [[d[u],[r],[c]],[s[u],[r],[c]]]
    questions = chpter_init(questions)
    r = []
    # for D and S
    num_of_objective_div = [i // 2 for i in num_of_objective]
    # random question for exam
    for i in range(len(questions)):
        a = [[], [], []]
        #print('num_of_objective_div', len(num_of_objective_div))
        for j in range(len(questions[i])):
            if questions[i][j]:
                a[j] = (random.sample(questions[i][j], int(num_of_objective_div[j])))
        r.append(a)
    # union lists
    result = []
    for i in range(3):
        a = r[0][i] + r[1][i]
        result.append(a)
    # add reminder
    for i in range(len(result)):
        if len(result[i]) < num_of_objective[i]:
            reminde = num_of_objective[i] - len(result[i])
            #  print('reminder', reminde)
            for j in range(reminde):
                if questions[0][i] or questions[1][i]:
                    q_all = questions[0][i] + questions[1][i]
                    while True:
                        q = random.sample(q_all, 1)
                        if not q in result[i]:
                            # print(result[i])
                            # print(q)
                            result[i].append(q[0])
                            break


    return result
