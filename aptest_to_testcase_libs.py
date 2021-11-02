__author__ = 'Pradeep Mondal P'

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# used to get current root directory
from scripts.lib.common_api_and_ui.logging import root_dir


# library used to search nearest matched string/substring
from fuzzywuzzy import process

# using Porter 2 or Snowball stemmer library for stemming
from nltk.stem.snowball import SnowballStemmer

# main dictionary
from inputs.tools.aptest_to_testcase_converter.database.hashtable.aptest_constant_hashtable import aptest_constant_dictionary


from inputs.tools.aptest_to_testcase_converter.database.central_management_db import Central_Management_Hashtable
from inputs.tools.aptest_to_testcase_converter.database.connect_tunnel_db import Connect_Tunnel_Hashtable
from inputs.tools.aptest_to_testcase_converter.database.extraweb_db import Extra_Web_Hashtable
from inputs.tools.aptest_to_testcase_converter.database.general_db import General_Hashtable
from inputs.tools.aptest_to_testcase_converter.database.security_administration_db import Security_Administration_Hashtable
from inputs.tools.aptest_to_testcase_converter.database.monitoring_db import Monitoring_Hashtable
from inputs.tools.aptest_to_testcase_converter.database.system_configuration_db import System_Configuration_Hashtable
from inputs.tools.aptest_to_testcase_converter.database.user_access_db import User_Acess_Hashtable



# list contains uuid's
uuid_list = []
# list contains class names
test_cases_name_list = []

# test case file first half body :- contains librarys
class_body_of_TC_1 = """
__author__ = ''

from scripts.lib.api.mgmt_api.mgmt_api_session import *
from scripts.lib.common_api_and_ui.setup import *
from scripts.lib.common_api_and_ui.decorators import Decorator

"""
# test case file second half body :- contains body ( can change as per requirement )
class_body_of_TC_2 = """
class classname (Test):
    uuid = uuidvalue

    @Decorator._exception_logger
    def runTest(self):
        api_obj = ManagementAPISession()
        # Restore the 'tier2' config.
        api_obj.restore_AMC_config('tier2')
        # apply changes
        api_obj.apply_changes()
        
"""

# test suite file first half body
class_body_of_TS_1 = """
#  __author__ = ''
#  automated on :
#  aptest path  : 

import sys
import os

root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
suite_absolute_path = (scriptPath.split(os.sep))
for i in range(suite_absolute_path.index('scripts')-1, len(suite_absolute_path)-1):
    root = root + "../"
os.chdir(root)
dir = os.path.abspath(os.curdir)
sys.path.append(dir)

"""

class_body_of_TS_2 = """
def suite():
    test_cases = [
"""
# test suite file second half body
class_body_of_TS_3 = """  ]

    suites = unittest.TestSuite()
    i = 0
    while i < test_cases.__len__():
        suites.addTest(test_cases[i])
        i += 1
    return suites


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    results = runner.run(test_suite)
    resultsString = str(results)
    resultArray = resultsString.split(" ")
    x = resultArray[1]
    y = resultArray[2]
    z = resultArray[3]
    logger("<" + x + " ," + y + " ," + z)

"""

class TestsuiteExport:

    # Non-tc class name
    non_tc_class_name = 'TestNonTC'
    # the testcase path of the python file to be generated
    user_input_path = None
    # Enter your file name  ( do not enter .py  extension )
    file_name = None
    # Write your Root directory of the project
    root_dir = None

    # some constants
    path_1 = None
    # xml file name
    xml_file_name = None
    # test case path
    test_case_path = None
    # test suite path
    test_suite_path = None
    # xml file path
    xml_file_path = None
    # test suite library importing
    test_suite_library = None

    # all heading name , before the UI steps/ expected result starts ,  update it parallely
    UI_part_const_list = [
        "CLIENT_", "OWA_CLIENT_" , "OUTPUT_",
        "EW_", "EW_CT_", "EW_CT_MCT_", "EW_MC_", "EW_MCT_",
        "WP_", "WP_CT_", "WP_CT_MCT_", "WP_MC_", "WP_MCT_", "CT_" ,
        "CT_EW_", "CT_MC_", "CT_MCT_", "CT_ODT_", "CONNECT_DISCONNECT_CT_",
        "LAUNCH_CT_", "LAUNCH_CTS_", "LAUNCH_CT_CLIENT_", "LAUNCH_CT_CONNECT_", "CONNECT_CT_", "CONNECT_CT_CLIENT_",
        "LAUNCH_IE_", "LAUNCH_FIREFOX_",
        "ODT_CT_",
    ]

    # initialize the path , file name and others
    def __init__(self , file_path , file_name ):

        # sample input for user_input_path path and file name   ( do not enter  "/" at begining or ending )
        self.user_input_path = file_path
        # Enter your file name  ( do not enter .py  extension )
        self.file_name = file_name
        # Write your Root directory of the project
        self.root_dir = root_dir

        # some constants
        self.path_1 = self.root_dir + 'KF2.0/scripts/'
        # xml file name
        self.xml_file_name = 'testCases.xml'
        # test case path
        self.test_case_path = self.path_1 + 'test_cases' + '/' + self.user_input_path + '/'
        # test suite path
        self.test_suite_path = self.path_1 + 'test_suites' + '/' + self.user_input_path + '/'
        # xml file path
        self.xml_file_path = self.test_case_path + self.xml_file_name
        # test suite library importing
        self.test_suite_library = 'scripts/test_cases' + '/' + self.user_input_path

    # generate testcase in the respective location with sample body
    def generate_test_case_with_sample_body(self, file_path, file_name):

        # initialize all paths
        self.__init__(file_path, file_name)

        # path to create the testcase file
        final_path = self.test_case_path + self.file_name + ".py"
        file = open(final_path, "w")

        # list to store entire xml file data
        lines = self.read_input_xml_file()
        # this list stores the class body , and write into the file
        class_body_list = []

        # class_name_found variable is used to check we got the string which conatins ( class Name && UUID )
        class_name_found = 0

        # write header section of the file
        file.write(class_body_of_TC_1)

        print("\n\n$$$$$$$...  test case generation has been started please wait ")

        i = 3
        #  start from  3rd  line of the xml file
        while i < len(lines):
            # current line/steps
            cur_step_string = str(lines[i])

            # when pointer is at the string which contain class name and uuid
            if 0 == class_name_found:
                # ) store uuid and class name in respective list
                # ) replace  class name and uuid from template
                # ) update class_name_found 2 , since there will be two empty lines at the end of each TC
                class_name_found = 2

                # write the previous class  data to the file
                file.write(''.join(class_body_list))
                # clear the class_body_list
                class_body_list.clear()

                ###########################  fetch uuid ####################
                result_uuid = cur_step_string[124: 160]
                uuid_list.append(result_uuid)
                ###########################  fetch class name  ##############
                list = cur_step_string.split("/")
                required_class_name = list[len(list) - 3]
                result_class_name = required_class_name.replace("&lt;", "")
                test_cases_name_list.append(result_class_name)
                ###########  main class name/ uuid with default value  #####
                str_copy = class_body_of_TC_2
                str_copy = re.sub(r"\bclassname\b", result_class_name, str_copy)
                str_copy = re.sub(r"\buuidvalue\b", "'" + result_uuid + "'", str_copy)

                # append  new class body to the list
                class_body_list.append(str_copy)
                continue

                # when pointer is at the blank line
            if 1 == len(cur_step_string):
                class_name_found -= 1

            # increment i  value of while loop ,to read next line
            i += 1

        # outside while loop
        if len(class_body_list) != 0:
            file.write(''.join(class_body_list))

        # close file
        file.close()

        print("\n$$$$$$$...  test case has been generated in " + final_path)


    # generate testcase in the respective location , along with each steps code
    # parameter "generate_non_tc" is a boolean value , if  True it will generate NON-TC , else not
    def generate_test_case(self , file_path , file_name , generate_non_tc):

        # initialize all paths
        self.__init__( file_path , file_name)

        # path to create the testcase file
        final_path = self.test_case_path + self.file_name + ".py"
        file = open(final_path, "w")

        # list to store entire xml file data
        lines = self.read_input_xml_file()
        # this list stores the class body , and write into the file
        class_body_list = []

        # used to count "total steps" and "auto generated code" steps from the xml file
        total_steps_present = 0
        auto_generated_steps = 0
        # class_name_found variable is used to check we got the string which conatins ( class Name && UUID )
        class_name_found = 0


        # write header section of the file
        file.write(class_body_of_TC_1)

        print("\n\n$$$$$$$...  test case generation has been started please wait ")

        # generate NON-TC class , if user choice to
        if True == generate_non_tc:
            class_body_list, non_tc_constant_dict = self.generate_NON_TC_class()

        i = 3
        #  start from  3rd  line of the xml file
        while i < len(lines):
            # current line/steps
            cur_step_string = str(lines[i])

            # when pointer is at the string which contain class name and uuid
            if 0 == class_name_found:
                # ) store uuid and class name in respective list
                # ) replace  class name and uuid from template
                # ) update class_name_found 2 , since there will be two empty lines at the end of each TC
                class_name_found = 2

                # write the previous class  data to the file
                file.write(''.join(class_body_list))
                # clear the class_body_list
                class_body_list.clear()

                ###########################  fetch uuid ####################
                result_uuid = cur_step_string[124: 160]
                uuid_list.append(result_uuid)
                ###########################  fetch class name  ##############
                list = cur_step_string.split("/")
                required_class_name = list[len(list) - 3]
                result_class_name = required_class_name.replace("&lt;", "")
                test_cases_name_list.append(result_class_name)
                ###########  main class name/ uuid with default value  #####
                str_copy = class_body_of_TC_2
                str_copy = re.sub(r"\bclassname\b", result_class_name, str_copy)
                str_copy = re.sub(r"\buuidvalue\b", "'" + result_uuid + "'", str_copy)

                # append  new class body to the list
                class_body_list.append(str_copy)
                continue

                # when pointer is at the blank line
            if 1 == len(cur_step_string):
                class_name_found -= 1

                #  when pointer is at the  testcase steps
            else:
                # generate the keyword for the step
                # both the generated_constant  , generated_key has same value
                # generated_constant is in Capital Case , generated_key is in lower Case
                generated_constant, generated_key = self.convert_string_to_stop_word(cur_step_string)

                # check if the step is already present in NON-TC config or not
                if (True == generate_non_tc) and (generated_constant in non_tc_constant_dict.keys()):
                    class_body_list.append('\n\t\t#  step -> : ' + str(self.remove_all_html_tages(cur_step_string)))
                    class_body_list.append('\n\t\t# is present inside NON-TC' + '\n\n')
                    auto_generated_steps += 1
                    total_steps_present += 1
                    i += 1
                    continue

                # search the keyword in the dictionary , if present append keyword's code to the file
                if generated_key in aptest_constant_dictionary.keys():
                    dict_val = aptest_constant_dictionary.get(generated_key)
                    # print("$$$$$ value is  " + str(dict_val))
                    hashmap_obj = self.get_hashtable_object( str(dict_val) )
                    class_body_list.append(getattr(hashmap_obj, generated_constant) + "\n")
                    auto_generated_steps += 1
                    total_steps_present += 1

                # if generated key is absent in DB ,
                # ) search nearly matched String , if found add it to the auto generated code
                # ) otherwise add it to the SET , to display it ,  absent in the DB
                else:
                    resultant_matching_string, resultant_matching_string_match_ratio = TestsuiteExport.get_nearest_matching_string(
                        generated_key, aptest_constant_dictionary.keys())

                    # if 70 % of the string comparision is matched and also 2nd verifi ( key is present or not )
                    # after matching , fetch respective code from respective class object
                    if resultant_matching_string_match_ratio >= 75 and resultant_matching_string in aptest_constant_dictionary.keys():
                        dict_val = aptest_constant_dictionary.get(resultant_matching_string)
                        # print("$$$$$ value is  " + str(dict_val))
                        hashmap_obj = self.get_hashtable_object(str(dict_val))
                        class_body_list.append(getattr(hashmap_obj, str(resultant_matching_string).upper()) + "\n")
                        auto_generated_steps += 1
                        total_steps_present += 1


                    # otherwise ,count all non empty/minimum constant  70 > size > 4 constants absent in DB
                    elif 4 < len(generated_constant) and 70 > len(generated_constant):
                        class_body_list.append(
                            '\n\t\t# 1 step missed here : ' + str(self.remove_all_html_tages(cur_step_string)))
                        # get hash_key for the constant
                        constant , hash_table_key = self.convert_string_to_stop_word(generated_constant)
                        class_body_list.append('\n\t\t# generated token for the step is : ' + str(generated_constant) +
                                   "   ->   " + str(hash_table_key) +'\n\n')

                        total_steps_present += 1

            # increment i  value of while loop ,to read next line
            i += 1

        # outside while loop
        if len(class_body_list) != 0:
            file.write(''.join(class_body_list))

        # close file
        file.close()

        # substracting size of classes becoz ,  assuming there will be atleast 1 unrequired Constant generated
        total_steps_present -= len(test_cases_name_list)
        efficiency_rate = (auto_generated_steps / total_steps_present) * 100
        # extra 10% refers to class names,uuid and class body
        efficiency_rate += 10

        # print all the constant that are absent in Dataset
        # self.generate_all_constants_absent_in_db(file_path , generate_hash_key= False)
        # print("$$$$$$$ efficiency of  auto generated  code   " + str(efficiency_rate) + " % ")
        print("\n$$$$$$$...  test case has been generated in " + final_path)

    # generate test suite in the respective location
    def generate_test_suite(self , file_path, file_name):

        # initialize all paths
        self.__init__(file_path, file_name)

        final_path = self.test_suite_path + self.file_name + ".py"
        file = open(final_path, "w")

        # if class names and uuid is not generated , it will generated it and store in the list
        if 0 == len(uuid_list) and 0 == len(test_cases_name_list):
            self.fetch_class_name_and_uuid()

        # writing first half to the file
        file.write(class_body_of_TS_1)

        print("\n\n$$$$$$$...  test Suite generation has been started please wait ")

        # importing libraray (testcase/pfom_indep/ so ... ) replace into (testcase.pfom_indep. so ... )
        list = self.test_suite_library.split("/")
        file.write("from ")
        for i in range(len(list)):
            file.write(list[i] + ".")

        file.write(self.file_name)
        file.write("  import *")

        # writing middle part
        file.write(class_body_of_TS_2)

        # writing class name to the file
        for i in range(len(test_cases_name_list)):
            file.write("\t\t\t" + test_cases_name_list[i] + "(),\n")

        # writing second half to the file
        file.write(class_body_of_TS_3)

        # close file
        file.close()
        print("$$$$$$$ test suite has been generated in " + final_path)

    # generate all the constants present in the xml file
    def generate_all_constants(self , file_path  ):

        # initialize all paths
        self.__init__( file_path , None )

        # list to store entire xml file data
        lines = self.read_input_xml_file()

        # this variable is used to check we got the string which conatins ( class Name + UUID )
        class_name_found = 0
        # creating a set object, to store generated constants and to avoid repitive things
        constant_set_obj = set()

        print("\n\n.......$$$$  Generating all Constants present in the XML file ........")

        i = 3
        #  start from  3rd  line of the xml file
        while i < len(lines):
            cur_step_string = str(lines[i])

            # when pointer is at the string which contain class name and uuid
            if 0 == class_name_found:
                # ) update class_name_found 2 , since there will be two empty lines at the end of each TC
                class_name_found = 2
                # increment i value
                i += 1
                continue

                # when pointer is at the blank line
            if 1 == len(cur_step_string):
                class_name_found -= 1

                #  when pointer is at the  testcase steps
            else:
                # generate the keyword for the step
                # both the generated_constant  , generated_key has same value
                # generated_constant is in Capital Case , generated_key is in lower Case
                generated_constant, generated_key = self.convert_string_to_stop_word(cur_step_string)

                # adding all generated constants , min size = 4  &&  less than 70 char
                if 4 < len(generated_constant) and 70 > len(generated_constant):
                    constant_set_obj.add(str(generated_constant))

            # increment i  value of while loop ,to read next line
            i += 1

        # print all the constants
        self.print_generated_set_obj_const(constant_set_obj , generate_hash_key= False)
        print("\n...$$$$$$$$$$  Total constant present in file is ........." + str(len(constant_set_obj)))

    # generate all the constants which are  present in the xml file but absent in Database
    def generate_all_constants_absent_in_db(self , file_path  , generate_hash_key ):

        # initialize all paths
        self.__init__(file_path, None )

        # list to store entire xml file data
        lines = self.read_input_xml_file()

        # this variable is used to check we got the string which conatins ( class Name + UUID )
        class_name_found = 0
        # creating a set object, to store generated constants and to avoid repitive things
        constant_set_obj = set()

        print("\n\n.......$$$$  Generating all Constants present in  XML file  BUT absent in DB........")

        #  start from  3rd  line of the xml file
        i = 3
        while i < len(lines):
            cur_step_string = str(lines[i])

            # when pointer is at the string which contain class name and uuid
            if 0 == class_name_found:
                # ) update class_name_found 2 , since there will be two empty lines at the end of each TC
                class_name_found = 2
                # increment i value of while loop ,to read next line
                i += 1
                continue

                # when pointer is at the blank line
            if 1 == len(cur_step_string):
                class_name_found -= 1

                #  when pointer is at the  testcase steps
            else:
                # generate the keyword for the step
                # both the generated_constant  , generated_key has same value
                # generated_constant is in Capital Case , generated_key is in lower Case
                generated_constant, generated_key = self.convert_string_to_stop_word(cur_step_string)

                # check if the generated constant is absent in DB
                if not generated_key in aptest_constant_dictionary.keys():

                    # adding all generated constants to the set, 80 > size > 4
                    if 4 < len(generated_constant) and 80 > len(generated_constant):

                        # first check , whether the similar constant exists in DB or not
                        resultant_matching_string, resultant_matching_string_match_ratio = TestsuiteExport.get_nearest_matching_string(
                            generated_key, aptest_constant_dictionary.keys())

                        # if the similar matching string >= 90 % matched , we consider it as a matching string and ignore it
                        # otherwise , constant doesnt exist in the DB , so adding it to Set
                        if resultant_matching_string_match_ratio < 90:
                            constant_set_obj.add(str(generated_constant))

            # increment i value of while loop ,to read next line
            i += 1

        # print the set
        self.print_generated_set_obj_const(constant_set_obj , generate_hash_key)
        print("\n...$$$$$$$$$$  Total constant present in file & absent in DB ........." + str(len(constant_set_obj)))


    """ it creates a constant , and removed stop words from string
    return two string as output (generated_constant  , generated_key) having same value
    generated_constant is in Capital Case , generated_key is in lower Case"""
    def convert_string_to_stop_word(self, input_string):

        #  lib used for stemming
        snow_stemmer = SnowballStemmer(language='english')

        # first remove all html tages / other invalid constants
        raw_string = self.remove_all_html_tages(input_string)

        stop_words = set(stopwords.words('english'))

        word_tokens = word_tokenize(raw_string)

        #  converting to constants and storing in a list
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

        filtered_sentence = []

        for w in word_tokens:
            if w not in stop_words:
                # ) using Porter2/snowball algorithm for stemming
                filtered_sentence.append(snow_stemmer.stem(w))

                # add _ after each word
                filtered_sentence.append("_")

        return ''.join(filtered_sentence).upper(), ''.join(filtered_sentence).lower()

    # remove all html  tages , unnecessary characters/words
    def remove_all_html_tages(self, input_string):
        # regex , to replace the word/character present in the string
        input_string = input_string. \
            replace(" b'", ""). \
            replace("N/A", ""). \
            replace("CMC", ""). \
            replace(".", ""). \
            replace("�", " "). \
            replace(":", ""). \
            replace("BACKEND", ""). \
            replace("Back End", ""). \
            replace("BackEnd", ""). \
            replace("BACK END", ""). \
            replace("procedure", ""). \
            replace("PROCEDURE", ""). \
            replace("NOTE", ""). \
            replace("<output>", ""). \
            replace("</output>", ""). \
            replace("&lt;br /&gt;", ""). \
            replace("&lt;p&gt;", ""). \
            replace("&lt;strong&gt;", ""). \
            replace("&lt;/strong&gt;", ""). \
            replace("&lt;/p&gt;", ""). \
            replace("&lt;li&gt;", ""). \
            replace("&lt;/li&gt;", ""). \
            replace("&lt;div&gt;", ""). \
            replace("&lt;/div&gt;", ""). \
            replace("&lt;span&gt;", ""). \
            replace("&lt;/span&gt;", ""). \
            replace("</procedure>", ""). \
            replace("</entry>", ""). \
            replace("<atm_tests>", ""). \
            replace("&amp;gt;", ""). \
            replace("&amp;amp;", ""). \
            replace("<procedure>&lt;p&gt;", ""). \
            replace("<?xml version='1.0''?>", ""). \
            replace("<procedure>&lt;p&gt;AMC:&lt;/p&gt;", ""). \
            replace("<procedure>&lt;p&gt;&lt;br /&gt;", "")

        # remove all white spaces at beginning and ending
        input_string = input_string.strip()

        # regex to remove all numerical part of string
        result = re.sub('[^A-Za-z]+', ' ', input_string)

        return result

    # it compares nearest matched string from the DB and returns it
    def get_nearest_matching_string(query_string, original_string_list, limit=1):

        # apply extract function to fetch the nearest string
        result = process.extract(query_string, original_string_list, limit=limit)

        # get top 1 , matched string details
        resultant_matching_string_tuple = result[0]
        # store matched string name
        resultant_matching_string = resultant_matching_string_tuple[0]
        # store matched ratio
        resultant_matching_string_match_ratio = resultant_matching_string_tuple[1]

        # print("............result .........." + str(result))
        return resultant_matching_string, resultant_matching_string_match_ratio

    # fetch class name and uuid from xml
    def fetch_class_name_and_uuid(self):

        # list to store entire xml file data
        lines = self.read_input_xml_file()

        # this variable is used to check we got the string which conatins ( class Name && UUID )
        class_name_found = 0

        #  start from  3rd  line of the xml file
        for i in range(3, len(lines)):
            # current line/steps
            cur_step_string = str(lines[i])

            # when pointer is at the string which contain class name and uuid
            if 0 == class_name_found:
                # ) store uuid and class name in respective list
                # ) replace  class name and uuid from template
                # ) update class_name_found 2 , since there will be two empty lines at the end of each TC
                class_name_found = 2

                ###########################  fetch uuid ####################
                result_uuid = cur_step_string[124: 160]
                uuid_list.append(result_uuid)
                ###########################  fetch class name  ##############
                list = cur_step_string.split("/")
                required_class_name = list[len(list) - 3]
                result_class_name = required_class_name.replace("&lt;", "")
                test_cases_name_list.append(result_class_name)
                continue

                # when pointer is at the blank line
            if 1 == len(cur_step_string):
                class_name_found -= 1

    # print all the constants present in the set
    def print_generated_set_obj_const(self, constant_set_obj , generate_hash_key):
        constant_set_obj = sorted(constant_set_obj)

        # we need to generate hash_key along with constant
        if True == generate_hash_key:
            for constants in constant_set_obj:
                const , hash_key = self.convert_string_to_stop_word(constants)
                print(str(constants) +"\t --> \t" + str(hash_key))
        else:
            for constants in constant_set_obj:
                print(constants)

    # generate all the constants present in the xml file
    def generate_all_NON_TC_constant(self):

        # list to store entire xml file data
        lines = self.read_input_xml_file()

        # dictionary , which will store all repeated constants
        non_tc_constant_dict = {}

        i = 3
        #  start from  3rd  line of the xml file
        while i < len(lines):
            cur_step_string = str(lines[i])
            generated_constant, generated_key = self.convert_string_to_stop_word(cur_step_string)

            # if we find any UI/output related step , skip all line untill we get an blank line
            if str(generated_constant) in self.UI_part_const_list:
                while i < len(lines):
                    # print("------------> " + str(generated_constant))
                    i += 1
                    cur_step_string = str(lines[i])
                    generated_constant, generated_key = self.convert_string_to_stop_word(cur_step_string)
                    if len(cur_step_string) == 1:
                        break

            # adding all generated constants , min size = 4  &&  less than 70 char
            if 4 < len(generated_constant) and 70 > len(generated_constant):

                # key is CONSTANT  and value is no.Of times constant has repeated
                key = generated_constant
                if key in non_tc_constant_dict.keys():
                    non_tc_constant_dict[key] = non_tc_constant_dict.get(key) + 1
                else:
                    non_tc_constant_dict.setdefault(key, 1)

            # increment i  value of while loop ,to read next line
            i += 1

        # sorting the dict , based on value , descending order
        sorted_dict = {k: v for k, v in sorted(non_tc_constant_dict.items(), key=lambda v: v[1], reverse=True)}

        # if class names and uuid is not generated , it will generated it and store in the list
        if 0 == len(test_cases_name_list):
            self.fetch_class_name_and_uuid()

        total_TC = len(uuid_list)

        # new dictionary which contains , step constant repeated > 30 %
        result_dict = {}

        for key, val in sorted_dict.items():
            # calculate and check for 30 %
            percentage = (val / total_TC) * 100
            if percentage >= 30:
                result_dict.setdefault(key, val)
            else:
                break

        # clear the uuid_list and test_case_name thing ..
        uuid_list.clear()
        test_cases_name_list.clear()

        return result_dict

    # generate NON-TC class
    def generate_NON_TC_class(self):

        non_tc_constant_dict = self.generate_all_NON_TC_constant()
        class_body_list = []

        if len(non_tc_constant_dict) == 0:
            return list

        print("result dict with minimum 30% common steps is  ")
        print(str(non_tc_constant_dict))

        # append the NON-TC class body to the list
        str_copy = class_body_of_TC_2
        str_copy = re.sub(r"\bclassname\b", self.non_tc_class_name, str_copy)
        str_copy = re.sub(r"\buuidvalue\b", "'" + "" + "'", str_copy)

        # append  new class body to the list
        class_body_list.append(str_copy)

        # iterate the dictionary , and add data to the list
        # key -> generated  constant for each step ,  val-> no.Of times repeated
        for key, val in non_tc_constant_dict.items():
            # print("key is " + str(key))
            resultant_matching_string, resultant_matching_string_match_ratio = TestsuiteExport.get_nearest_matching_string(
                key, aptest_constant_dictionary.keys())

            # if 70 % of the string comparision is matched and also 2nd verifi ( key is present or not )
            # after matching , fetch respective code from respective class object
            if resultant_matching_string_match_ratio >= 75 and resultant_matching_string in aptest_constant_dictionary.keys():
                dict_val = aptest_constant_dictionary.get(resultant_matching_string)
                # print(" dict value   " + str(dict_val) )
                hashmap_obj = self.get_hashtable_object(dict_val)
                class_body_list.append(getattr(hashmap_obj, str(resultant_matching_string).upper()) + "\n")

            # otherwise ,count all non empty/minimum constant  70 > size > 4 constants absent in DB
            elif 4 < len(key) and 70 > len(key):
                class_body_list.append('\n\t\t# 1 step missed here , it has repeated  :' + str(val) + '\t times ')
                # get hash_key for the constant
                constant, hash_table_key = self.convert_string_to_stop_word(key)
                class_body_list.append('\n\t\t# generated token for the step is : ' + str(key) +
                                       "   ->   " + str(hash_table_key) + '\n\n')

        # add Non-TC class name to the test_cases_name_list , so it can be appended to Test suite
        test_cases_name_list.append(self.non_tc_class_name)

        # apply changes at the end of cofig
        hashmap_obj = self.get_hashtable_object(str('General_Hashtable'))
        class_body_list.append(getattr(hashmap_obj, 'APPLY_CHANGES_') + "\n")
        class_body_list.append(getattr(hashmap_obj, 'SAVE_AMC_CONFIG_') + "\n")

        return class_body_list, non_tc_constant_dict

    # read entire xml file , store into a string , and return
    def read_input_xml_file(self):
        # list to store entire xml file data
        lines = []
        # reading xml file and storing data in  lines
        with open(self.xml_file_path) as f:
            lines = f.readlines()

        return lines

    # print the constant for the given input string
    def get_single_string_constant(self , string):
        constant , map_key = self.convert_string_to_stop_word(string)
        print(str(constant) +"      ->       " + str(map_key))

    # returns the object of the given class
    def get_hashtable_object(self , class_name):

        return {
            'Central_Management_Hashtable'  : Central_Management_Hashtable(),
            'Connect_Tunnel_Hashtable'      : Connect_Tunnel_Hashtable(),
            'Extra_Web_Hashtable'           : Extra_Web_Hashtable(),
            'General_Hashtable'             : General_Hashtable(),
            'Monitoring_Hashtable'             : Monitoring_Hashtable(),
            'Security_Administration_Hashtable': Security_Administration_Hashtable(),
            'System_Configuration_Hashtable'   : System_Configuration_Hashtable(),
            'User_Acess_Hashtable'             : User_Acess_Hashtable()
        }[class_name]
