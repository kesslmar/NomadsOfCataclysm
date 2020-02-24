def loadDB():

    return {
        'RESC': {
            'Organic Farm': {   'Price': 250, 'Time': 60, 'yield': 'Vegetable crates', 'incVal': 20, 'yieldText': '20 Vegetable crates per tick',
                                'req': 'Athmosphere', 'decVal': 0, 'reqText': 'Athmosphere, 200 Energy', 'enrgDrain': 200,
                                'desc': 'Basic vegetable farm to satisfy nutrition needs.',
                                'img': 'models/organicfarm.jpg'},

            'Coal Drill': {     'Price': 300, 'Time': 60, 'yield': 'Coal sacks', 'incVal': 10, 'yieldText': '10 Coal sacks per tick', 
                                'req': 'Coal', 'decVal': 0, 'reqText': 'Coal, 100 Energy', 'enrgDrain': 100,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/coaldrill.jpg'},

            'Iron Mine': {      'Price': 450, 'Time': 100, 'yield': 'Iron ingots', 'incVal': 15, 'yieldText': '15 Iron ingots per tick',
                                'req': 'Iron', 'decVal': 0, 'reqText': 'Iron, 150 Energy', 'enrgDrain': 150,
                                'desc': 'Sophisticated mine to faciliate iron, which is used for further Production.',
                                'img': 'models/ironmine.jpg'},

            'Uranium Site': {   'Price': 600, 'Time': 300, 'yield': 'Uranium containers', 'incVal': 5, 'yieldText': '5 Uranium containters per tick',
                                'req': 'Uranium', 'decVal': 0, 'reqText': 'Uranium, 500 Energy', 'enrgDrain': 500,
                                'desc': 'High tech facility to gather raw uranium. This has then to be enriched for further use.',
                                'img': 'models/uraniumsite.jpg'}
        },
        'PROD':{
            'Weapon Forge': {   'Price': 500, 'Time': 120, 'yield': 'Weapons', 'incVal': 10, 'yieldText': '10 Weapons per tick',
                                'req': 'Iron ingots', 'decVal': 10, 'reqText': '10 Iron ingots per tick, 250 Energy', 'enrgDrain': 250,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'},

            'Ship Yard': {      'Price': 550, 'Time': 130, 'yield': 'Ships', 'incVal': 10, 'yieldText': '10 Ships per tick',
                                'req': 'Iron ingots', 'decVal': 30, 'reqText': '30 Iron ingots per tick, 250 Energy', 'enrgDrain': 300,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'},

            'Uranium Enricher':{'Price': 750, 'Time': 400, 'yield': 'Uranium rods', 'incVal': 10, 'yieldText': '10 Uranium rods per tick',
                                'req': 'Uranium containers', 'decVal': 5, 'reqText': '5 Uranium container per tick, 650 Energy', 'enrgDrain': 650,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'}
        },
        'ENRG':{
            'Wind Turbine': {   'Price': 150, 'Time': 30, 'yield': 'Energy', 'incVal': 150, 'yieldText': '150 Energy',
                                'req': 'Wind', 'decVal': 0, 'reqText': 'Wind', 'enrgDrain': 0,
                                'desc': 'First instance of energy supply. Needs at least level 1 Wind activities.',
                                'img': 'models/windgenerator.jpg'},

            'Coal Generator': { 'Price': 300, 'Time': 50, 'yield': 'Energy', 'incVal': 500, 'yieldText': '500 Energy',
                                'req': 'Coal sacks', 'decVal': 5, 'reqText': '5 Coal sacks per tick', 'enrgDrain': 0,
                                'desc': 'Delivers bigger and more reliable energy output. Polution might be a Prolbem though.',
                                'img': 'models/coalplant.jpg'},

            'M.W. Transmitter':{'Price': 650, 'Time': 250, 'yield': 'Energy', 'incVal': 1000, 'yieldText': '1000 Energy',
                                'req': 'Micro waves', 'decVal': 0, 'reqText': 'Micro wave connection to other planet', 'enrgDrain': 0,
                                'desc': 'Enables multiple Planents to send energy supply to each other.',
                                'img': 'models/mw_transmitter.jpg'},

            'Nuclear Reactor': {'Price': 850, 'Time': 350, 'yield': 'Energy', 'incVal': 5000, 'yieldText': '5000 Energy',
                                'req': 'Uranium rods', 'decVal': 7, 'reqText': '7 Uranium rods per tick', 'enrgDrain': 0,
                                'desc': 'Highest energy source that can be constructed planet site.',
                                'img': 'models/powerplant.jpg'},

            'Dyson Sphere': {   'Price': 3200, 'Time': 600, 'yield': 'Energy', 'incVal': 50000, 'yieldText': '50000 Energy',
                                'req': 'Sun', 'decVal': 0, 'reqText': 'Sun as center of construction',
                                'desc': 'Experimental construction, which others refer to as the newest wonder of the known worlds.', 'enrgDrain': 0,
                                'img': 'models/dysonsphere.jpg'}
        },
        'DEV':{
            'Trading Center': { 'Price': 575, 'Time': 300, 'yield': 'Trading ability', 'incVal': 0, 'yieldText': 'Trading ability',
                                'req': None, 'decVal': 0, 'reqText': '450 Energy', 'enrgDrain': 450,
                                'desc': 'Allows to set trading routes and to trade with the open galaxy market. Only one needed per solar system.',
                                'img': 'models/placeholder.jpg'},

            'Milkyway Uni.': {  'Price': 350, 'Time': 200, 'yield': 'Society improvements', 'incVal': 0, 'yieldText': 'Society improvements',
                                'req': None, 'decVal': 0, 'reqText': '240 Energy', 'enrgDrain':  240,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'},

            'Science Institut':{'Price': 500, 'Time': 280, 'yield': 'New researches', 'incVal': 0, 'yieldText': 'New researches',
                                'req': None, 'decVal': 0, 'reqText': '310 Energy', 'enrgDrain': 310,
                                'desc': 'Researches conducted by this institute allow enhancements of productivity and habitation standards.',
                                'img': 'models/placeholder.jpg'},

            'Space Port': {     'Price': 190, 'Time': 150, 'yield': 'Space abilities', 'incVal': 0, 'yieldText': 'Space abilities',
                                'req': None, 'decVal': 0, 'reqText': '560 Energy', 'enrgDrain': 560,
                                'desc': 'Extends the interactions of a planet with its surrounding objects like asteroids or other celestial objects.',
                                'img': 'models/placeholder.jpg'}
        },
        'HAB':{
            'Pod Settlement': { 'Price': 120, 'Time': 30, 'yield': 'Nomads', 'incVal': 100, 'yieldText': '100 Nomads',
                                'req': None, 'decVal': 0, 'reqText': '120 Energy', 'enrgDrain': 120,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'},

            'Skyscraper City': {'Price': 400, 'Time': 230, 'yield': '900 Nomads', 'incVal': 900,  'yieldText':  '900 Nomads',
                                'req': 'Autom. Hospital', 'decVal': 0, 'reqText': 'Autom. Hospital, 290 Energy', 'enrgDrain': 290,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'},

            'Sol Resort': {     'Price': 625, 'Time': 240, 'yield': 'Tourism ability', 'incVal': 0, 'yieldText':  'Tourism ability',
                                'req': 'Skyscraper City', 'decVal': 0, 'reqText': 'Skyscraper City, 360 Energy', 'enrgDrain':  360,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'},

            'Autom. Hospital': {'Price': 350, 'Time': 200, 'yield': 'TBD', 'incVal': 0, 'yieldText':  'TBD',
                                'req': None, 'decVal': 0, 'reqText': '230 Energy', 'enrgDrain': 230,
                                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                                'img': 'models/placeholder.jpg'}
        }
    }


if __name__ == '__main__':
    pass
