""" Test the test_send_course_reminder_emails command line script."""


from unittest.mock import patch, MagicMock

import ddt
from django.core.management import call_command
from django.core.management.base import CommandError

from openedx.core.djangolib.testing.utils import skip_unless_lms
from common.djangoapps.student.tests.factories import UserFactory
from lms.djangoapps.save_for_later.tests.factories import SavedCourseFactory
from openedx.core.djangoapps.content.course_overviews.tests.factories import CourseOverviewFactory

from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase


@ddt.ddt
@skip_unless_lms
class SavedCourseReminderEmailsTest(SharedModuleStoreTestCase):
    """
    Test the test_send_course_reminder_emails management command
    """

    def setUp(self):
        super().setUp()
        self.course_id = 'course-v1:edX+DemoX+Demo_Course'
        self.user = UserFactory(email='email@test.com', username='jdoe')
        self.saved_course = SavedCourseFactory.create(course_id=self.course_id, user_id=self.user.id)
        self.saved_course_1 = SavedCourseFactory.create(course_id=self.course_id)
        CourseOverviewFactory.create(id=self.saved_course.course_id)
        CourseOverviewFactory.create(id=self.saved_course_1.course_id)

    def test_send_reminder_emails(self):
        with patch('lms.djangoapps.save_for_later.helper.BrazeClient') as mock_task:
            call_command('send_course_reminder_emails')
            mock_task.assert_called()
