from django.utils import timezone
from datetime import timedelta,datetime
from faker import Faker
import os
import django
import random
from django.core.files import File

fake = Faker('en_IN')  
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# Initialize Django
django.setup()


from manage_account.models import Farmer
from dashboard.models import Cultivation, Inventory,Farms
from todo.models import Tasks




def create_sample_farmers():
    for _ in range(10):
        username = fake.user_name()
        password = username + '123'
        full_name = fake.name()
        phone_number = fake.phone_number()
        email = fake.email()
        company = fake.company()
        address = fake.address()

        Farmer.objects.create_user(
            username=username,
            password=password,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            company=company,
            address=address,
            is_active=True,  # Default to active users
            is_superuser=False,
            is_staff=False,
            date_joined=timezone.now(),
            last_login=timezone.now()  # Set last login to now
        )









def populate_Cultivation_Farms_Inventory():

    # List of rice types cultivated in India
    rice_types = ["Basmati Rice", "Jasmine Rice", "Parboiled Rice", "Red Rice", "Brown Rice"]

    # List of harvested rice products
    rice_products = ["Basmati Rice", "Jasmine Rice", "Parboiled Rice", "Red Rice", "Brown Rice"]

    Towns_kerala = ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Kollam', 'Thrissur', 'Kannur', 'Alappuzha', 'Palakkad', 'Malappuram', 'Ponnani', 'Vatakara', 'Tirur', 'Thalassery', 'Kottayam', 'Chalakudy', 'Neyyattinkara', 'Kayamkulam', 'Nedumangad', 'Kanjirappally', 'Kodungallur', 'Cherthala', 'Changanassery', 'Thiruvalla', 'Kunnamkulam', 'Kasaragod', 'Ottappalam', 'Thodupuzha', 'Chittoor', 'Muvattupuzha', 'Perinthalmanna', 'Adoor', 'Mannarkkad', 'Karunagappally', 'Thripunithura', 'Paravur', 'Pathanamthitta', 'Perumbavoor', 'Punalur', 'Nilambur', 'Chengannur', 'Angamaly', 'Painavu', 'Pattambi', 'Taliparamba', 'Piravom', 'Manjeri', 'Cheruvannur', 'Irinjalakuda', 'Kothamangalam', 'Pala', 'Payyanur', 'Kattappana', 'Haripad', 'Attingal', 'Wadakkancherry', 'Kalpetta', 'Sultan Bathery', 'Shoranur', 'Koduvally', 'Kondotty', 'Vaikom', 'Mavelikkara', 'Koothattukulam', 'Thaliparamba', 'Guruvayur', 'Mattannur', 'Koyilandy', 'Kannur', 'Kunnamangalam', 'Thrikkakara', 'Kuttippuram', 'Chavakkad', 'Thalassery', 'Kannur']

    # Get 10 Farmer instances
    users = Farmer.objects.all()[:50]

    for user in users:
        # Create Fields for each user
        Farms.objects.create(user=user,location=random.choice(Towns_kerala),status = random.choice(["good production",'average production','below average production'])
    )

        # Generate Cultivation for each user
        for _ in range(50):
            product = random.choice(rice_types)
            location = random.choice(Towns_kerala) + ", Kerala"
            cultivated_area = f"{random.randint(5, 20)} acres"  # Random area between 5 and 100 acres
            description = fake.text()

            # Generate a start date
            start_date = fake.date_time_this_year()
            random_hours = random.randint(7, 17)
            random_minutes = random.randint(0, 59)
            start_date = start_date.replace(hour=random_hours , minute= random_minutes,second=0) #creating fake start date and time

            # Calculate the end date ensuring at least a 50-day gap43
            random_hours = random.randint(6, 18)
            random_minutes = random.randint(0, 59)
                # Adding the random time to the harvestDate
            end_date = start_date + timedelta(days=random.randrange(50,60))
            end_date = end_date.replace(hour=random_hours, minute=random_minutes, second=0)
            # Generate a date within the range

            current_date = datetime(2023, 11, 13,14,45,00) #setting current date for data 

            if current_date < end_date: 
                status = "harvested"
                new_harvestDate = end_date
            else:
                status = "not_harvested"
                new_harvestDate =None # will only work if attribute accespts null value

            random_str=  str(user.username) + str(random.randint(0, 90000)) 
            product_id = f"{product}{random_str}"

            # Create Cultivation instance for the user
            cultivation = Cultivation.objects.create(
                user=user,
                product=product,
                status=status,
                location=location,
                cultivated_area=cultivated_area,
                start_date=start_date,
                harvested_date = new_harvestDate,
                description=description,
                product_id=product_id
            )

            # Create Inventory for harvested rice products
            if status == "harvested" and product in rice_products:
                Inventory.objects.create(
                    user=user,
                    product=product,
                    quantity=str(int(cultivated_area.split(' ')[0])*1092) + ' kg'# Matching the cultivated area in Inventory quantity
                )



def addHarvest():
    dataset = Cultivation.objects.all()
    for data in dataset:
        if data.status == 'harvested':
            new_harvestDate = data.start_date + timedelta(day= 60).date()
            Cultivation.harvested_date = new_harvestDate
            Cultivation.save()


#better and correct implementation of above function by chatgpt
def addHarvestDateandTime():
    # Fetch all instances where status is 'harvested'
    dataset = Cultivation.objects.filter(status='harvested')

    for data in dataset:
        new_harvestDate = data.start_date + timedelta(days=60) # timedelta takes days as argument not day
        # Generating a random time between 6:00 AM (6 hours) and 6:00 PM (18 hours)
        random_hours = random.randint(6, 18)
        random_minutes = random.randint(0, 59)
        
        # Adding the random time to the new_harvestDate
        new_harvestDate = new_harvestDate.replace(hour=random_hours, minute=random_minutes, second=0)
        
        data.harvested_date = new_harvestDate# storing only the date
        data.save() #we need to save the istance , not the class so use data.save() not Cultivation.save()

'''Changing class-level data directly affects all instances created from that class. 
However, it's important to note that this isn’t a standard practice.
Modifying instance data via the class, like Cultivation.harvested_date = new_date,
 will impact all instances of Cultivation, effectively changing the default value
for any new instances created but not affecting existing instances.
'''

'''attempting to change the class attribute directly (Cultivation.harvested_date = new_harvestDate)
 would mean you're changing the default value for the harvested_date attribute 
 in the Cultivation class definition, not the value of a specific instance's attribute.
 '''



def set_random_profile_photos():
    # Path to the folder containing profile photos
    profile_photos_folder = 'profilepics/'

    # Get a list of all files in the profile photos folder
    profile_photos = os.listdir(profile_photos_folder)

    # Retrieve all Farmer objects
    farmers = Farmer.objects.all()

    for farmer in farmers:
        # Choose a random profile photo from the folder
        random_photo = random.choice(profile_photos)

        # Construct the full path to the selected profile photo
        photo_path = os.path.join(profile_photos_folder, random_photo)

        # Open the file and create a Django File object
        with open(photo_path, 'rb+') as file:
            django_file = File(file)

            # Save the file to the media folder using the default storage
            farmer.profile_pic.save(random_photo, django_file)


rice_types = ["Basmati Rice", "Jasmine Rice", "Parboiled Rice", "Red Rice", "Brown Rice"]
def inventory_images():
    image_folder = 'inventoryproducts/'
    images = os.listdir(image_folder)
    inventory = Inventory.objects.all()
    
    for produces in inventory:
        if produces.product == 'Basmati Rice':
            image = 'fresh-basmati-rice.jpeg'
            image_path = os.path.join(image_folder,image)
            with open(image_path ,'rb+') as file:
                inventory_image_file = File(file)
                Inventory.images.save(image,inventory_image_file)

        elif produces.product == 'Jasmine Rice':
            image = 'thai-jasmine-rice.jpeg'
            image_path = os.path.join(image_folder,image)
            with open(image_path ,'rb+') as file:
                inventory_image_file = File(file)
                Inventory.images.save(image,inventory_image_file)

        elif produces.product == 'Parboiled Rice':
            image = 'parboild.jpg'
            image_path = os.path.join(image_folder,image)
            with open(image_path ,'rb+') as file:
                inventory_image_file = File(file)
                Inventory.images.save(image,inventory_image_file)

        elif produces.product == 'Red Rice':
            image = 'organic-red-rice-500x5001-1-1200x900.jpg'
            image_path = os.path.join(image_folder,image)
            with open(image_path ,'rb+') as file:
                inventory_image_file = File(file)
                Inventory.images.save(image,inventory_image_file)

        elif produces.product == 'Brown Rice':
            image = 'organic-brown-rice.jpeg'
            image_path = os.path.join(image_folder,image)
            with open(image_path ,'rb+') as file:
                inventory_image_file = File(file)
                Inventory.images.save(image,inventory_image_file)
        
        else:
            continue
        



    # optimised code from chatgpt
        
def inventory_images2():
    image_folder = 'inventoryproducts/'
    inventory = Inventory.objects.all()
    product_images = {
        "Basmati Rice": "fresh-basmati-rice.jpeg",
        "Jasmine Rice": "thai-jasmine-rice.jpeg",
        "Parboiled Rice": "parboild.jpg",
        "Red Rice": "organic-red-rice-500x5001-1-1200x900.jpg",
        "Brown Rice": "organic-brown-rice.jpeg"
    }
    
    for product in inventory:
        image_name = product_images.get(product.product)
        if image_name:
            image_path = os.path.join(image_folder, image_name)
            try:
                with open(image_path, 'rb') as file:
                    inventory_image_file = File(file)
                    product.images.save(image_name, inventory_image_file)
            except FileNotFoundError:
                print(f"Image file not found for product: {product.product}")
            except Exception as e:
                print(f"Error processing image for product {product.product}: {e}")

    
inventory_images2()