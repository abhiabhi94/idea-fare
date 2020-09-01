from django.conf import settings

from flag.tests.base import BaseFlagViewTest, Flag, FlagInstance


class TestSetFlag(BaseFlagViewTest):
    def test_set_flag_for_flagging(self):
        idea = self.create_idea()
        data = self.data.copy()
        data['model_id'] = idea.id
        response = self.request('post', self.url, data=data)
        response_data = {
            'status': 0,
            'flag': 1,
            'msg': 'The content has been flagged successfully. A moderator will review it shortly.'
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

        # check database
        flag = Flag.objects.get_flag(idea)
        __, created = FlagInstance.objects.get_or_create(
                flag=flag,
                user=response.wsgi_request.user,
                reason=data['reason']
                )
        self.assertEqual(created, False)

    def test_set_flag_for_flagging_flagged_object(self):
        idea = self.create_idea()
        data = self.data.copy()
        data['model_id'] = idea.id
        self.set_flag(idea)
        response = self.request('post', self.url, data=data)
        response_data = {
            'status': 1,
            'msg': [f'This content has already been flagged by the user ({self.user_1.username})']
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

    def test_set_flag_for_flagging_unflagged_object(self):
        idea = self.create_idea()
        data = self.data.copy()
        data['model_id'] = idea.id
        data.pop('reason')
        response = self.request('post', self.url, data=data)
        response_data = {
            'status': 1,
            'msg': [f'This content has not been flagged by the user ({self.user_1.username})']
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

    def test_set_flag_for_unflagging(self):
        # un-flag => no reason is passed and the comment must be already flagged by the user
        idea = self.create_idea()
        self.set_flag(model_obj=idea)
        data = self.data.copy()
        data['model_id'] = idea.id
        data.pop('reason')
        response = self.request('post', self.url, data=data)
        response_data = {
            'status': 0,
            'msg': 'The content has been unflagged successfully.'
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)
        # check database
        flag = Flag.objects.get_flag(idea)
        __, created = FlagInstance.objects.get_or_create(
                flag=flag,
                user=response.wsgi_request.user,
                reason=FlagInstance.reason_values[0]
                )
        self.assertEqual(created, True)

    def test_set_flag_for_unauthenticated_user(self):
        """Test whether unauthenticated user can create/delete flag using view"""
        self.client.logout()
        url = self.url
        response = self.request('post', url, data=self.data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/{}/?next={}'.format(settings.LOGIN_URL, url))

    def test_incorrect_reason(self):
        """Test response when incorrect reason is passed"""
        data = self.data.copy()
        reason = -1
        data['reason'] = reason
        response = self.request('post', self.url, data=data)
        response_data = {
            'status': 1,
            'msg': [f'{reason} is an invalid reason']
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

    def test_choosing_last_reason_without_info(self):
        """Test response when incorrect reason is passed"""
        data = self.data.copy()
        reason = FlagInstance.reason_values[-1]
        data.update({'reason': reason})
        response = self.request('post', self.url, data=data)
        response_data = {
            'status': 1,
            'msg': ['Please supply some information as the reason for flagging']
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), response_data)

    def test_choosing_last_reason_with_info(self):
        """Test response when last reason is passed with info"""
        data = self.data.copy()
        idea = self.idea_2
        reason = FlagInstance.reason_values[-1]
        info = 'weird'
        data.update({'reason': reason, 'info': info, 'model_id': idea.id})
        response = self.request('post', self.url, data=data)
        response_data = {
            'status': 0,
            'flag': 1,
            'msg': 'The content has been flagged successfully. A moderator will review it shortly.'
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)
        # check database
        flag = Flag.objects.get_flag(idea)
        self.assertEqual(FlagInstance.objects.get(user=response.wsgi_request.user, flag=flag).info, info)
