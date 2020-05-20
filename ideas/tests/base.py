from abc import abstractmethod

from tests.base import TestBaseView


class TestIdeaBase(TestBaseView):

    @classmethod
    def setUpClass(cls):
        """
        Create
        - 2 users
            - 1 will be used to associate ideas
            - 2nd will be used for checking unauthorised access during tests
        - 24 ideas to test pagination\
            ( text inside brackets indicate pattern used for generating id)
            - 6 anonymous ideas (x % 4 == 0)
            - 18 non-anonymous ideas
                - 1 private idea (x % 4 != 0 and x % 10 == 0)
                - 17 public ideas (x%4 != 0 and x%10 != 0)
        """
        super().setUpClass()
        # Create 24 ideas to test pagination
        num_ideas = 25
        cls.dummy_user = cls.create_user(
                                        username='tester3',
                                        email='jach.kar.ta@gmail.com',
                                        password='user123#'
                                        )
        for idea_id in range(1, num_ideas):
            if idea_id % 4 == 0:
                cls.create_idea(
                    title=f'Anonymous Idea: idea number {idea_id}',
                    concept=f'The concept of the idea {idea_id}',
                    tags=f'tag_{idea_id}, tag_{idea_id+1}'
                )
            else:
                cls.create_idea(
                    title=f'Non-anonymous Idea: idea number {idea_id}',
                    concept=f'The concept of the idea{idea_id}',
                    tags=f'tag_{idea_id}, tag_{idea_id+1}',
                    user=cls.user,
                    visibility=False if idea_id % 10 == 0 else True
                )

    @abstractmethod
    def get_url(self):
        """A utility function that returns URL for the view"""
        raise NotImplementedError
