import json
import os



def names_of_registered_students(input_json_path, course_name):
    """
    This function returns a list of the names of the students who registered for
    the course with the name "course_name".

    :param input_json_path: Path of the students database json file.
    :param course_name: The name of the course.
    :return: List of the names of the students.
    """
    list_of_students = []

    with open(input_json_path, 'r') as f:
        student_dict = json.load(f)

    for student_id in student_dict.keys():
        if course_name in student_dict[student_id]['registered_courses']:
            list_of_students.append(student_dict[student_id]['student_name'])

    return list_of_students
    pass


def enrollment_numbers(input_json_path, output_file_path):
    """
    This function writes all the course names and the number of enrolled
    student in ascending order to the output file in the given path.

    :param input_json_path: Path of the students database json file.
    :param output_file_path: Path of the output text file.
    """
    with open(input_json_path, 'r') as f:
        student_dict = json.load(f)
    
    enrollment_numbers_dict = {}
    for key in student_dict.keys():
        list_of_courses = student_dict[key]["registered_courses"]
        for course in list_of_courses:
            if course in enrollment_numbers_dict:
                enrollment_numbers_dict[course] = enrollment_numbers_dict[course] + 1
            else:
                enrollment_numbers_dict[course] = 1
    
    # lexographic order sorting
    #lexographic_order_dict = sorted(enrollment_numbers_dict)
    with open(output_file_path, 'w') as f:
        #f.write('"{key}" {enroll}\n'.format(key=key, enroll=enrollment_numbers_dict[key]))
        course_str = json.dumps(enrollment_numbers_dict, sort_keys=True, separators=('\n', ' '), allow_nan=False)
        f.write(course_str[1:len(course_str) - 1] + "\n")

    pass



def courses_for_lecturers(json_directory_path, output_json_path):
    """
    This function writes the courses given by each lecturer in json format.

    :param json_directory_path: Path of the semsters_data files.
    :param output_json_path: Path of the output json file.
    """
    dict_of_courses = { }

    list_of_files = os.listdir(json_directory_path)
    num_of_files = len(list_of_files)

    dict_courses_per_semester = {}

    for filename in list_of_files:
        if filename.endswith(".json"):
            with open(os.path.join(json_directory_path, filename), 'r') as f:
                dict_courses_per_semester[filename] = json.load(f)

    first_semester = list(dict_courses_per_semester.keys())[0]
    dict_of_every_sem_courses = dict_courses_per_semester[first_semester]

    for semester in dict_courses_per_semester:
        for course in dict_courses_per_semester[semester]:
            if course in dict_of_every_sem_courses:
                this_semester_lec = dict_courses_per_semester[semester][course]["lecturers"]
                permament_lectures = dict_of_every_sem_courses[course]["lecturers"]
                for lecture in permament_lectures:
                    if lecture not in this_semester_lec:
                        dict_of_every_sem_courses[course]["lecturers"].remove(lecture)
            else:
                dict_of_every_sem_courses[course] = dict_courses_per_semester[semester][course]


    dict_lecturers = { }

    for course in dict_of_every_sem_courses:
        for lecture in dict_of_every_sem_courses[course]["lecturers"]:
            if lecture not in dict_lecturers:
                dict_lecturers[lecture] = [dict_of_every_sem_courses[course]["course_name"]]
            else:
                dict_lecturers[lecture].append(dict_of_every_sem_courses[course]["course_name"])
    
    with open(output_json_path, 'w') as f:
        json.dump(dict_lecturers, f, separators=(',\n', ': '))
            

    pass


