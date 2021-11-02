from inputs.tools.aptest_to_testcase_converter.database.central_management_db import Central_Management_Hashtable

from inputs.tools.aptest_to_testcase_converter.aptest_to_testcase_libs import TestsuiteExport


 # sample input for user_input_path path
 # Enter the path from   pFrom independent  and file name   ( do not enter  "/" at begining or ending )
user_input_path = 'platform_independent/end_user_3/appliance_authorization_5/acl_testing'
# Enter your file name  ( do not enter .py  extension )
file_name = 'testing_file'

obj = TestsuiteExport( user_input_path , file_name )





# .........................select the requirement function and run .................

# generate test case with sample body
obj.generate_test_case_with_sample_body( user_input_path , file_name  )


# generate test case with each steps code
# obj.generate_test_case( user_input_path , file_name , generate_non_tc = True )

# generate test suite
obj.generate_test_suite(user_input_path , file_name)

# generate all the constant present in the xml file
# obj.generate_all_constants(user_input_path )


# generate all the constant present in the xml file but absent in Database
# obj.generate_all_constants_absent_in_db(user_input_path  , generate_hash_key = False )


# eneter any individual string to print its generated constant
# input_string = """
# enter_any_string_to_get_its_constant """
# obj.get_single_string_constant(input_string)