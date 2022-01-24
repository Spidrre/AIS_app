from django.test import TestCase
from .models import Task
import datetime
from django.contrib.auth.models import User


# class tablTestCase(TestCase):
#     def setUp(self):
#         tabl.objects.create(one=1, name="lisa")
#         tabl.objects.create(one=2, name="mick")
#
#     def test_for_print(self):
#         lisa = tabl.objects.get(name="lisa")
#         mick = tabl.objects.get(name="mick")
#         self.assertEqual(lisa.printt(), "i'm 1 lisa")
#         self.assertEqual(mick.printt(), "i'm 2 mick")

class TaskTestCase(TestCase):
    def setUp(self):
        unit1_deadline = '2022-01-16 01:37'
        unit2_deadline = '2022-01-17 01:37'
        format = '%Y-%m-%d %H:%M'

        user1 = User.objects.create(username='testuser')
        user1.set_password('h12345678')
        user1.save()

        Task.objects.create(user=user1, title="unit1", description="unit1desc",
                            deadline=datetime.datetime.strptime(unit1_deadline, format), complete=True, tag="unit")
        Task.objects.create(user=user1, title="unit2", description="unit2desc",
                            deadline=datetime.datetime.strptime(unit2_deadline, format), complete=False, tag="unit")

    def test_create_print(self):
        unit1_deadline = '2022-01-16 01:37'
        unit2_deadline = '2022-01-17 01:37'
        format = '%Y-%m-%d %H:%M'
        first = Task.objects.get(user__username="testuser", title="unit1", description="unit1desc",
                                 deadline=datetime.datetime.strptime(unit1_deadline, format), complete=True, tag="unit")
        second = Task.objects.get(user__username="testuser", title="unit2", description="unit2desc",
                                  deadline=datetime.datetime.strptime(unit2_deadline, format), complete=False,
                                  tag="unit")
        self.assertEqual(first.printt(), "Title: unit1, Description: unit1desc")
        self.assertEqual(second.printt(), "Title: unit2, Description: unit2desc")

    def test_update_print(self):
        unit1_deadline = '2022-01-16 01:37'
        unit2_deadline = '2022-01-17 01:37'
        format = '%Y-%m-%d %H:%M'
        first = Task.objects.get(user__username="testuser", title="unit1", description="unit1desc",
                                 deadline=datetime.datetime.strptime(unit1_deadline, format), complete=True, tag="unit")
        second = Task.objects.get(user__username="testuser", title="unit2", description="unit2desc",
                                  deadline=datetime.datetime.strptime(unit2_deadline, format), complete=False,
                                  tag="unit")

        unit1_new_deadline = '2022-01-18 01:37'
        unit2_new_deadline = '2022-01-19 01:37'
        # first['deadline'] = datetime.datetime.strptime(unit1_new_deadline, format)
        # second['deadline'] = datetime.datetime.strptime(unit2_new_deadline, format)

        setattr(first, 'deadline', datetime.datetime.strptime(unit1_new_deadline, format))
        setattr(second, 'deadline', datetime.datetime.strptime(unit2_new_deadline, format))

        self.assertEqual(first.printd(), "Deadline: 2022-01-18 01:37:00")
        self.assertEqual(second.printd(), "Deadline: 2022-01-19 01:37:00")

    def test_delete_print(self):
        unit1_deadline = '2022-01-16 01:37'
        unit2_deadline = '2022-01-17 01:37'
        format = '%Y-%m-%d %H:%M'
        first = Task.objects.get(user__username="testuser", title="unit1", description="unit1desc",
                                 deadline=datetime.datetime.strptime(unit1_deadline, format), complete=True, tag="unit")
        second = Task.objects.get(user__username="testuser", title="unit2", description="unit2desc",
                                  deadline=datetime.datetime.strptime(unit2_deadline, format), complete=False,
                                  tag="unit")

        first.delete()
        second.delete()

        try:
            first_check = Task.objects.get(user__username="testuser", title="unit1", description="unit1desc",
                                           deadline=datetime.datetime.strptime(unit1_deadline, format), complete=True,
                                           tag="unit")
        except:
            print("No first_task found")

        try:
            second = Task.objects.get(user__username="testuser", title="unit2", description="unit2desc",
                                      deadline=datetime.datetime.strptime(unit2_deadline, format), complete=False,
                                      tag="unit")
        except:
            print("No second_task found")

        # self.assertEqual(first.printd(), "Deadline: 2022-01-18 01:37:00")
        # self.assertEqual(second.printd(), "Deadline: 2022-01-19 01:37:00")
