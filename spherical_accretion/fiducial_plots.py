import numpy as np

M = 1/2
r = 4

v = 0.5

gamma = 1 / np.sqrt(1-v**2)

y = gamma * np.sqrt(1 - 2 * M / r)

#%%

def norm(vec, M, r):
    g_00 = - (1 - 2 * M / r)
    g_11 = - 1/g_00
    return(vec[0]**2 * g_00 + vec[1]**2 * g_11)

#%%

e_t = [gamma**2 / y, -y*v]
e_r = [-v*gamma**2 / y,  y]

#%%

print(e_t)
print(e_r)
print(y)
print(gamma)

#%%

import plotly.graph_objects as go

# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in np.arange(0, 5, 0.1):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            x=np.arange(0, 10, 0.01),
            y=np.sin(step * np.arange(0, 10, 0.01))))

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="restyle",
        args=["visible", [False] * len(fig.data)],
    )
    step["args"][1][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.show()
