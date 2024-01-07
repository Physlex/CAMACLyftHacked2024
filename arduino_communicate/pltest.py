import numpy as np
import matplotlib.pyplot as plt

# plt.axis([0, 10, 0, 1])

fig = plt.figure(figsize = (10, 5))
# plt.bar(courses, values, color ='maroon', width = 0.4)
plt.xlabel("Courses offered")
plt.ylabel("No. of students enrolled")
plt.title("Students enrolled in different courses")


while True:
  try:
    data = {'C': np.random.random(), 'C++': np.random.random(), 'Java': np.random.random(), 'Python': np.random.random()}
    courses = list(data.keys())
    values = list(data.values())
      
    # fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.clf()
    plt.bar(courses, values, color ='maroon', width = 0.4)

    ax = plt.gca()
    # ax.set_xlim([xmin, xmax])
    ax.set_ylim([0, 1])
    # plt.xlabel("Courses offered")
    # plt.ylabel("No. of students enrolled")
    # plt.title("Students enrolled in different courses")
    # plt.show()

  

    # y = np.random.random()
    # plt.scatter(i, y)
    plt.pause(0.05)
  
  except KeyboardInterrupt:
    print("\n\n== Terminating ==")
    break

# plt.show()