import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from urlextract import URLExtract

from flag.models import Flag
from ideas.manager import IdeaManager

MAX_TITLE_LENGTH = 60
MAX_CONCEPT_LENGTH = 500
MAX_SLUG_LENGTH = 80
LENGTH_OF_RANDOM_ALPHANUMERIC_SLUG = 4

User = get_user_model()
AnonymousUser.username = 'anonymous'


class Idea(models.Model):
    # allow anonymous posting
    user = models.ForeignKey(User, blank=True, db_column='conceiver',
                             null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=MAX_TITLE_LENGTH,
                             help_text=_('Try to keep this short and sweet. Max 60 characters')
                             )
    concept = models.CharField(max_length=MAX_CONCEPT_LENGTH,
                               help_text=_('Try to explain your idea in a concise form. Max 500 characters'))
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default='', max_length=MAX_SLUG_LENGTH)
    visibility = models.BooleanField(verbose_name=_('public'), default=True)
    flag = GenericRelation(Flag, related_query_name='idea_flagged')

    objects = models.Manager()
    public_objects = IdeaManager()
    tags = TaggableManager()

    _metadata = {
        'title': 'title',
        'description': 'concept',
        'keywords': 'get_tags_list',
        'og_author': '_get_meta_conceiver',
        'url': 'get_absolute_url',
    }

    class Meta:
        ordering = ['-date_created']

    def save(self, *args, **kwargs):
        """
        set the slug for the first time only
            - slugify the title with a random alphanumeric
        """

        if self.date_updated is None:
            self.slug = slugify(
                self.title + '-' +
                secrets.token_urlsafe(LENGTH_OF_RANDOM_ALPHANUMERIC_SLUG)
            )
        # Anonymous Ideas will always be public
        if self.user is None:
            self.visibility = True

        # Linkinfy the links
        extractor = URLExtract()
        for url in extractor.gen_urls(self.concept):
            self.concept = self.concept.replace(url, "<a href={}>{}</a>".format(url, url))

        super(Idea, self).save(*args, **kwargs)

    def __str__(self):
        """Returns title when the object is printed"""
        return self.title

    @property
    def conceiver(self):
        """Setting the attribute for anonymous users"""
        if self.user is None:
            AnonymousUser.username = 'anonymous'
            return AnonymousUser
        return self.user

    def _get_meta_conceiver(self):
        """Returns full name conceiver of the idea"""
        return self.conceiver.get_full_name()

    def get_absolute_url(self):
        return reverse('ideas:idea-details', kwargs={'slug': self.slug})

    def get_tags_list(self):
        return self.tags.all()
