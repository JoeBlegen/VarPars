import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt

st.set_option('deprecation.showPyplotGlobalUse', False)

class var:
    def __init__(self,label,min_val,max_val,units,set_val):
        self.label = label
        self.min_val = min_val
        self.max_val = max_val
        self.units = units
        self.set_val = set_val

perm_const = 8.8541878128 * (10**-12)

l = var('Length',0.1,0.5,'m',.2)
w = var('Width',0.1,0.5,'m',.2)
f = var('Frequency',400.0,1000.0,'kHz',500.0)
k = var('Dielectric Constant',1.0,5.0,'',3.0)
t = var('Dielectric Thickness',1.0,5.0,'mm',3.0)

pos_vars = [l,w,f,k,t]

if __name__ == "__main__":
    non_vis_var = []
    vis_var_label = st.sidebar.selectbox("Select variable to visualize",[x.label for x in pos_vars])
    for v in pos_vars:
        if vis_var_label == v.label:
            vis_var = v
        else:
            non_vis_var.append(v)

    vis_var.set_min_val, vis_var.set_max_val = st.sidebar.slider(f"Set {vis_var.label} range of vals",
                                            vis_var.min_val,vis_var.max_val,
                                            (float(vis_var.min_val*1.2),float(vis_var.max_val*.8)))

    for v in non_vis_var:
        v.set_val = st.sidebar.slider(f"Set {v.label} value",v.min_val,v.max_val,v.set_val)

    x_p = np.linspace(vis_var.set_min_val,vis_var.set_max_val,50)
    imp = (10**-3) / (2*np.pi*(10**3)*perm_const)

    for v in non_vis_var:
        if v.label == 'Dielectric Thickness':
            imp *= v.set_val  
        else:
            imp /= v.set_val

    if vis_var.label == "Dielectric Thickness":
        imp *= x_p
    else:
        imp /= x_p

    fig = plt.figure()
    ax=fig.add_subplot(111)
    for axis in ['top','bottom','left','right']:
       ax.spines[axis].set_linewidth(2)
    ax.tick_params(direction='in', length=6, width=2, colors='k')
    ax.tick_params(labelcolor='k', labelsize=14)
    plt.plot(x_p,imp,'r')
    plt.title(f"Impedance change based on {vis_var.label}", fontsize = 14)
    plt.grid()
    plt.xlabel(f'{vis_var.label} ({vis_var.units})',fontsize=14)
    plt.ylabel('Impedance (Ohms)',fontsize=14)
    st.pyplot()

