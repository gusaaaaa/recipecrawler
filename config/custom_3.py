# Random scheduler + Intersection Similarity Relevancy (tshold=2)

SCHEDULER = 'recipebot.randomscheduler.RandomScheduler'
SPIDER_CLASS = 'recipebot.spiders.intersectionbfs.IntersectionBfsSpider'
RELEVANCY_THRESHOLD = 2
KEYWORD_SET = set(['recipe', 'ingredient', 'cook', 'fish', 'beef',
    'pork', 'menu', 'food', 'dish', 'diet', 'fruit', 'egg'
    'vegetarian', 'gluten', 'oister', 'mussel'])
