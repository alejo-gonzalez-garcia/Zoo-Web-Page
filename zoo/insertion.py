from flask_sqlalchemy import SQLAlchemy
import datetime

def insertUser(user, db, model): 
        for characteristic in user:   
                new_user = model.User(email=characteristic[0], name=characteristic[1], last_name = characteristic[2], password_hash= characteristic[3], role = characteristic[4])
                db.session.add(new_user)
        db.session.commit()      

def insertAnimal(animals, db, model):
        for characteristic in animals:   
                new_animal = model.Animal(name=characteristic[0], scientific_name = characteristic[1], type= characteristic[2], diet = characteristic[3], weight = characteristic[4],
                size=characteristic[5], is_danger_extinction=characteristic[6], birthdate=characteristic[7], image = characteristic[8], continent=characteristic[9], habitat=characteristic[10], description=characteristic[11])
                db.session.add(new_animal)
        db.session.commit()

def insertAnimalHabitat(animal_habitats, db, model):
        for habitat in animal_habitats:   
                new_animal_habitat = model.AnimalHabitat(name = habitat)
                db.session.add(new_animal_habitat)
        db.session.commit()

def insertActivity(activities, db, model):
        for characteristic in activities:   
                new_activity = model.Activity(name=characteristic[0], description=characteristic[6], image = characteristic[2], minimum_age= characteristic[3], is_parent_required = characteristic[4], is_featured = characteristic[5], type_name = characteristic[1])
                db.session.add(new_activity)
        db.session.commit()

def insertActivityType(activity_types, db, model):
        for activity_type in activity_types:   
                new_activity_type = model.ActivityType(name = activity_type)
                db.session.add(new_activity_type)
        db.session.commit()

def insertActivitySchedule(activity_schedules, db, model):
        for characteristic in activity_schedules:   
                new_activity_schedule = model.ActivitySchedule(total=characteristic[0], timestamp=characteristic[1], price = characteristic[2], activity_id = characteristic[3])
                db.session.add(new_activity_schedule)
        db.session.commit()        

def insertActivityBooking(activity_booking, db, model):
        for characteristic in activity_booking:   
                new_activity_booking = model.ActivityBooking(timestamp=characteristic[0], seats_booked=characteristic[1], user_email = characteristic[2], activity_schedule_id  = characteristic[3])
                db.session.add(new_activity_booking)
        db.session.commit() 

def insert_data(model, app):

        db = SQLAlchemy(app=app)

        users = [ 
                ['customer@gmail.com', 'Customer', 'Customer', '$2b$12$j9zHT6xhYU2.L1rULbnsB.C2P6FP6wickSEYpRFuh.61E37GHDH36', 'customer'], #password is customer
                ['manager@gmail.com', 'Manager', 'Manager', '$2b$12$E6pIEtoafNpYmzDyfBp3zOeGRl5ljWcDnHmGF6k.clDj/Pyh5v3Ka', 'manager'] #password is manager
        ]
        insertUser(users, db, model)

        animals = [
                ['Koala', 'Phascolarctos cinereus', 'mamal', 'Herbivorous', 9.07, 320, True, datetime.date(2009, 4, 1), '/static/images/koala.png', 'Australia', 'Tropical', 'The koala is an iconic Australian animal. Often called the koala “bear,” this tree-climbing animal is a marsupial—a mammal with a pouch for the development of offspring.'],
                ['Zebra', 'Equus quagga', 'mamal', 'Herbivorous', 360, 122, False, datetime.date(2002, 4, 1), '/static/images/zebra1.png', 'Africa', 'Sabana', 'Zebras are African equines with distinctive black-and-white striped coats. They share the genus Equus with horses and asses, the three groups being the only living members of the family Equidae.'],
                ['Giraffe', 'Giraffa camelopardalis', 'mamal', 'Herbivorous', 990, 480, True, datetime.date(2019, 8, 5), '/static/images/giraffe.png', 'Africa','Sabana', 'The giraffe is a large African hoofed mammal belonging to the genus Giraffa. It is the tallest living terrestrial animal and the largest ruminant on Earth.'],
                ['Lion', 'Panthera leo', 'mamal', 'Carnivorous', 150, 195, False, datetime.date(2018, 8, 5), '/static/images/lion2.png', 'Africa', 'Sabana','The lion (Panthera leo) is a large cat of the genus Panthera native to Africa and India. It has a muscular, broad-chested body, short, rounded head, round ears, and a hairy tuft at the end of its tail.'],
                ['Woodpecker', 'Dryobates pubescens', 'bird', 'Omnivorous', 0.3 , 15, False, datetime.date(2021, 12, 3), '/static/images/woodpeaker.png', 'America','Forest', 'Woodpeckers are part of the bird family Picidae, which also includes the piculets, wrynecks, and sapsuckers. '],
                ['Rhinoceros', 'Ceratotherium simum', 'mamal', 'Herbivorous', 1500, 375, True, datetime.date(2005, 5, 7), '/static/images/rhino.png', 'Africa','Sabana', 'Rhinoceroses are some of the largest remaining megafauna: all weight at least one tonne in adulthood. They have a herbivorous diet, small brains (400–600 g) for mammals of their size, one or two horns, and a thick (1.5–5 cm), protective skin formed from layers of collagen positioned in a lattice structure.'],
                ['Red Fox', 'Vulpes vulpes', 'mamal', 'Carnivorous', 44, 95, False, datetime.date(2009, 3, 3), '/static/images/fox.png', 'Europe', 'Forest','Foxes are small to medium-sized, omnivorous mammals belonging to several genera of the family Canidae. They have a flattened skull, upright triangular ears, a pointed, slightly upturned snout, and a long bushy tail (or brush).'],
                ['Bengal Tiger', 'Panthera tigris tigris', 'mamal', 'Carnivorous', 200, 182, True, datetime.date(2012, 3, 4), '/static/images/tiger.png', 'Asia','Tropical', 'The tiger (Panthera tigris) is the largest living cat species and a member of the genus Panthera. It is most recognisable for its dark vertical stripes on orange fur with a white underside. An apex predator, it primarily preys on ungulates, such as deer and wild boar.'],
                ['Lemur', 'Ring-Tailed Lemur', 'mamal', 'Herbivorous', 2.72, 52, False, datetime.date(2010, 8, 9), '/static/images/lemur.png', 'Africa', 'Jungle','Lemurs are wet-nosed primates of the superfamily Lemuroidea, divided into 8 families and consisting of 15 genera and around 100 existing species. They are endemic to the island of Madagascar.'],
                ['Elephant', 'Loxodonta', 'mamal', 'Herbivorous', 5000, 300, True, datetime.date(1995, 10, 8), '/static/images/elephant.png', 'Africa','Sabana', 'Elephants are the largest existing land animals. Three living species are currently recognised: the African bush elephant, the African forest elephant, and the Asian elephant. They are the only surviving members of the family Elephantidae and the order Proboscidea. '],
                ['Flamingo', 'Phoenicopterus ruber', 'bird', 'Herbivorous', 1.3, 150, True, datetime.date(1993, 2, 15), '/static/images/flamingo.png', 'America','Steppe', 'The American flamingo is a large species of flamingo closely related to the greater flamingo and Chilean flamingo native to the Neotropics. It was formerly considered conspecific with the greater flamingo, but that treatment is now widely viewed as incorrect due to a lack of evidence.'],
                ['Penguins', 'Spheniscidae', 'bird', 'Carnivorous', 15, 63, True, datetime.date(2013, 12, 5), '/static/images/penguin.png', 'Antarctica', 'Glaciar', 'Highly adapted for life in the water, penguins have countershaded dark and white plumage and flippers for swimming. Most penguins feed on krill, fish, squid and other forms of sea life which they catch with their bills and swallow it whole while swimming']
        ]
        insertAnimal(animals, db, model)

        activity_types = ['Party', 'Guided Tour', 'Parents´ Day', 'Special Days', 'Creativity', 'Animal Feeding']
        insertActivityType(activity_types, db, model)
        
        activities = [
            ['Elon´s Birthday', activity_types[3], '/static/images/birthday_kid.png', 0, 0, 1, 'Do you want to celebrate the birthdate of your kids rounded of animals? Contact us!' ], 
            ['Valentine´s Day', activity_types[3] , '/static/images/valentin.png', 16, 0, 0, 'Come celebrate Valentine´s Day with us during the whole week of February! Meet babys and feel what it is like to hold one!'], 
            ['Mother´s Day', activity_types[2], '/static/images/mother.png', 0, 1, 0, 'Celebrate Mother´s Day with us on the zoo. You will have plenty of activities scheduled to demonstrate your mum´s love.'], 
            ['Father´s Day',  activity_types[2], '/static/images/father.png', 0, 1, 1, 'Come and celebrate your dad´s day with us! You will be able to make him be proud and feel relaxed on company of our animals!'], 
            ['Easter Holiday', activity_types[0], '/static/images/flamingoEaster.png', 4, 1, 1, 'Celebrate with us during all Eastern Week. Paint eggs and visit our caribbean flamingos!'], 
            ['Summer Holiday',  activity_types[0], '/static/images/summer2.png', 3, 0, 0, 'Enjoy the summer with the Final Lemmur Party. We have created a beach where you can play with our animals while remaining cooled!'], 
            ['Winter Holiday', activity_types[0], '/static/images/winter.png', 3, 0, 0, 'Come visit the penguins in a freezing experience. You can swim with them and see how they eat and life!'], 
            ['Christmas Holiday', activity_types[0], '/static/images/christmas.png', 3, 1, 1,'Happy Christmas!! Do you want to celebrate it with us? Come to visit the present´s factory surrounded of woodpeckers!'], 
            ['Mountain Trip',  activity_types[1], '/static/images/jeep.png', 10, 1, 1, 'Are you brave enough? Let´s visit the Klint Mountain with our off-road vehicles and watch the wild-nature!'],
            ['Elephant Trip',  activity_types[1], '/static/images/elephantTrip.png', 5, 0, 1, 'For our young participants, ride a 2 TONS elephant around the forest!'],
            ['Wood Sculpture',  activity_types[4], '/static/images/sculture.png', 6, 0, 0, 'Do you really know how important are Woodpeckers for the habitats where they life? You can actually learn how to make some real sculptures with the same techniques this special birds use!'],
            ['Koala Feeding',  activity_types[5], '/static/images/koalaFeed.png', 3, 0, 1, 'Have you ever wanted to see and hold a koala? You can come to help us feed them!']
        ]
        insertActivity(activities, db, model)

        activity_schedules = [
                [18, datetime.datetime(2022, 8, 23, 9, 15, 0), 15.96, 1], # 1 is the activity id! 
                [30, datetime.datetime(2022, 2, 1, 12, 0, 0), 15.96, 1], 
                [30, datetime.datetime(2022, 2, 1, 15, 30, 0), 15.96, 1], 
                [50, datetime.datetime(2022, 12, 5, 9, 15, 0), 15.96, 2],
                [30, datetime.datetime(2022, 2, 1, 12, 15, 0), 15.96, 2], 
                [30, datetime.datetime(2022, 3, 1, 9, 15, 0), 15.96, 3], 
                [30, datetime.datetime(2022, 4, 1, 12, 15, 0), 15.96, 3], 
                [30, datetime.datetime(2022, 5, 1, 9, 15, 0), 15.96, 4], 
                [30, datetime.datetime(2022, 6, 1, 12, 15, 0), 15.96, 4], 
                [30, datetime.datetime(2023, 7, 1, 9, 15, 0), 15.96, 5], 
                [30, datetime.datetime(2023, 8, 1, 12, 15, 0), 15.96, 5], 
                [30, datetime.datetime(2023, 9, 1, 9, 15, 0), 15.96, 6], 
                [30, datetime.datetime(2023, 10, 1, 12, 15, 0), 15.96, 6], 
                [30, datetime.datetime(2023, 11, 1, 9, 15, 0), 15.96, 7], 
                [30, datetime.datetime(2023, 1, 1, 12, 15, 0), 15.96, 7], 
                [30, datetime.datetime(2022, 12, 25, 21, 15, 0), 15.96, 8], 
                [30, datetime.datetime(2022, 12, 25, 22, 15, 0), 15.96, 8], 
                [30, datetime.datetime(2023, 2, 1, 9, 15, 0), 15.96, 9], 
                [30, datetime.datetime(2023, 3, 1, 12, 15, 0), 15.96, 9], 
                [30, datetime.datetime(2023, 4, 1, 9, 15, 0), 15.96, 10], 
                [30, datetime.datetime(2023, 5, 1, 12, 15, 0), 15.96, 10],
                [30, datetime.datetime(2023, 6, 1, 9, 15, 0), 15.96, 11], 
                [30, datetime.datetime(2023, 7, 1, 12, 15, 0), 15.96, 11],
                [30, datetime.datetime(2023, 8, 1, 9, 15, 0), 15.96, 12], 
                [30, datetime.datetime(2023, 9, 1, 12, 15, 0), 15.96, 12], 
                [30, datetime.datetime(2023, 10, 1, 12, 0, 0), 15.96, 1], 
                [30, datetime.datetime(2023, 11, 1, 15, 30, 0), 15.96, 1], 
                [50, datetime.datetime(2023, 12, 5, 9, 15, 0), 15.96, 2],
                [30, datetime.datetime(2023, 1, 1, 12, 15, 0), 15.96, 2], 
                [30, datetime.datetime(2023, 2, 1, 9, 15, 0), 15.96, 3], 
                [30, datetime.datetime(2023, 3, 1, 12, 15, 0), 15.96, 3], 
                [30, datetime.datetime(2023, 4, 1, 9, 15, 0), 15.96, 4], 
                [30, datetime.datetime(2023, 5, 1, 12, 15, 0), 15.96, 4], 
                [30, datetime.datetime(2022, 6, 1, 9, 15, 0), 15.96, 5], 
                [30, datetime.datetime(2022, 7, 1, 12, 15, 0), 15.96, 5], 
                [30, datetime.datetime(2022, 8, 1, 9, 15, 0), 15.96, 6], 
                [30, datetime.datetime(2022, 9, 1, 12, 15, 0), 15.96, 6], 
                [30, datetime.datetime(2022, 10, 1, 9, 15, 0), 15.96, 7], 
                [30, datetime.datetime(2022, 11, 1, 12, 15, 0), 15.96, 7], 
                [30, datetime.datetime(2022, 12, 25, 21, 15, 0), 15.96, 8], 
                [30, datetime.datetime(2022, 12, 25, 22, 15, 0), 15.96, 8], 
                [30, datetime.datetime(2022, 2, 1, 9, 15, 0), 15.96, 9], 
                [30, datetime.datetime(2022, 3, 1, 12, 15, 0), 15.96, 9], 
                [30, datetime.datetime(2022, 4, 1, 9, 15, 0), 15.96, 10], 
                [30, datetime.datetime(2022, 5, 1, 12, 15, 0), 15.96, 10],
                [30, datetime.datetime(2022, 6, 1, 9, 15, 0), 15.96, 11], 
                [30, datetime.datetime(2022, 7, 1, 12, 15, 0), 15.96, 11],
                [30, datetime.datetime(2022, 8, 1, 9, 15, 0), 15.96, 12], 
                [30, datetime.datetime(2022, 9, 1, 12, 15, 0), 15.96, 12]
        ]
        insertActivitySchedule(activity_schedules, db, model)

        activity_booking = [
                [datetime.datetime(2021, 1, 5), 1, users[0][0], 1], 
                [datetime.datetime(2020, 4, 2),3, users[0][0], 2], 
                [datetime.datetime(2023, 4, 2),10, users[0][0], 3], 
                [datetime.datetime(2020, 4, 2),4, users[0][0], 5], 
                [datetime.datetime(2020, 4, 2),6, users[0][0], 8], 
                [datetime.datetime(2020, 4, 2),2, users[1][0], 6], 
                [datetime.datetime(2020, 4, 2),7, users[1][0], 7], 
                [datetime.datetime(2020, 4, 2),7, users[1][0], 9], 
                [datetime.datetime(2022, 12, 12), 12, users[1][0], 10]
        ]
        insertActivityBooking(activity_booking, db, model)

