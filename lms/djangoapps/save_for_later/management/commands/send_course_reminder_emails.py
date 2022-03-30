"""
Management command to send reminder emails.
"""

from textwrap import dedent
from datetime import datetime, timedelta
from pytz import UTC, timezone
import logging

from django.conf import settings
from django.core.management import BaseCommand
from django.contrib.auth.models import User

from lms.djangoapps.save_for_later.helper import send_email
from lms.djangoapps.save_for_later.models import SavedCourse
from common.djangoapps.student.models import CourseEnrollment
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from common.djangoapps.util.query import use_read_replica_if_available

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command to send reminder emails to those users who
    saved course by email but not register within 15 days.


    Examples:

        ./manage.py lms send_course_reminder_emails
    """
    help = dedent(__doc__)

    @staticmethod
    def should_send_email(saved_course_date):
        saved_course_days = (datetime.now(UTC) - saved_course_date).days
        return saved_course_days > settings.SAVE_FOR_LATER_REMINDER_EMAIL_THRESHOLD

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Maximum number of users to send email in one celery task')

    def handle(self, *args, **options):
        """
        Handle the send save for later reminder emails.
        """
        total = SavedCourse.objects.count()
        batch_size = max(1, options.get('batch_size'))
        num_batches = ((total - 1) / batch_size + 1) if total > 0 else 0
        for batch_num in range(int(num_batches)):
            start = batch_num * batch_size + 1  # ids are 1-based, so add 1
            end = min(start + batch_size, total)


        # reminder_email_threshold_date = datetime.now() + timedelta(days=settings.SAVE_FOR_LATER_REMINDER_EMAIL_THRESHOLD)
        # saved_courses = SavedCourse.objects.\
        #     filter(reminder_email_sent=False, modified__gt=reminder_email_threshold_date).\
        #     order_by('-modified')#[:batch_size]
        # # saved_courses = use_read_replica_if_available(query)
        # for saved_course in saved_courses:
        #     user = None
        #     if saved_course.user_id:
        #         user = User.objects.filter(id=saved_course.user_id).first()
        #     course = CourseOverview.get_from_id(saved_course.course_id)
        #     course_data = {
        #         'course': course,
        #         'send_to_self': None,
        #         'user_id': saved_course.user_id,
        #         'org_img_url': saved_course.org_img_url,
        #         'marketing_url': saved_course.marketing_url,
        #         'weeks_to_complete': saved_course.weeks_to_complete,
        #         'min_effort': saved_course.min_effort,
        #         'max_effort': saved_course.max_effort,
        #         'type': 'course',
        #     }
        #     if Command.should_send_email(saved_course.modified):
        #         if user:
        #             enrollment = CourseEnrollment.get_enrollment(user, saved_course.course_id)
        #             if enrollment:
        #                 return
        #         send_email(saved_course.email, course_data)
