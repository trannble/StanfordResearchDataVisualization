"""
File: report2.py
_______________
This file parses, sorts, calculates, and creates visual models of raw data from Stanford.
Model 1: "Stanford Engineering Percent of Women and Minority Faculty, 2010 - 2020"
Model 2: "Stanford Engineering Number of Professoriate Faculty By Race/Ethnicity"

Note: The raw data is not included.
Created by: Tran Le 12/14/20
"""

import matplotlib.pyplot as plt


KEY_FEMALE = "F"
KEY_MALE = "M"
FILE_NAME = "ideal_dashboard_data copy.csv"


def main():
    eng_data, total_headcount = read_file(FILE_NAME)

    model1_data = {
        "Women": 0,
        "Black or Afr. American": 0,
        "Asian": 0,
        "Hispanic": 0
    }
    update_model1_data(model1_data, eng_data, total_headcount)
    visualize_model(model1_data, "Stanford Engineering Percent of Women and Minority Faculty, 2010 - 2020")

    model2_data = {}
    for key in eng_data.keys():
        if key != KEY_FEMALE and key != KEY_MALE:
            model2_data[key] = 0
    update_model2_data(model2_data, eng_data)
    visualize_model(model2_data, f"Stanford Engineering Number of Professoriate Faculty By Race/Ethnicity, {total_headcount} ")


def visualize_model(model_data, title):
    """
    This function displays the data as bar graphs.

    :param model_data: the aggregated label and values
    :param title: title of bar graph
    :return: none
    """
    names = list(model_data.keys())
    values = list(model_data.values())
    fig, ax = plt.subplots()
    ax.bar(names, values)
    fig.suptitle(title)
    plt.show()


def update_model2_data(model2_data, eng_data):
    """
    This function updates the second model data.

    :param model2_data: the model2 calculated data
    :param eng_data: the entire data indexed
    :return: none, updates model2_data
    """
    for key, value in eng_data.items():
        if key in model2_data:
            model2_data[key] = eng_data[key]


def update_model1_data(model1_data, eng_data, total_headcount):
    """
    This function updates the first model data.

    :param model1_data: the model1 calculated data
    :param eng_data: the entire data indexed
    :param total_headcount: int
    :return: none, updates model1_data
    """
    model1_data["Women"] = eng_data[KEY_FEMALE]
    model1_data["Black or Afr. American"] = eng_data["Black/African American"]
    model1_data["Asian"] = eng_data["Asian"]
    model1_data["Hispanic"] = eng_data["Hispanic/Latino"]
    for key, value in model1_data.items():
        print(key, value)
        model1_data[key] = model1_data[key] / total_headcount * 100


def read_file(filename):
    """
    Reads the information from the specified file and indexes the information into a dictionary
    for later usage.

    Input:
        filename (str): name of the file holding Stanford demographics data of different groups (including faculty)
    :return: a dict with data on engineering faculty and the total number of engineering faculty
    """
    eng_data = {
        KEY_FEMALE: 0,
        KEY_MALE: 0
    }
    total_headcount = 0
    file = open(filename)
    next(file)
    for line in file:
        line = line.strip()
        data = line.split(',')
        if data[2] != "Professoriate Faculty":
            continue
        total_headcount = update_dicts_values(data, eng_data, total_headcount)
    return eng_data, total_headcount


def update_dicts_values(data, eng_data, total_headcount):
    """
    Populates the data passed in to the correct dictionary and bucket (sex & race/ethnicity).
    Performs various string parsing to check correct schools/other areas.
    :param data: the data of the current line
    :param eng_data: the dict of current year
    :param total_headcount: the total number of engineering faculty
    :return: the updated total_headcount
    """
    school = data[4]
    sex = data[5]
    race_ethnicity = data[3]
    headcount = data[7]
    if school == "School of Engineering":
        headcount = int(headcount)
        total_headcount += headcount
        eng_data[sex] += headcount
        if race_ethnicity not in eng_data:
            eng_data[race_ethnicity] = 0
        eng_data[race_ethnicity] += headcount
    return total_headcount


if __name__ == "__main__":
    main()