
    Goal
    convert ( Basic + advanced) Common requirements  from aptest into code

  Algorithm
  1) export the testsuite in xml format
  2) put the input  xml file in  a proper location
  3) create a basic Template for the Testcase which need to be added in the file
  3) read xml file  &&  fetch   uuid ,class name  && store in two different list
  5) read the steps and fetch code , append resultant  code to the template
  6) write the final template to the required location

  7) create a basic Template for TestSuite which need to be added in the file
  8) fetch the class names and uuids  from the lists and append to the template
  9) write the final template to the required location



........................................................................................................................
........................................................................................................................

                 current design of the data
                 multiple key ,single value concept   ( many to one mapping )

     Keywords are stored in 2 different file

    1)  aptest_constant_hashtable : keyword are in small case
                                  : all keywords are stored as a key to the hashtable

    2) DB respected file          : keyword are in Capital case
                                  : all keywords are stored as a String constants ,
                                    whose values are respected code




........................................................................................................................
........................................................................................................................
           how keywords to be generated

    1) generate both the constant ( Constant , hash_key ) using api function
    i) two similar constant are generated with capital/small case
    ii) small case constant refer ->  hash_key
    iii) capital case constant refere -> the main constant , in which value to be stored

    2) put the hash_key inside aptest_constant_hashtable ( in the respected position)
       and the value should be the file name , in which "Capital case constant " to be kept

    3) put the Capital case constant with data , inside the respected file

    4)