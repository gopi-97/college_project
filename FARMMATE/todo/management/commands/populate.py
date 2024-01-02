
from django.core.management.base import BaseCommand
import random
import os
import django
import datetime
from faker import Faker
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FarmMate.settings")
# Initialize Django
django.setup()
fake = Faker()

from manage_account.models import Farmer
from todo.models import Tasks

#python manage.py populate

class Command(BaseCommand):

    def handle(self, *args, **options) -> str | None:

        farm_tasks = {
            'Prepare Soil for Planting': 'Check soil moisture, clear debris, and till the land for the upcoming planting season.',
            'Purchase Seeds and Fertilizers': 'Research and buy high-quality seeds and fertilizers suitable for the crops to be cultivated.',
            'Schedule Irrigation System Check': 'Ensure proper functioning of irrigation systems; inspect pipes, valves, and timers for efficient water distribution.',
            'Plan Crop Rotation Strategy': 'Determine a rotation schedule to optimize soil fertility and minimize disease risks for different crop seasons.',
            'Arrange Pest Control Measures': 'Schedule pest monitoring and implement pest control measures to safeguard crops from infestation.',
            'Conduct Soil Testing': 'Collect soil samples and conduct tests for nutrient levels, pH, and other factors essential for crop health.',
            'Schedule Pruning Session': 'Plan and execute pruning activities for trees, vines, or bushes to promote healthy growth.',
            'Monitor Weather Forecasts': 'Stay updated with weather predictions to make informed decisions regarding planting, harvesting, and crop protection.',
            'Arrange Harvesting Equipment': 'Prepare and organize harvesting machinery and tools for efficient crop collection.',
            'Implement Weed Control Methods': 'Deploy weed management strategies such as mulching, manual removal, or selective herbicide application.',
            'Plan Crop Protection Measures': 'Develop a strategy to protect crops from diseases, considering fungicides or disease-resistant varieties.',
            'Schedule Livestock Vaccinations': 'Organize vaccinations and health checkups for livestock to maintain their well-being.',
            'Perform Equipment Maintenance': 'Service and maintain farming machinery, ensuring they\'re in good working condition.',
            'Check Market Prices': 'Research market trends and prices to decide on the right time for crop sales or purchases.',
            'Evaluate Previous Season\'s Performance': 'Analyze the outcomes of the last season to identify strengths, weaknesses, and areas for improvement.',
            'Implement Crop Covering': 'Apply covering methods like plastic mulch or row covers to protect crops from adverse weather or pests.',
            'Monitor Watering Schedule': 'Review and adjust watering schedules based on seasonal changes and crop requirements.',
            'Conduct Field Surveys': 'Inspect fields regularly for signs of disease, pest infestation, or other issues requiring attention.',
            'Plan Soil Amendments': 'Determine necessary soil amendments like compost or organic matter to enhance soil quality.',
            'Arrange Crop Storage Facilities': 'Prepare storage areas and facilities for harvested crops to maintain their quality.',
            'Implement Sustainable Farming Practices': 'Adopt eco-friendly methods to conserve resources and promote environmental sustainability.',
            'Schedule Field Crop Inspections': 'Conduct regular inspections to identify nutrient deficiencies or signs of diseases in crops.',
            'Plan Cover Crop Planting': 'Prepare and plant cover crops to improve soil health and prevent erosion during off-seasons.',
            'Arrange Machinery Upgrades': 'Upgrade or modernize farming equipment for improved efficiency and reduced resource consumption.',
            'Monitor Crop Growth Progress': 'Regularly monitor and track the growth stages of crops to assess their health and development.',
            'Implement Integrated Pest Management': 'Deploy integrated approaches to manage pests, including biological control and habitat manipulation.',
            'Schedule Crop Harvesting Techniques Workshop': 'Organize workshops to educate farmworkers on optimal crop harvesting methods.',
            'Plan Crop Diversity Strategies': 'Diversify crop selections to mitigate risks associated with market fluctuations and climate change.',
            'Evaluate Soil Erosion Control Measures': 'Assess and refine strategies to control soil erosion and maintain soil structure.',
            "Arrange Farmer's Market Participation": "Prepare produce and participate in local farmer's markets to promote farm products."
        }

        users = Farmer.objects.all()[:50]

        for user in users:
            # Randomly select 5 tasks for each user
            selected_tasks = random.sample(list(farm_tasks.items()), k=5)
            
            for title, description in selected_tasks:
                task = Tasks.objects.create(
                    user_id=user,
                    title=title,
                    description=description,
                    complete=random.choice([True, False]),
                    created= fake.date_time_this_year()  # Consider if you want a fixed time for all tasks
                )











