import random
import numpy

if __name__ == "__main__":

    skills=[
        'Vue',
        'React',
        'React Native',

        'SQL',
        'MongoDB',
        'R',

        'C#',
        'Python',

        'Entrepeneurship',
        'Language learning',
        'Economics',
        'Excel',
    ]
    print("You should study {}".format(
        random.choice(skills)
    ))