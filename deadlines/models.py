from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _



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
    payed_date = models.DateField(
    	verbose_name=_(u'Data di pagamento'), 
    	blank=True, null=True
    )
    payed_image = models.ImageField(
    	verbose_name=_(u'Immagine bolletta pagata'),
    	blank=True, null=True
    )

    class Meta:
        verbose_name = _('Bolletta')
        verbose_name_plural = _('Bollette')
        ordering = ('expiry_date',)


    def __str__(self):
        return '{} - {}'.format(self.title, self.expiry_date)
