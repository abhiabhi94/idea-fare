from django.core.exceptions import ValidationError

from flag.tests.base import BaseFlagModelTest, Flag, FlagInstance


class FlagModelTest(BaseFlagModelTest):
    def test_can_create_flag(self):
        self.assertIsNotNone(Flag.objects.create(content_object=self.idea_2))

    def test_increase_count(self):
        self.flag.increase_count()
        self.flag.refresh_from_db()

        self.assertEqual(self.flag.count, 1)

    def test_decrease_count(self):
        self.flag.increase_count()
        self.flag.decrease_count()
        self.flag.refresh_from_db()

        self.assertEqual(self.flag.count, 0)

    def test_toggle_state(self):
        self.flag.increase_count()
        self.flag.toggle_state()

        self.assertEqual(self.flag.state, Flag.State.FLAGGED)

        with self.settings(FLAGS_ALLOWED=1):
            self.flag.increase_count()
            self.flag.toggle_state()

            self.assertEqual(self.flag.state, Flag.State.UNFLAGGED)
            # flag once more to toggle the state
            self.flag.increase_count()
            self.flag.toggle_state()

            self.assertEqual(self.flag.state, Flag.State.FLAGGED)


class FlagManagerTest(BaseFlagModelTest):
    def setUp(self):
        super().setUp()
        self.flag = Flag.objects.create(content_object=self.content_object_2, creator=self.idea_2.user)

    def test_get_flag(self):
        self.assertEqual(Flag.objects.get_flag(self.idea_2), self.flag)


class FlagInstanceModelTest(BaseFlagModelTest):
    def test_create_flag_instance(self):
        self.assertIsNotNone(
            FlagInstance.objects.create(
                flag=self.flag,
                reason=FlagInstance.reason_values[0],
                user=self.user_1
            )
        )

    def test_flagged_signal(self):
        user = self.user_2
        flag = self.create_flag(self.content_object_2, user)
        FlagInstance.objects.create_flag(user=user, flag=flag, reason=FlagInstance.reason_values[0], info='')
        flag.refresh_from_db()

        self.assertEqual(flag.count, 1)
        self.assertEqual(flag.state, Flag.State.FLAGGED)

        # instance edited won't increase the flag count
        flag_instance = FlagInstance.objects.get(user=user, flag=flag)
        self.assertIsNotNone(flag_instance)
        flag_instance.info = 'change value for test'
        flag_instance.save()
        flag.refresh_from_db()

        self.assertEqual(flag.count, 1)

    def test_unflagged_signal(self):
        user = self.user_1
        flag = self.create_flag(self.content_object_2, user)
        self.set_flag(model_obj=self.idea_2, user=user)
        FlagInstance.objects.delete_flag(user=user, flag=flag)
        flag.refresh_from_db()

        self.assertEqual(flag.count, 0)
        self.assertEqual(flag.state, Flag.State.UNFLAGGED)


class TestFlagInstanceManager(BaseFlagModelTest):

    def test_has_flagged(self):
        user = self.user_2
        idea = self.idea_2
        self.assertEqual(FlagInstance.objects.has_flagged(user, idea), False)

        self.set_flag(self.idea_2, user=user)

        self.assertEqual(FlagInstance.objects.has_flagged(user, idea), True)

    def test_clean_when_last_reason_is_used(self):
        flag = self.flag

        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create(
                flag=flag,
                reason=FlagInstance.reason_values[-1]
            )
        self.assertEqual(
            error.exception.message_dict['info'],
            ['Please provide some information why you choose to report the content'])

    def test_clean_reason_for_invalid_values(self):
        flag = self.flag
        user = self.user_1
        reason = -1
        info = None

        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user=user, flag=flag, reason=reason, info=info)

        self.assertEqual(error.exception.messages, [f'{reason} is an invalid reason'])

        reason = 'r'
        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user=user, flag=flag, reason=reason, info=info)

        self.assertEqual(error.exception.messages, [f'{reason} is an invalid reason'])

        reason = None
        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user=user, flag=flag, reason=reason, info=info)

        self.assertEqual(error.exception.messages, [f'{reason} is an invalid reason'])

    def test_create_flag_for_flagging_twice(self):
        user = self.user_1
        flag = self.flag
        reason = FlagInstance.reason_values[0]
        info = None

        FlagInstance.objects.create_flag(user, flag, reason, info)
        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.create_flag(user, flag, reason, info)

        self.assertEqual(error.exception.messages, [f'This content has already been flagged by the user ({user})'])

    def test_delete_flag_without_flagging(self):
        user = self.user_1
        flag = self.flag

        with self.assertRaises(ValidationError) as error:
            FlagInstance.objects.delete_flag(user, flag)

        self.assertEqual(error.exception.messages, [f'This content has not been flagged by the user ({user})'])
