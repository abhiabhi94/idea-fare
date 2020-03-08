import secrets
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.urls import reverse


class Idea(models.Model):
    # allow anonymous posting
    conceiver = models.ForeignKey(User, blank=True,
                                  null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=60,
                             help_text='Try to keep this short and sweet. Max 60 characters'
                             )
    concept = models.CharField(max_length=500,
                               help_text='Try to explain your idea in a concise form. Max 500 characters')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default='', max_length=70)
    visibility = models.BooleanField(verbose_name='public', default=True)
    # tags = models.
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
            self.slug = slugify(self.title + '-' + secrets.token_urlsafe(16))

        super(Idea, self).save(*args, **kwargs)

    def _get_meta_conceiver(self):
        """Returns full name conceiver of the idea"""
        return self.conceiver.get_full_name()

    def get_absolute_url(self):
        return reverse('ideas:idea-details', kwargs={'slug': self.slug})
