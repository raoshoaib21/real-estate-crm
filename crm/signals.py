from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from crm.models.deal import Deal
from crm.models.commission import Commission


@receiver(post_save, sender=Deal)
def create_commission_on_deal_closed(sender, instance, created, **kwargs):
    if instance.stage and instance.stage.name.lower() in ['closed', 'won']:
        if not instance.commissions.exists():
            Commission.objects.create(
                deal=instance,
                agent=instance.agent,
                deal_value=instance.deal_value,
                commission_rate=instance.agent.commission_rate if instance.agent else 5,
                status='pending',
            )
