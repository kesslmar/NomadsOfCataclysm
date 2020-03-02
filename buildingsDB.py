def loadDB():

    return {
        'RES': {
            'Organic Farm': {
                'price': 250, 'time': 60, 'enrDrain': 200,
                'yield': 'Vegetable crates', 'incVal': 20,
                'yieldText': '20 Vegetable crates per tick',
                'req': 'Athmosphere', 'decVal': 0,
                'reqText': 'Athmosphere, 200 Energy',
                'desc': 'Basic vegetable farm to satisfy nutrition needs.',
                'img': 'models/organicfarm.jpg'},

            'Coal Drill': {
                'price': 300, 'time': 60, 'enrDrain': 100,
                'yield': 'Coal sacks', 'incVal': 10,
                'yieldText': '10 Coal sacks per tick',
                'req': 'Coal', 'decVal': 0,
                'reqText': 'Coal, 100 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/coaldrill.jpg'},

            'Iron Mine': {
                'price': 450, 'time': 100, 'enrDrain': 150,
                'yield': 'Iron ingots', 'incVal': 15,
                'yieldText': '15 Iron ingots per tick',
                'req': 'Iron', 'decVal': 0,
                'reqText': 'Iron, 150 Energy',
                'desc': 'Sophisticated mine to faciliate iron, which ' +
                        'is used for further Production.',
                'img': 'models/ironmine.jpg'},

            'Uranium Site': {
                'price': 600, 'time': 300, 'enrDrain': 500,
                'yield': 'Uranium containers', 'incVal': 5,
                'yieldText': '5 Uranium containters per tick',
                'req': 'Uranium', 'decVal': 0,
                'reqText': 'Uranium, 500 Energy',
                'desc': 'High tech facility to gather raw uranium. This has ' +
                        'then to be enriched for further use.',
                'img': 'models/uraniumsite.jpg'}
        },
        'PRO': {
            'Weapon Forge': {
                'price': 500, 'time': 120, 'enrDrain': 250,
                'yield': 'Weapons', 'incVal': 10,
                'yieldText': '10 Weapons per tick',
                'req': 'Iron ingots', 'decVal': 10,
                'reqText': '10 Iron ingots per tick, 250 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Ship Yard': {
                'price': 550, 'time': 130, 'enrDrain': 300,
                'yield': 'Ships', 'incVal': 10,
                'yieldText': '10 Ships per tick',
                'req': 'Iron ingots', 'decVal': 30,
                'reqText': '30 Iron ingots per tick, 250 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Uranium Enricher': {
                'price': 750, 'time': 400, 'enrDrain': 650,
                'yield': 'Uranium rods', 'incVal': 10,
                'yieldText': '10 Uranium rods per tick',
                'req': 'Uranium containers', 'decVal': 5,
                'reqText': '5 Uranium container per tick, 650 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'}
        },
        'ENR': {
            'Wind Turbine': {
                'price': 150, 'time': 30, 'enrDrain': 0,
                'yield': 'Energy', 'incVal': 150,
                'yieldText': '150 Energy',
                'req': 'Wind', 'decVal': 0,
                'reqText': 'Wind',
                'desc': 'First instance of energy supply. Needs at least level 1 Wind activities.',
                'img': 'models/windgenerator.jpg'},

            'Coal Generator': {
                'price': 300, 'time': 50, 'enrDrain': 0,
                'yield': 'Energy', 'incVal': 500,
                'yieldText': '500 Energy',
                'req': 'Coal sacks', 'decVal': 5,
                'reqText': '5 Coal sacks per tick',
                'desc': 'Delivers bigger and more reliable energy output. ' +
                        'Polution might be a Prolbem though.',
                'img': 'models/coalplant.jpg'},

            'M.W. Transmitter': {
                'price': 650, 'time': 250, 'enrDrain': 0,
                'yield': 'Energy', 'incVal': 1000,
                'yieldText': '1000 Energy',
                'req': 'Micro waves', 'decVal': 0,
                'reqText': 'Micro wave connection to other planet',
                'desc': 'Enables multiple Planents to send energy supply to each other.',
                'img': 'models/mw_transmitter.jpg'},

            'Nuclear Reactor': {
                'price': 850, 'time': 350, 'enrDrain': 0,
                'yield': 'Energy', 'incVal': 5000,
                'yieldText': '5000 Energy',
                'req': 'Uranium rods', 'decVal': 7,
                'reqText': '7 Uranium rods per tick',
                'desc': 'Highest energy source that can be constructed planet site.',
                'img': 'models/powerplant.jpg'},

            'Dyson Sphere': {
                'price': 3200, 'time': 600, 'enrDrain': 0,
                'yield': 'Energy', 'incVal': 50000,
                'yieldText': '50000 Energy',
                'req': 'Sun', 'decVal': 0,
                'reqText': 'Sun as center of construction',
                'desc': 'Experimental construction, which others ' +
                        'refer to as the newest wonder of the known worlds.',
                'img': 'models/dysonsphere.jpg'}
        },
        'DEV': {
            'Trading Center': {
                'price': 575, 'time': 300, 'enrDrain': 450,
                'yield': 'Trading ability', 'incVal': 0,
                'yieldText': 'Trading ability',
                'req': None, 'decVal': 0,
                'reqText': '450 Energy',
                'desc': 'Allows to set trading routes and to trade with the ' +
                        'open galaxy market. Only one needed per solar system.',
                'img': 'models/placeholder.jpg'},

            'Milkyway Uni.': {
                'price': 350, 'time': 200, 'enrDrain': 240,
                'yield': 'Society improvements', 'incVal': 0,
                'yieldText': 'Society improvements',
                'req': None, 'decVal': 0,
                'reqText': '240 Energy',
                'desc': 'Performance and efficiency in habitation and consumption ' +
                        'can here get improved.',
                'img': 'models/placeholder.jpg'},

            'Science Institut': {
                'price': 500, 'time': 280, 'enrDrain': 310,
                'yield': 'New researches', 'incVal': 0,
                'yieldText': 'New researches',
                'req': None, 'decVal': 0,
                'reqText': '310 Energy',
                'desc': 'Researches conducted by this institute allow enhancements of ' +
                        'productivity and habitation standards.',
                'img': 'models/placeholder.jpg'},

            'Space Port': {
                'price': 190, 'time': 150, 'enrDrain': 560,
                'yield': 'Space abilities', 'incVal': 0,
                'yieldText': 'Space abilities',
                'req': None, 'decVal': 0,
                'reqText': '560 Energy',
                'desc': 'Extends the interactions of a planet with its surrounding ' +
                        'objects like asteroids or other celestial objects.',
                'img': 'models/placeholder.jpg'},

            'Academy': {
                'price': 430, 'time': 300, 'enrDrain': 440,
                'yield': 'Military', 'incVal': 0,
                'yieldText': 'Military',
                'req': None, 'decVal': 0,
                'reqText': '560 Energy',
                'desc': 'Enables to perform military operations in attack and defense.',
                'img': 'models/placeholder.jpg'}
        },
        'HAB': {
            'Pod Settlement': {
                'price': 120, 'time': 30, 'enrDrain': 120,
                'yield': 'Nomads', 'incVal': 100,
                'yieldText': '100 Nomads',
                'req': None, 'decVal': 0,
                'reqText': '120 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Skyscraper City': {
                'price': 400, 'time': 230, 'enrDrain': 290,
                'yield': '900 Nomads', 'incVal': 900,
                'yieldText': '900 Nomads',
                'req': 'Autom. Hospital', 'decVal': 0,
                'reqText': 'Autom. Hospital, 290 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Sol Resort': {
                'price': 625, 'time': 240, 'enrDrain': 360,
                'yield': 'Tourism ability', 'incVal': 0,
                'yieldText': 'Tourism ability',
                'req': 'Skyscraper City', 'decVal': 0,
                'reqText': 'Skyscraper City, 360 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Autom. Hospital': {
                'price': 350, 'time': 200, 'enrDrain': 230,
                'yield': 'TBD', 'incVal': 0,
                'yieldText': 'TBD',
                'req': None, 'decVal': 0,
                'reqText': '230 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'}
        }
    }


if __name__ == '__main__':
    pass
