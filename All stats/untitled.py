import streamlit as st
import pandas as pd
import hvplot.pandas
import holoviews as hv

front = "/Users/Jordandass/"

table_list = ["Desktop/FPL/All stats/fpl_prices_new.csv", 
"Desktop/FPL/All stats/fpl_points.csv", 
"Desktop/FPL/All stats/Player_possession.csv", 
"Desktop/FPL/All stats/Player_defense.csv",
"Desktop/FPL/All stats/Player_pass.csv",
"Desktop/FPL/All stats/Player_shot.csv"]



def get_scatter(min_games, multiple_position, position_chosen, max_price = 100):
    df = pd.read_csv("/Users/Jordandass/Desktop/FPL/All stats/fpl_points.csv")
    
    df_min = df[df["minutes"] >= 90 * min_games]
    df_min = df_min[df_min["position"].isin(position_chosen)]
    
    df_min = df_min[df_min["cost"] <= max_price]
    
    df_min["points_per_min"] = df_min["total_points"]/df_min["minutes"]
    df_min["points_per_mil"] = df_min["total_points"]/df_min["cost"]
    
    df_min.dropna(inplace=True)
    
    check_dict = {}
    if multiple_position == 'True':
        if "GKP" in position_chosen:
            df = df_min[df_min["position"] == "GKP"]
            if len(df) == 0:
                check_dict["GKP"] = False
            else:
                check_dict["GKP"] = True
                gkp_scatter = df_min[df_min["position"] == "GKP"].hvplot.scatter(x = "points_per_min", y = "points_per_mil", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
                gkp_slope = hv.Slope.from_scatter(gkp_scatter).opts(color = "yellow")
        
        if "DEF" in position_chosen:
            df = df_min[df_min["position"] == "DEF"]
            if len(df) == 0:
                check_dict["DEF"] = False
            else:
                check_dict["DEF"] = True
                def_scatter = df_min[df_min["position"] == "DEF"].hvplot.scatter(x = "points_per_min", y = "points_per_mil", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
                def_slope = hv.Slope.from_scatter(def_scatter).opts(color = "blue")
        
        if "MID" in position_chosen:
            df = df_min[df_min["position"] == "MID"]
            if len(df) == 0:
                check_dict["MID"] = False
            else:
                check_dict["MID"] = True
                mid_scatter = df_min[df_min["position"] == "MID"].hvplot.scatter(x = "points_per_min", y = "points_per_mil", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
                mid_slope = hv.Slope.from_scatter(mid_scatter).opts(color = "green")
        
        if "FWD" in position_chosen:
            df = df_min[df_min["position"] == "FWD"]
            if len(df) == 0:
                check_dict["FWD"] = False
            else:
                check_dict["FWD"] = True
                fwd_scatter = df_min[df_min["position"] == "FWD"].hvplot.scatter(x = "points_per_min", y = "points_per_mil", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
                fwd_slope = hv.Slope.from_scatter(fwd_scatter).opts(color = "red")
        
        full_scatter = df_min.hvplot.scatter(x = "points_per_min", y = "points_per_mil", by = "position", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
        
        list_to_eval = ["full_scatter"]
        for position in position_chosen:
            if check_dict[position] == True:
                list_to_eval.append(f"{position.lower()}_slope")
                
            
        return eval("*".join(list_to_eval)), df_min, gkp_slope, def_slope, mid_slope, fwd_slope
    
    else:
        scatter = df_min.hvplot.scatter(x = "points_per_min", y = "points_per_mil", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
        full_scatter = df_min.hvplot.scatter(x = "points_per_min", y = "points_per_mil", by = "position", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
        
        return [full_scatter * hv.Slope.from_scatter(scatter), df_min, hv.Slope.from_scatter(scatter)]
    
def team_chosen_scatter(team_chosen, min_games, multiple_position, position_chosen, max_price = 100):
    if multiple_position == "False":
        scatter, df, slope = get_scatter(min_games, multiple_position, position_chosen, max_price)

        team_df = df[df["team"].isin(team_chosen)]
    
        full_scatter = team_df.hvplot.scatter(x = "points_per_min", y = "points_per_mil", by = "position", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
    
        return full_scatter * slope
    
    elif multiple_position == "True":
        scatter, df, gkp_slope, def_slope, mid_slope, fwd_slope = get_scatter(min_games, multiple_position, position_chosen, max_price)
        
        team_df = df[df["team"].isin(team_chosen)]
    
        full_scatter = team_df.hvplot.scatter(x = "points_per_min", y = "points_per_mil", by = "position", hover_cols = ["name", "team", "position", "cost", "minutes", "total_points"])
    
        return full_scatter * gkp_slope * def_slope * mid_slope * fwd_slope

position_chosen = st.multiselect(
     'Position compared',
     ['GKP', 'DEF', 'MID', 'FWD'],
     ['GKP', 'DEF', 'MID', 'FWD'])    

min_games = st.select_slider(
     'Minimum amount of games played',
     options=list(range(0, 39)), 
    value = 10)

multiple_position = st.select_slider(
     'Regression lines by position',
     options=['True', 'False'])



df = pd.read_csv("/Users/Jordandass/Desktop/FPL/All stats/fpl_points.csv")
highest_price = sorted(df["cost"])[-1]
price = 0
price_list = []
while price <= highest_price:
    price_list.append(round(price, 1))
    price += 0.1

max_price = st.select_slider(
     'Maximum price of player',
     options=price_list, 
    value = highest_price)

nice_plot = get_scatter(min_games, multiple_position, position_chosen, max_price)

team_chosen = st.multiselect(
     'Team selection',
     ['AVL',
 'SOU',
 'LEI',
 'ARS',
 'LIV',
 'BHA',
 'EVE',
 'MCI',
 'BRE',
 'WHU',
 'TOT',
 'WOL',
 'LEE',
 'MUN',
 'CRY',
 'NEW',
 'CHE'],
     ['AVL',
 'SOU',
 'LEI',
 'ARS',
 'LIV',
 'BHA',
 'EVE',
 'MCI',
 'BRE',
 'WHU',
 'TOT',
 'WOL',
 'LEE',
 'MUN',
 'CRY',
 'NEW',
 'CHE'])  

nice_plot2 = team_chosen_scatter(team_chosen, min_games, multiple_position, position_chosen, max_price)
        
st.bokeh_chart(hv.render(nice_plot[0], backend='bokeh'))
st.bokeh_chart(hv.render(nice_plot2, backend='bokeh'))