from flask import request
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import Span, Label
import pandas as pd


def TransCalc(trans_type, trans_dist):
    if trans_type == "Personal Car (Non-Electric)":
        emission = 0.1224*trans_dist
        return emission
    elif trans_type == "Carpooling":
        emission = (0.1224*trans_dist)/4
        return emission
    elif trans_type == "Transit":
        emission = 0.050*trans_dist
        return emission
    else:
        print("Error: Transport type invalid.")
        return


def EnergyCalc(energy_type, energy_use):
    if energy_type == "Coal-Powered":
        emission = 0.996*energy_use
        return emission
    elif energy_type == "Oil-Powered":
        emission = 0.735*energy_use
        return emission
    elif energy_type == "Hydroelectric":
        emission = 0.0185*energy_use
        return emission
    elif energy_type == "Nuclear":
        emission = 0.004*energy_use
        return emission
    elif energy_type == "Wind":
        emission = 0.004*energy_use
        return emission
    elif energy_type == "Solar":
        emission = 0.006*energy_use
    elif energy_type == "Geothermal":
        emission = 0.05*energy_use
    else:
        print("Error: Energy type invalid.")


def HousingCalc(house_sel, peep_no):
    # 569.5 kg-CO2/m2
    if house_sel == "Bachelor Apartment":
        emission = (569.5*50)/peep_no
    elif house_sel == "1-2 BHK Apartment":
        emission = (595.5*65)/peep_no
    elif house_sel == "3-4 BHK Apartment":
        emission = (595.5*120)/peep_no
    elif house_sel == "Townhouse":
        emission = (595.5*150)/peep_no
    elif house_sel == "Detached House":
        emission = (595.5*185)/peep_no
    else:
        print("Error: House type invalid.")
        return

    return emission


def consumeCalc(consume_sel):
    if consume_sel == "Apparel":
        clothes_no = float(request.form.get("clothes-no"))
        shoes_no = float(request.form.get("clothes-no"))
        emission = 20*clothes_no + 12.5*shoes_no
    elif consume_sel == "Electronics":
        phones_no = float(request.form.get("phones-no"))
        comp_no = float(request.form.get("comp-no"))
        emission = 60*phones_no+120*comp_no
    elif consume_sel == "Household":
        decor_no = float(request.form.get("decor-no"))
        appliance_no = float(request.form.get("appliance-no"))
        emission = 70*decor_no+200*appliance_no
    else:
        print("Error: Consumer good type invalid.")

    return emission


class emission():
    def __init__(self, all_emissions):
        self.all_emissions = all_emissions
        self.trans_emm = 0
        self.food_emm = 0
        self.energy_emm = 0
        self.water_emm = 0
        self.housing_emm = 0
        self.consume_emm = 0
        self.total_emm = 0

    def emmSum(self):
        for emission in self.all_emissions:
            if emission["Type"] == "Transport":
                self.trans_emm += emission["COe"]
            elif emission["Type"] == "Food":
                self.food_emm += emission["COe"]
            elif emission["Type"] == "Energy":
                self.energy_emm += emission["COe"]
            elif emission["Type"] == "Water":
                self.water_emm += emission["COe"]
            elif emission["Type"] == "Housing":
                self.housing_emm += emission["COe"]
            elif emission["Type"] == "Consumer Goods":
                self.consume_emm += emission["COe"]
        self.total_emm = self.trans_emm + self.food_emm + self.energy_emm + \
            self.water_emm + self.housing_emm + self.consume_emm
        return self.total_emm

    def emmGraph(self):
        plot = figure(plot_height=300, x_axis_type='datetime',
                      sizing_mode='stretch_both')
        emm_date = []
        emm_amt = []
        for emission in self.all_emissions:
            try:
                if emm_date.count(emission["Date"]) >= 1:
                    i = emm_date.index(emission["Date"])
                    emm_amt[i] += emission["COe"]
                else:
                    emm_date.append(emission["Date"])
                    emm_amt.append(emission["COe"])
            except:
                emm_date.append(emission["Date"])
                emm_amt.append(emission["COe"])
        emm_date = pd.to_datetime(emm_date)
        plot.line(emm_date, emm_amt, line_width=4, line_color="#50a476")
        avg_label = Label(y=0, x=400, x_units='screen',
                          text='World Average', text_color="red")
        plot.add_layout(avg_label)
        avg_line = Span(location=400,
                        dimension='width', line_color='red',
                        line_dash='dashed', line_width=3)
        plot.add_layout(avg_line)

        plot.background_fill_color = "#001b0b"
        plot.toolbar.autohide = True
        plot.y_range.start = 0

        plot.xgrid.grid_line_color = "#50a476"
        plot.xgrid.grid_line_alpha = 0.5
        plot.xgrid.grid_line_dash = [6, 4]
        plot.ygrid.grid_line_color = "#50a476"
        plot.ygrid.grid_line_alpha = 0.5
        plot.ygrid.grid_line_dash = [6, 4]

        plot.xaxis.axis_label = "Date"
        plot.xaxis.axis_label_text_color = "#50a476"
        plot.xaxis.axis_line_color = "#50a476"
        plot.xaxis.axis_line_color = "#50a476"
        plot.xaxis.major_label_text_color = "#50a476"
        plot.xaxis.minor_tick_line_color = None
        plot.xaxis.major_tick_line_color = "#50a476"

        plot.yaxis.axis_label = "CO2 equiv (kgs)"
        plot.yaxis.axis_label_text_color = "#50a476"
        plot.yaxis.axis_line_color = "#50a476"
        plot.yaxis.axis_line_color = "#50a476"
        plot.yaxis.major_label_text_color = "#50a476"
        plot.yaxis.minor_tick_line_color = "#50a476"
        plot.yaxis.major_tick_line_color = "#50a476"

        plot.border_fill_color = "#00242e"
        plot.outline_line_color = "#50a476"

        script, div = components(plot)
        return script, div

    def ftprint(self):
        ratftprint = {
            "Transport": [float("{:.3g}".format((self.trans_emm/self.total_emm)*100)), "#ef476f"],
            "Food":  [float("{:.3g}".format((self.food_emm/self.total_emm)*100)), "#ffd166"],
            "Energy":  [float("{:.3g}".format((self.energy_emm/self.total_emm)*100)), "#83d483"],
            "Water":  [float("{:.3g}".format((self.water_emm/self.total_emm)*100)), "#06d6a0"],
            "Housing":  [float("{:.3g}".format((self.housing_emm/self.total_emm)*100)), "#118ab2"],
            "Consume":  [float("{:.3g}".format((self.consume_emm/self.total_emm)*100)), "#073b4c"]
        }
        return ratftprint
