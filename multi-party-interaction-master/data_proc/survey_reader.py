import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
import seaborn as sns
import csv
sns.set(style="darkgrid")
plt.rcParams['font.size'] = 8.0


# csv file name
filename = "/home/chris/USC/multi-party/surveys.csv"

"""File Structure:
Ln1 Unique ID
Ln2 Question
Ln4->83 Participants
"""
data_by_question = pd.read_csv(filename, header=1)
data_by_code = pd.read_csv(filename, header=0, skiprows=[1])

# Map of Q codes to questions (e.g. question_map['Q1']='Gender')
question_map = pd.read_csv(filename, header=0, nrows=1, squeeze=True).to_dict(orient='records')


###########################
# Demographic Visualization
###########################
def demographics():
    # data_by_question["age"] = data_by_question["Q1"].astype("category")
    # table = pd.pivot_table(data_by_question, index=["Q1"], columns=["Q3"], values=["Q2"], aggfunc='mean'
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    data_by_question.groupby('Ethnic Background (check all that apply) - Selected Choice').size().plot.pie(ax=ax1)
    data_by_question.groupby('Gender').size().plot.pie(ax=ax2)
    data_by_question.groupby('Age').size().plot.bar(ax=ax3)
    data_by_question.groupby('Highest Education Received').size().plot.pie(ax=ax4)
    # plt.show()
    ["Q1", "Q2", "Q3", "Q6", "Q8_1", "Q32"]


##################################################
# Basic Survey Scoring
##################################################
"""
Arguments:
    questions: a list of questions to read
        e.g. ["Q1", "Q2", "Q3", "Q6", "Q8_1", "Q32"]
    answers: a list of potential answers to look through
        e.g. ['Strongly Disagree', 'Disagree', 'Undecided', 'Agree', 'Strongly Agree']
    subscales: an optional list of subscales within the questions
        e.g. [[1,3,5],[2.4.6]] # starts at 1
    data: The csv mapped by Q code

Returns:
    scores: the total score of each participant across all questions, normalized to zero and averaged
    subscores: the scores for each subscore
"""


def score(questions, answers, reverse_questions, subscales=[], data=data_by_code, missing='fill'):
    scores_list = []
    if subscales:
        print("there are %d scales" % len(subscales))
        subscores_lists = [[] for i in range(len(subscales))]
        print(subscores_lists)
    for index, participant in data_by_code.iterrows():

        # reset score counters
        score_total = 0
        if subscales:
            subscores_total = [0 for i in range(len(subscales))]

        # Convert written answers to cumulative scores
        for question in questions:
            answer = participant[question]
            if answer not in answers:
                if missing == 'fill':
                    answer = answers[(len(answers) - 1) / 2]  # Will not work if len of answers not odd

            # Normalize score around center value
            q_score = (answers.index(answer)) - ((len(answers) - 1) / 2)  # e.g. 'strongly agree' = (4+1 - (5-1)/2) = 3
            # print(q_score)
            # Add to total and normalize
            question_index = questions.index(question) + 1
            if question_index in reverse_questions:
                q_score = q_score * -1

            score_total += (float(q_score) / len(questions))

            if subscales:
                for i in range(len(subscales)):
                    if question_index in subscales[i]:
                        subscores_total[i] += float(q_score)

        scores_list.append(score_total)
        if subscales:
            for i in range(len(subscales)):
                subscores_lists[i].append(subscores_total[i] / len(subscales[i]))

    if subscales:
        return (scores_list, subscores_lists)
    return (scores_list)


##################################################
# Basic Histogram Visuals
##################################################
"""
Arguments:
    scores: main scores
    title: main title
    subscores: list of subscores
    titles: list of subscore titles
"""


def visualize_hist(scores, title, subscores=[], titles=[], bin_size=20, range_vals=[-2, 2]):
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle(title)

    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    (mu, sigma) = norm.fit(scores)
    n, bins, patches = ax1.hist(scores, bins=bin_size, range=range_vals)
    y = mlab.normpdf(bins, mu, sigma)
    ax1.plot(bins, y, 'r--', linewidth=2)

    ax2.hist(subscores[0], bins=bin_size, range=range_vals)
    ax3.hist(subscores[1], bins=bin_size, range=range_vals)
    ax4.hist(subscores[2], bins=bin_size, range=range_vals)
    ax1.title.set_text('Total Score')
    ax2.title.set_text(titles[0])
    ax3.title.set_text(titles[1])
    ax4.title.set_text(titles[2])


###########################
# Scoring NARS
###########################


def scoring_nars():
    questions = ['Q15_' + str(i) for i in range(1, 14 + 1)]
    subscale_1 = [4, 7, 8, 9, 10, 12]   # Negative Attitudes toward Situations and Interactions with Robots
    subscale_2 = [1, 2, 11, 13, 14]     # Negative Attitudes toward Social Influence of Robots,
    subscale_3 = [3, 5, 6]              # Negative Attitudes toward Emotions in Interaction with Robots
    answers = ['Strongly Disagree', 'Disagree', 'Undecided', 'Agree', 'Strongly Agree']
    r = [3, 5, 6]
    subscales = [subscale_1, subscale_2, subscale_3]
    NARS_scores, subscores = score(questions, answers, r, subscales=subscales)
    [NARS_sub_1, NARS_sub_2, NARS_sub_3] = subscores

    title = 'NARS Histogram (Higher -> More Negative Attitudes)'
    titles = ['Negative Attitudes Towards Situations and Interactions with Robots', 'Negative Attitudes Towards Social Influence of Robots', 'Negative Attitudes Towards Emotions in Interaction with Robots']

    visualize_hist(NARS_scores, title, subscores=subscores, titles=titles)


##################
# Scoring Trust
##################
def scoring_trust(section):
    answers = ['Strongly Disagree', 'Disagree', 'Somewhat Disagree', 'Neither Agree nor Disagree', 'Somewhat Agree' 'Agree', 'Strongly Agree']  # Higher scores indicate a more negative attitude
    robot_trust_questions = [section + str(i) for i in range(1, 33 + 1)]     # 'Q18_1' ->'Q18_33'
    subscale_1 = [i for i in range(1, 6 + 1)]
    subscale_2 = [i for i in range(6 + 1, 13 + 1)]
    subscale_3 = [i for i in range(13 + 1, 33 + 1)]
    r = [2, 4, 6, 7, 8, 12, 14, 18]
    subscales = [subscale_1, subscale_2, subscale_3]
    scores, subscores = score(robot_trust_questions, answers, r, subscales=subscales)
    [sub_1, sub_2, sub_3] = subscores

    title = 'Robot Trust Histogram (Higher -> More Trusting Attitudes)'
    titles = ['Custom Questions', 'Survey 1', 'Survey 2']

    visualize_hist(scores, title, subscores=subscores, titles=titles)


def main():
    scoring_nars()
    scoring_trust('Q18_')
    scoring_trust('Q56_')
    plt.show()


main()
