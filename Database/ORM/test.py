from flask import jsonify
from mongoengine import *


class Test2(Document):
    tid = IntField(max_length=50)


class Test(Document):
    name = StringField(max_length=4)
    test1 = ReferenceField(Test2)
    test2 = ReferenceField(Test2)
    test3 = ReferenceField(Test2)


def do_test():
    test2_1 = Test2(tid=1).save()
    test2_2 = Test2(tid=2).save()
    test2_3 = Test2(tid=3).save()

    Test(
        name='test',
        test1=test2_1,
        test2=test2_2,
        test3=test2_3
    ).save()
    tests = []
    for test in Test.objects():
        #print(test.to_mongo())
        #test = test.to_mongo()
        for test2 in Test2.objects():
            if test['test1']['tid'] == test2['tid']:
                test['test1']['tid'] = test2['tid']
            elif test['test2']['tid'] == test2['tid']:
                test['test2']['tid'] = test2['tid']
        tests.append(test)
        test.delete()
    return jsonify(tests)
