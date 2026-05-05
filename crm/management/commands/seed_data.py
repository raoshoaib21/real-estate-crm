from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, datetime, timedelta
import random
from crm.models.property import Property
from crm.models.lead import Lead, LeadSource
from crm.models.deal import Deal, PipelineStage
from crm.models.visit import SiteVisit
from crm.models.commission import Commission
from crm.models.interaction import Interaction, Task

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create pipeline stages
        stages_data = [
            {'name': 'Negotiation', 'order': 1, 'probability': 40, 'color': '#F59E0B'},
            {'name': 'Contract', 'order': 2, 'probability': 60, 'color': '#3B82F6'},
            {'name': 'Pending', 'order': 3, 'probability': 80, 'color': '#8B5CF6'},
            {'name': 'Closed', 'order': 4, 'probability': 100, 'color': '#10B981'},
            {'name': 'Lost', 'order': 5, 'probability': 0, 'color': '#EF4444'},
        ]

        stages = []
        for sd in stages_data:
            stage, _ = PipelineStage.objects.get_or_create(name=sd['name'], defaults=sd)
            stages.append(stage)

        # Create users
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'admin@propcrm.com',
                'role': 'admin',
                'phone': '+1-555-0100',
                'commission_rate': 5.0,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        manager_user, _ = User.objects.get_or_create(
            username='manager',
            defaults={
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah@propcrm.com',
                'role': 'manager',
                'phone': '+1-555-0101',
                'commission_rate': 5.0,
            }
        )
        manager_user.set_password('manager123')
        manager_user.save()

        agent_names = [
            ('mike', 'Mike', 'Williams', 'mike@propcrm.com', '+1-555-0201'),
            ('emma', 'Emma', 'Davis', 'emma@propcrm.com', '+1-555-0202'),
            ('james', 'James', 'Brown', 'james@propcrm.com', '+1-555-0203'),
        ]

        agents = []
        for username, first, last, email, phone in agent_names:
            agent, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': email,
                    'role': 'agent',
                    'phone': phone,
                    'commission_rate': random.choice([4.0, 5.0, 6.0]),
                }
            )
            agent.set_password('agent123')
            agent.save()
            agents.append(agent)

        self.stdout.write(f'Created {len(agents)} agents')

        # Create properties
        property_types = ['apartment', 'house', 'villa', 'commercial', 'land', 'plot']
        statuses = ['available', 'available', 'available', 'under_offer', 'sold']
        cities = ['New York', 'Los Angeles', 'Miami', 'Chicago', 'Houston', 'San Francisco']

        property_data = [
            ('Luxury Penthouse Downtown', 'apartment', 2500000, 3500, 4, 3, 'Manhattan', 'New York', 'NY'),
            ('Beachfront Villa', 'villa', 4800000, 5200, 5, 4, 'Malibu Beach', 'Los Angeles', 'CA'),
            ('Modern Studio Apartment', 'studio', 450000, 650, 1, 1, 'Brooklyn', 'New York', 'NY'),
            ('Family House with Garden', 'house', 1200000, 2800, 4, 2, 'Oak Park', 'Chicago', 'IL'),
            ('Commercial Office Space', 'commercial', 3200000, 8000, 0, 2, 'Financial District', 'San Francisco', 'CA'),
            ('Waterfront Estate', 'villa', 6500000, 7500, 6, 5, 'Star Island', 'Miami', 'FL'),
            ('Cozy 2BR Apartment', 'apartment', 750000, 1100, 2, 1, 'Midtown', 'New York', 'NY'),
            ('Suburban Family Home', 'house', 890000, 2200, 3, 2, 'Pasadena', 'Los Angeles', 'CA'),
            ('Development Land', 'land', 1500000, 45000, 0, 0, ' outskirts', 'Houston', 'TX'),
            ('Penthouse with Pool', 'penthouse', 3800000, 4200, 3, 3, 'South Beach', 'Miami', 'FL'),
            ('Downtown Loft', 'apartment', 920000, 1400, 2, 2, 'River North', 'Chicago', 'IL'),
            ('Residential Plot', 'plot', 350000, 12000, 0, 0, 'Suburbs', 'Houston', 'TX'),
        ]

        properties = []
        for title, ptype, price, area, beds, baths, address, city, state in property_data:
            prop = Property.objects.create(
                title=title,
                description=f'Beautiful {ptype.lower()} located in {city}. Features modern amenities and great views.',
                property_type=ptype,
                status=random.choice(statuses),
                price=price,
                negotiable=random.choice([True, False]),
                area_sqft=area,
                bedrooms=beds,
                bathrooms=baths,
                address=address,
                city=city,
                state=state,
                zip_code=f'{random.randint(10000, 99999)}',
                parking_spaces=random.randint(1, 4),
                listed_by=random.choice(agents + [admin_user]),
                featured=random.choice([True, False, False]),
                amenities={'pool': random.choice([True, False]), 'garage': random.choice([True, False]), 'garden': random.choice([True, False])},
            )
            properties.append(prop)

        self.stdout.write(f'Created {len(properties)} properties')

        # Create leads
        first_names = ['David', 'Emily', 'Michael', 'Jessica', 'Daniel', 'Ashley', 'Christopher', 'Amanda', 'Matthew', 'Stephanie', 'Andrew', 'Nicole', 'Joshua', 'Elizabeth', 'Ryan', 'Megan']
        last_names = ['Taylor', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee', 'Walker']

        lead_types = ['buyer', 'buyer', 'buyer', 'seller', 'renter']
        lead_statuses = ['new', 'new', 'contacted', 'qualified', 'proposal', 'negotiation', 'won', 'lost']
        lead_priorities = ['low', 'medium', 'medium', 'high', 'hot']
        sources = ['website', 'referral', 'walk_in', 'social', 'portal', 'cold_call']

        leads = []
        for i in range(30):
            lead = Lead.objects.create(
                lead_type=random.choice(lead_types),
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f'lead{i+1}@example.com',
                phone=f'+1-555-{random.randint(1000, 9999)}',
                source=random.choice(sources),
                status=random.choice(lead_statuses),
                assigned_to=random.choice(agents),
                priority=random.choice(lead_priorities),
                budget_min=random.choice([500000, 750000, 1000000, 1500000]),
                budget_max=random.choice([1000000, 1500000, 2000000, 3000000, 5000000]),
                preferred_location=random.choice(cities),
                preferred_type=random.choice(['any', 'apartment', 'house', 'villa']),
                requirements='Looking for a property with good amenities and location.',
            )
            leads.append(lead)

        self.stdout.write(f'Created {len(leads)} leads')

        # Create deals
        deal_values = [850000, 1200000, 2500000, 4800000, 750000, 1500000, 3200000, 920000, 6500000, 3800000]

        for i in range(10):
            deal = Deal.objects.create(
                lead=leads[i],
                deal_property=random.choice(properties),
                agent=random.choice(agents),
                stage=random.choice(stages[:4]),
                deal_value=random.choice(deal_values),
                deal_type='sale',
                expected_close_date=date.today() + timedelta(days=random.randint(15, 90)),
            )

            # Create commission for closed deals
            if deal.stage.name == 'Closed':
                deal.actual_close_date = date.today() - timedelta(days=random.randint(1, 30))
                deal.save()
                Commission.objects.create(
                    deal=deal,
                    agent=deal.agent,
                    deal_value=deal.deal_value,
                    commission_rate=deal.agent.commission_rate,
                    status=random.choice(['paid', 'approved']),
                    paid_date=date.today() if random.choice([True, False]) else None,
                )

        self.stdout.write('Created 10 deals')

        # Create site visits
        today = date.today()
        for i in range(8):
            SiteVisit.objects.create(
                lead=random.choice(leads[:15]),
                property=random.choice(properties),
                agent=random.choice(agents),
                scheduled_date=today + timedelta(days=random.randint(-5, 10)),
                scheduled_time=datetime.strptime(f'{random.randint(9, 17)}:{random.choice([0, 30]):02d}', '%H:%M').time(),
                status=random.choice(['scheduled', 'scheduled', 'completed', 'completed']),
            )

        self.stdout.write('Created 8 site visits')

        # Create interactions
        int_types = ['call', 'email', 'meeting', 'note']
        subjects = ['Initial consultation', 'Property viewing scheduled', 'Follow-up call', 'Offer discussion', 'Contract review', 'Price negotiation', 'Market update', 'Feedback session']

        for lead in leads[:20]:
            for _ in range(random.randint(1, 4)):
                Interaction.objects.create(
                    lead=lead,
                    interaction_type=random.choice(int_types),
                    subject=random.choice(subjects),
                    description=f'Discussed property options and requirements with {lead.first_name}.',
                    created_by=random.choice(agents + [admin_user]),
                    follow_up_date=today + timedelta(days=random.randint(1, 14)) if random.choice([True, False, False]) else None,
                )

        self.stdout.write('Created interactions')

        # Create tasks
        task_titles = ['Follow up with lead', 'Schedule property viewing', 'Prepare contract documents', 'Send market analysis', 'Call back potential buyer', 'Update property listing', 'Review offer details', 'Arrange inspection']

        for _ in range(15):
            Task.objects.create(
                title=random.choice(task_titles),
                assigned_to=random.choice(agents),
                related_lead=random.choice(leads) if random.choice([True, False]) else None,
                due_date=today + timedelta(days=random.randint(-2, 14)),
                priority=random.choice(['low', 'medium', 'medium', 'high', 'urgent']),
                status=random.choice(['pending', 'pending', 'in_progress', 'completed']),
            )

        self.stdout.write('Created tasks')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.WARNING('\nLogin credentials:'))
        self.stdout.write('  Admin:    admin / admin123')
        self.stdout.write('  Manager:  manager / manager123')
        self.stdout.write('  Agent:    mike / agent123')
