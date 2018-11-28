from src.poet_class import Poet

user_input = "lgrgrgrgrgrg"

#create instance of imdb class
poet_object = Poet(user_input)

#get target poem

target_poem = poet_object.get_poem()

print(target_poem)
