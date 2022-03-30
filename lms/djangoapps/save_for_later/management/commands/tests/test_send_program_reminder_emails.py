""" Test the test_send_program_reminder_emails command line script."""


from unittest.mock import patch, MagicMock

import ddt
from django.core.management import call_command

from openedx.core.djangolib.testing.utils import skip_unless_lms
from lms.djangoapps.save_for_later.tests.factories import SavedPogramFactory
from openedx.core.djangoapps.catalog.tests.factories import ProgramFactory

from xmodule.modulestore.tests.django_utils import SharedModuleStoreTestCase


@ddt.ddt
@skip_unless_lms
class SavedProgramReminderEmailsTest(SharedModuleStoreTestCase):
    """
    Test the send_program_reminder_emails management command
    """

    def setUp(self):
        super().setUp()
        self.uuid = '587f6abe-bfa4-4125-9fbe-4789bf3f97f1'
        self.saved_program = SavedPogramFactory.create(program_uuid=self.uuid)
        self.program = ProgramFactory(uuid=self.uuid)

    def test_send_reminder_emails(self):
        with patch('lms.djangoapps.save_for_later.helper.BrazeClient') as mock_task:
            call_command('send_program_reminder_emails')
            mock_task.assert_called()
