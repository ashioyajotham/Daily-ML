lst = [1, 2, 3, 4, 5]
lst.insert(1, 6) #replacing
del lst[0]
lst.append(1) #adding

print(lst)


areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, "bedroom", 10.75, "bathroom", 9.50]

# Add using + operator
areas_1 = areas + ["poolhouse", 24.5]
areas_2 = areas + ["garage", 12.8]


areas = ["hallway", 11.25, "kitchen", 18.0, "living room", 20.0, 
"bedroom", 10.75, "bathroom", 9.50, "poolhouse", 24.5, "garage", 15.45]
del areas[-4:-2] # ; separates two commands
print(areas)