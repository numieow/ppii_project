import re
import Salad_long_responses as long
import random


def message_probability(user_message, recognised_words, required_words=[]):
    message_certainty = 0
    has_required_words = True
    
    # Counts how many words are present in each predefined message
    for word in user_message:
        
        if word in recognised_words:
            message_certainty += len(word)

    # Checks that the required words are in the string
    for word in required_words:
        if (not word in user_message) and len(word)>=1:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words :
        return int(message_certainty)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}
    data = open("sources.txt",'r',encoding='utf-8')
    contenu=data.readlines()
    def reponse(bot_response, list_of_words, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, required_words)
    for ele in contenu :
        if ele=='\n':
            pass
        else:
            rep,mots,necessaires=ele.split("§")
            
            liste_mots=re.split('/|\s',mots)

            necessaires=necessaires.strip() 
            
            liste_necessaires=re.split('/|\s',necessaires)
            for i in liste_necessaires : 
                if len(i)<=1:
                    liste_necessaires.remove(i)
            reponse(rep,liste_mots,liste_necessaires)
    
    # Longer responses
    reponse(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    reponse(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return long.INCOMPREHENSION[random.randrange(len(long.INCOMPREHENSION))] if highest_prob_list[best_match] < 1 else best_match


def get_response(user_input):
    user_input=user_input.strip(" ")
    if user_input=="quit":
        global courant
        courant=False
        return "A bientôt ! "
    split_message = re.split(r"\s+", user_input.lower())
    response = check_all_messages(split_message)
    return response

courant=True
# Testing the response system
#while courant:
#    print('SALAD: ' + get_response(input('You: ')))

#Amélioration : l'appelle a sources.txt se fait a chaque -check_all_messages, pourrait etre interressant de l'appeller quune fois...
