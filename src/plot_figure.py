import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Load the CSV file
    data = pd.read_csv('tests/tests200b.csv')
    print(data.head())
    # Extract the columns
    n = data["n"]
    t1 = data["t1"]
    t2 = data["t2"]

    # Create a new figure
    plt.figure()

    # Plot the points and connect them with straight lines
    plt.plot(n, t1, '-o', label='Nasz algorytm')
    plt.plot(n, t2, '-o', label='Brute-force')

    # Add labels and title
    plt.xlabel('n')
    plt.ylabel('Czas (s)')

    # Add legend
    plt.legend()

    # Show the figure
    plt.show()