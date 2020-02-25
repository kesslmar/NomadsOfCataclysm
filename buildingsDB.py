def loadDB():

    return {
        'RES': {
            'Organic Farm': {
                'Price': 250, 'Time': 60, 'enrgDrain': 200,
                'yield': 'Vegetable crates', 'incVal': 20, 'yieldText': '20 Vegetable crates per tick',
                'req': 'Athmosphere', 'decVal': 0, 'reqText': 'Athmosphere, 200 Energy',
                'desc': 'Basic vegetable farm to satisfy nutrition needs.',
                'img': 'models/organicfarm.jpg'},

            'Coal Drill': {
                'Price': 300, 'Time': 60, 'enrgDrain': 100,
                'yield': 'Coal sacks', 'incVal': 10, 'yieldText': '10 Coal sacks per tick',
                'req': 'Coal', 'decVal': 0, 'reqText': 'Coal, 100 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/coaldrill.jpg'},

            'Iron Mine': {
                'Price': 450, 'Time': 100, 'enrgDrain': 150,
                'yield': 'Iron ingots', 'incVal': 15, 'yieldText': '15 Iron ingots per tick',
                'req': 'Iron', 'decVal': 0, 'reqText': 'Iron, 150 Energy',
                'desc': 'Sophisticated mine to faciliate iron, which is used for further Production.',
                'img': 'models/ironmine.jpg'},

            'Uranium Site': {
                'Price': 600, 'Time': 300, 'enrgDrain': 500,
                'yield': 'Uranium containers', 'incVal': 5, 'yieldText': '5 Uranium containters per tick',
                'req': 'Uranium', 'decVal': 0, 'reqText': 'Uranium, 500 Energy',
                'desc': 'High tech facility to gather raw uranium. This has then to be enriched for further use.',
                'img': 'models/uraniumsite.jpg'}
        },
        'PRO': {
            'Weapon Forge': {
                'Price': 500, 'Time': 120, 'enrgDrain': 250,
                'yield': 'Weapons', 'incVal': 10, 'yieldText': '10 Weapons per tick',
                'req': 'Iron ingots', 'decVal': 10, 'reqText': '10 Iron ingots per tick, 250 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Ship Yard': {
                'Price': 550, 'Time': 130, 'enrgDrain': 300,
                'yield': 'Ships', 'incVal': 10, 'yieldText': '10 Ships per tick',
                'req': 'Iron ingots', 'decVal': 30, 'reqText': '30 Iron ingots per tick, 250 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Uranium Enricher': {
                'Price': 750, 'Time': 400, 'enrgDrain': 650,
                'yield': 'Uranium rods', 'incVal': 10, 'yieldText': '10 Uranium rods per tick',
                'req': 'Uranium containers', 'decVal': 5, 'reqText': '5 Uranium container per tick, 650 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'}
        },
        'ENR': {
            'Wind Turbine': {
                'Price': 150, 'Time': 30, 'enrgDrain': 0,
                'yield': 'Energy', 'incVal': 150, 'yieldText': '150 Energy',
                'req': 'Wind', 'decVal': 0, 'reqText': 'Wind',
                'desc': 'First instance of energy supply. Needs at least level 1 Wind activities.',
                'img': 'models/windgenerator.jpg'},

            'Coal Generator': {
                'Price': 300, 'Time': 50, 'enrgDrain': 0,
                'yield': 'Energy', 'incVal': 500, 'yieldText': '500 Energy',
                'req': 'Coal sacks', 'decVal': 5, 'reqText': '5 Coal sacks per tick',
                'desc': 'Delivers bigger and more reliable energy output. Polution might be a Prolbem though.',
                'img': 'models/coalplant.jpg'},

            'M.W. Transmitter': {
                'Price': 650, 'Time': 250, 'enrgDrain': 0,
                'yield': 'Energy', 'incVal': 1000, 'yieldText': '1000 Energy',
                'req': 'Micro waves', 'decVal': 0, 'reqText': 'Micro wave connection to other planet',
                'desc': 'Enables multiple Planents to send energy supply to each other.',
                'img': 'models/mw_transmitter.jpg'},

            'Nuclear Reactor': {
                'Price': 850, 'Time': 350, 'enrgDrain': 0,
                'yield': 'Energy', 'incVal': 5000, 'yieldText': '5000 Energy',
                'req': 'Uranium rods', 'decVal': 7, 'reqText': '7 Uranium rods per tick',
                'desc': 'Highest energy source that can be constructed planet site.',
                'img': 'models/powerplant.jpg'},

            'Dyson Sphere': {
                'Price': 3200, 'Time': 600, 'enrgDrain': 0,
                'yield': 'Energy', 'incVal': 50000, 'yieldText': '50000 Energy',
                'req': 'Sun', 'decVal': 0, 'reqText': 'Sun as center of construction',
                'desc': 'Experimental construction, which others' +   # noqa: W504
                        'refer to as the newest wonder of the known worlds.',
                'img': 'models/dysonsphere.jpg'}
        },
        'DEV': {
            'Trading Center': {
                'Price': 575, 'Time': 300, 'enrgDrain': 450,
                'yield': 'Trading ability', 'incVal': 0, 'yieldText': 'Trading ability',
                'req': None, 'decVal': 0, 'reqText': '450 Energy',
                'desc': 'Allows to set trading routes and to trade with the' +  # noqa: W504
                        'open galaxy market. Only one needed per solar system.',
                'img': 'models/placeholder.jpg'},

            'Milkyway Uni.': {
                'Price': 350, 'Time': 200, 'enrgDrain': 240,
                'yield': 'Society improvements', 'incVal': 0, 'yieldText': 'Society improvements',
                'req': None, 'decVal': 0, 'reqText': '240 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Science Institut': {
                'Price': 500, 'Time': 280, 'enrgDrain': 310,
                'yield': 'New researches', 'incVal': 0, 'yieldText': 'New researches',
                'req': None, 'decVal': 0, 'reqText': '310 Energy',
                'desc': 'Researches conducted by this institute allow enhancements of' +  # noqa: W504
                        'productivity and habitation standards.',
                'img': 'models/placeholder.jpg'},

            'Space Port': {
                'Price': 190, 'Time': 150, 'enrgDrain': 560,
                'yield': 'Space abilities', 'incVal': 0, 'yieldText': 'Space abilities',
                'req': None, 'decVal': 0, 'reqText': '560 Energy',
                'desc': 'Extends the interactions of a planet with its surrounding' +  # noqa: W504
                        'objects like asteroids or other celestial objects.',
                'img': 'models/placeholder.jpg'}
        },
        'HAB': {
            'Pod Settlement': {
                'Price': 120, 'Time': 30, 'enrgDrain': 120,
                'yield': 'Nomads', 'incVal': 100, 'yieldText': '100 Nomads',
                'req': None, 'decVal': 0, 'reqText': '120 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Skyscraper City': {
                'Price': 400, 'Time': 230, 'enrgDrain': 290,
                'yield': '900 Nomads', 'incVal': 900, 'yieldText': '900 Nomads',
                'req': 'Autom. Hospital', 'decVal': 0, 'reqText': 'Autom. Hospital, 290 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Sol Resort': {
                'Price': 625, 'Time': 240, 'enrgDrain': 360,
                'yield': 'Tourism ability', 'incVal': 0, 'yieldText': 'Tourism ability',
                'req': 'Skyscraper City', 'decVal': 0, 'reqText': 'Skyscraper City, 360 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'},

            'Autom. Hospital': {
                'Price': 350, 'Time': 200, 'enrgDrain': 230,
                'yield': 'TBD', 'incVal': 0, 'yieldText': 'TBD',
                'req': None, 'decVal': 0, 'reqText': '230 Energy',
                'desc': 'Simple mining drill to extract coal rescources of a planet.',
                'img': 'models/placeholder.jpg'}
        }
    }


if __name__ == '__main__':
    pass
