
colors = (("green", "#00800"), ("blue", "#0000FF"))
#Convert tuple into dictionary
colors_as_dictionary = dict(colors)
print(colors_as_dictionary)


colors = (("green", "#00800"), ("blue", "#0000FF"))
colors_as_dictionary = dict((letter, number) for(number, letter) in colors)
print(colors_as_dictionary)
