import matplotlib.pyplot as plt

def pie_progress(starting, current, target):
    weight_lost = (starting - current)/(starting - target) * 100
    weight_to_lose = 100 - weight_lost
    portions = [weight_lost, weight_to_lose]
    labels = [f'Weight Lost: {starting-current} lbs', f'Weight Remaining: {current - target} lbs']
    explode = (0.1, 0)
    fig1, ax1 = plt.subplots()
    ax1.pie(portions, explode=explode, labels=labels,
            shadow=True, startangle=90,
            autopct='%1.1f%%')
    ax1.axis('equal')
    plt.show()

