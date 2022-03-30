"""
Management command to send program reminder emails.
"""

from textwrap import dedent
from datetime import datetime
from pytz import UTC, timezone
import logging

from django.conf import settings
from django.db.models import Count, Max
from django.core.management import BaseCommand
from django.contrib.auth.models import User

from lms.djangoapps.save_for_later.helper import send_email
from lms.djangoapps.save_for_later.models import SavedProgram
from lms.djangoapps.program_enrollments.api import get_program_enrollment
from openedx.core.djangoapps.catalog.utils import get_programs

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command to send reminder emails to those users who saved
    program by email but not enroll program within 15 days.


    Examples:

        ./manage.py lms send_program_reminder_emails
    """
    help = dedent(__doc__)

    @staticmethod
    def should_send_email(saved_program_date):
        saved_program_days = (datetime.now(UTC) - saved_program_date).days
        return saved_program_days > settings.SAVE_FOR_LATER_REMINDER_EMAIL_THRESHOLD

    def handle(self, *args, **options):
        """
        Handle the send save for later reminder emails.
        """
        saved_programs = SavedProgram.objects.all().order_by('-created')
        for saved_program in saved_programs:
            user = User.objects.filter(id=saved_program.user_id).first()
            program = get_programs(uuid=saved_program.program_uuid)
            if program:
                program_data = {
                    'program': program,
                    'send_to_self': None,
                    'user_id': user.id,
                    'pref-lang': saved_program.pref_lang,
                    'type': 'program',
                }
                if Command.should_send_email(saved_program.modified):
                    if user and get_program_enrollment(program_uuid=saved_program.uuid, user=user):
                        return
                    send_email(saved_program.email, program_data)
