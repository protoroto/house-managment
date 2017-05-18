# -*- coding: utf-8 -*-
from datetime import date

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


PERSON = (
    ('L', _("Leo")),
    ('I', _("Isa")),
)

MONTHS = (
    ('1', _("Gennaio")),
    ('2', _("Febbraio")),
    ('3', _("Marzo")),
    ('4', _("Aprile")),
    ('5', _("Maggio")),
    ('6', _("Giugno")),
    ('7', _("Luglio")),
    ('8', _("Agosto")),
    ('9', _("Settembre")),
    ('10', _("Ottobre")),
    ('11', _("Novembre")),
    ('12', _("Dicembre")),
)

class Bill(models.Model):
    title = models.CharField(
        verbose_name=_(u'Nome bolletta'),
        max_length=200
    )
    cost = models.DecimalField(
        verbose_name=_(u'Prezzo'),
        max_digits=6,
        decimal_places=2
    )
    expiry_date = models.DateField(
        verbose_name=_(u'Data di scadenza'),
        blank=False, null=False
    )
    payed = models.BooleanField(
        verbose_name=_(u'Pagata'),
        default=False
    )
    person = models.CharField(
        verbose_name=_(u"Chi ha pagato"),
        max_length=1, blank=True, null=True, choices=PERSON
    )
    payed_date = models.DateField(
        verbose_name=_(u'Data di pagamento'),
        blank=True, null=True,
        default=timezone.now
    )
    payed_image = models.ImageField(
        verbose_name=_(u'Immagine bolletta pagata'),
        blank=True, null=True,
        upload_to='bill-images/%Y/%m/%d/'
    )

    class Meta:
        verbose_name = _('Bolletta')
        verbose_name_plural = _('Bollette')
        ordering = ('expiry_date',)


    def __str__(self):
        return '{} - {}'.format(self.title, self.expiry_date)

    @property
    def get_person(self):
        if self.person:
            return self.get_person_display()
        return '-'


class Expense(models.Model):
    title = models.CharField(
        verbose_name=_(u'Nome spesa'),
        max_length=200,
        blank=False, null=False
    )
    cost = models.DecimalField(
        verbose_name=_(u'Prezzo'),
        max_digits=6,
        decimal_places=2,
        blank=False, null=False
    )
    payed_date = models.DateField(
        verbose_name=_(u'Data della spesa'),
        blank=False, null=False,
        default=timezone.now
    )
    person = models.CharField(
        verbose_name=_(u"Chi ha speso"),
        max_length=1, blank=False, null=False, choices=PERSON
    )

    class Meta:
        verbose_name = _('Spesa')
        verbose_name_plural = _('Spese')
        ordering = ('-payed_date',)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.payed_date, self.title, self.cost, self.person)

    @property
    def get_person(self):
        if self.person:
            return self.get_person_display()
        return '-'


class Memo(models.Model):
    title = models.CharField(
        verbose_name=_(u'Nome memo'),
        max_length=200,
        blank=False, null=False
    )
    cost = models.DecimalField(
        verbose_name=_(u'Prezzo'),
        max_digits=6,
        decimal_places=2,
        blank=True, null=True
    )
    expiry_date = models.DateField(
        verbose_name=_(u'Data della spesa'),
        blank=True, null=True
    )

    class Meta:
        verbose_name = _('Memo')
        verbose_name_plural = _('Memo')
        ordering = ('expiry_date', 'title')

    def __str__(self):
        if self.expiry_date:
            return '{} - {}'.format(self.expiry_date, self.title)
        else:
            return self.title
