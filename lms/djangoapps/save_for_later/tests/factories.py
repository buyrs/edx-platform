"""

"""

import factory

from datetime import datetime
from pytz import UTC

from factory.django import DjangoModelFactory

from lms.djangoapps.save_for_later.models import SavedCourse, SavedProgram


class SavedCourseFactory(DjangoModelFactory):
    class Meta:
        model = SavedCourse
        django_get_or_create = ('course_id', 'user_id')

    email = 'abc@test.com'
    course_id = factory.Sequence('{}'.format)
    user_id = factory.Sequence('{}'.format)
    created = datetime(2020, 1, 1, tzinfo=UTC)
    modified = datetime(2020, 2, 1, tzinfo=UTC)


class SavedPogramFactory(DjangoModelFactory):
    class Meta:
        model = SavedProgram
        django_get_or_create = ('program_uuid', )

    email = 'abc@test.com'
    user_id = factory.Sequence('{}'.format)
    program_uuid = factory.Sequence('{}'.format)
    created = datetime(2020, 1, 1, tzinfo=UTC)
    modified = datetime(2020, 2, 1, tzinfo=UTC)
