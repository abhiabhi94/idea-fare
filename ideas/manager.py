from django.db.models import Manager

class IdeaManager(Manager):
    def get_queryset(self, order='-date_created'):
        """
        Returns
            QuerySet
                the set of ideas that are public

        Args
            order: str
                The field according to which the list will be sorted
        """
        return super().get_queryset().filter(visibility=True)
