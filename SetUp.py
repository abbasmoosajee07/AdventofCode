import numpy as np
import matplotlib.pyplot as plt

# Enable interactive mode
# plt.ion()

# Generate test data using numpy
x = np.linspace(0, 10, 100)  # 100 points from 0 to 10
y = np.sin(x) + np.random.normal(0, 0.1, 100)  # Sine wave with some noise

# Create a plot using matplotlib
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Noisy Sine Wave', color='b', marker='o', markersize=4, linestyle='--')
plt.title('Test Plot: Noisy Sine Wave')
plt.xlabel('X-axis (0 to 10)')
plt.ylabel('Y-axis (sin(x) + noise)')
plt.legend()
plt.grid(True)
plt.show()  # Display the plot inline in VS Code's interactive window
