import numpy as np
import plotly.express as px  
import plotly.offline as pyo
import warnings
warnings.filterwarnings("ignore")
import plotly
from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
import pandas as pd
import re
import os
def Report(Results, sets_df, names, reference_system_df):
    
    #creating source, sink and stream IDs
    reslist = []
    for i in sets_df['TECHNOLOGY']['TECHNOLOGY']:
        res = re.findall('(\d+|[A-Za-z]+)', i)
        reslist.append(res)

    streamidlist = []
    sourcesinkidlist = []
    for i in range(0,len(reslist)):
        k = reslist[i]
        if len(k) > 1 and k[0] != 'str':
            streamidlist.append(k[3])
            sourcesinkidlist.append(k[1])
    streamidlistd = []
    sourcesinkidlistd = []

    for i in streamidlist:
        if int(i) not in streamidlistd:
            streamidlistd.append(int(i))

    for i in sourcesinkidlist:
        if int(i) not in sourcesinkidlistd:
            sourcesinkidlistd.append(int(i))

    # Start Visualization
    a = Results
    #Accumulated New Capacity
    AccumulatedNewCapacity = pd.DataFrame(a['AccumulatedNewCapacity'])
    AccumulatedNewCapacity = AccumulatedNewCapacity.loc[AccumulatedNewCapacity["TECHNOLOGY"] != "dhn"]
    Tech_list1 = AccumulatedNewCapacity['TECHNOLOGY'].tolist()
    Assign1 = []
    Assignt1 = []
    Assign2 = []
    Assign4 = []
    for x in Tech_list1:
        if("grid") in x:
            Assign1.append("Grid Specific")
            Assignt1.append('Grid Specific')
            Assign4.append('')
        elif ("dhn") in x:
            Assign1.append("District Heating Network")
            Assign4.append('')
        else:
            for j in names:
                i = int(j)
                if (','.join(["sou%dstr" % i ])) in x:
                    Assign1.append(names[j])
                elif (','.join(["sink%dstr" % i ])) in x:
                    Assign1.append(names[j])
            for i in sourcesinkidlistd:
                if (','.join(["sou%dstr" % i ])) in x:
                    Assignt1.append(','.join(["Source%d" % i ]))            
                elif (','.join(["sink%dstr" % i ])) in x:
                    Assignt1.append(','.join(["Sink%d" % i ]))
                elif x.endswith(','.join(["sou%d" % i ])) is True:
                    Assignt1.append('stream')
            if "sou" or "sink" in x:
                res = re.findall('(\d+|[A-Za-z]+)', str(x))
                for i in streamidlistd:
                        if len(res) > 1 and res[0] != 'str':
                            if(','.join(["%d" % i ])) == str(res[3]):
                                Assign4.append(','.join(["Stream%d" % i ]))
                        elif len(res) > 1 and res[0] == 'str':
                            if(','.join(["%d" % i ])) == str(res[1]):
                                Assign4.append(','.join(["Stream%d" % i ]))
            else:
                Assign4.append('')
            for i in streamidlistd:
                if(','.join(["str%dsou" % i ])) in x:
                    Assign1.append(','.join(["Stream%d" % i ])) 

        if ("gridspecificngboiler") in x:
            Assign2.append("Grid Specific Natural gas Boiler")
        elif ("gridspecificelboiler") in x:
            Assign2.append("Grid Specific Electric Boiler")
        elif ("gridspecificoilboiler") in x:
            Assign2.append("Grid Specific Oil Boiler")
        elif ("gridspecificbioboiler") in x:
            Assign2.append("Grid Specific Biomass Boiler")
        elif ("gridspecifichp") in x:
            Assign2.append("Grid Specific Heat Pump")
        elif ("gridspecificsthp") in x:
            Assign2.append("Grid Specific solar thermal with Heat Pump")
        elif ("dhn") in x:
            Assign2.append("District Heating Network")
        elif ("she") in x:
            Assign2.append("Single Heat Exchanger")      
        elif ("mhe") in x:
            Assign2.append("Multiple Heat Exchanger")
        elif ("elwhrb") in x:
            Assign2.append("Electric Heat Recovery Boiler")
        elif ("ngwhrb") in x:
            Assign2.append("Natural Gas Heat Recovery Boiler")
        elif ("oilwhrb") in x:
            Assign2.append("Oil Heat Recovery Boiler")
        elif ("biowhrb") in x:
            Assign2.append("Biomass Heat Recovery Boiler")
        elif ("chpng") in x:
            Assign2.append("Natural Gas CHP")
        elif ("chpoil") in x:
            Assign2.append("Oil CHP")
        elif ("chpbio") in x:
            Assign2.append("Biomass CHP")
        elif ("boosthp") in x:
            Assign2.append("Booster Heat Pump")
        elif ("sthp") in x:
            Assign2.append("Solar thermal Heat Pump")
        elif ("stngboiler") in x:
            Assign2.append("Solar thermal with Natural gas boiler")
        elif ("stoilboiler") in x:
            Assign2.append("Solar thermal with oil boiler")
        elif ("stbioboiler") in x:
            Assign2.append("Solar thermal with biomass boiler")
        elif ("stelboiler") in x:
            Assign2.append("Solar thermal with el boiler")
        elif x.endswith('ac') is True:
            Assign2.append("Absorption Chiller")
        elif x.endswith('acec') is True:
            Assign2.append("Absorption Chiller with Electric Chiller")
        elif ("acngboiler") in x:
            Assign2.append("Absorption Chiller with Natural gas boiler")
        elif ("acoilboiler") in x:
            Assign2.append("Absorption Chiller with oil boiler")
        elif ("acbioboiler") in x:
            Assign2.append("Absorption Chiller with biomass boiler")
        elif ("acelectricboiler") in x:
            Assign2.append("Absorption Chiller with electric boiler")  
        elif ("acecngboiler") in x:
            Assign2.append("Absorption Chiller and Electric Chiller with Natural gas boiler")
        elif ("acecoilboiler") in x:
            Assign2.append("Absorption Chiller and Electric Chiller with oil boiler")
        elif ("acecbioboiler") in x:
            Assign2.append("Absorption Chiller and Electric Chiller with biomass boiler")
        elif ("acecelectricboiler") in x:
            Assign2.append("Absorption Chiller and Electric Chiller with electric boiler")
        elif ("acechp") in x:
            Assign2.append("Absorption Chiller and Electric Chiller with heat pump")
        elif ("achp") in x:
            Assign2.append("Absorption Chiller with heat pump")
        elif ("orc") in x:
            Assign2.append("Organic Rankine Cycle")
        elif ("exgrid") in x:
            Assign2.append("Existing Grid Technologies")
        elif("hp") in x:
            for i in streamidlistd:
                if(','.join(["str%dhp" % i ])) in x:
                    Assign2.append("Heat Pump") 
        else:
            Assign2.append(" ")

    Assign3 = []
    for i in range(0, len(Assign1)):
        if Assign1[i] in Assign2[i]:
            Assign3.append(Assign2[i])
        elif Assign2[i] == '':
            Assign3.append(str(str(Assign1[i]) + str(Assign2[i])))
        elif Assign4[i] in Assign1[i]:
            Assign3.append(str(str(Assign1[i] + ' ' + str(Assign2[i]))))
        elif Assign4[i] not in Assign1[i]:
            Assign3.append(str(str(Assign1[i] + ' ' + Assign4[i] + ' ' + str(Assign2[i]))))

    AccumulatedNewCapacity['Assignment'] = Assign3
    AccumulatedNewCapacity = AccumulatedNewCapacity.drop(['TECHNOLOGY'], axis = 1)
    AccumulatedNewCapacity = AccumulatedNewCapacity.drop(['NAME'], axis = 1)
    AccumulatedNewCapacity.rename(columns={"Assignment": "TECHNOLOGY"}, inplace=True)
    AccumulatedNewCapacity = AccumulatedNewCapacity[['VALUE', 'TECHNOLOGY', 'YEAR']]
    AccumulatedNewCapacityplot = AccumulatedNewCapacity.pivot_table(AccumulatedNewCapacity,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
    AccumulatedNewCapacityplot = AccumulatedNewCapacityplot.reset_index()
    # del AccumulatedNewCapacityplot['index']
    AccumulatedNewCapacityplot = AccumulatedNewCapacityplot.droplevel(level=0, axis=1)
    
    streamidlistunique = []
    for i in streamidlist:
        if i not in streamidlistunique:
            streamidlistunique.append(i)

    for i in streamidlistunique:
        s = str("Stream" + str(i) + "  ")
        if s in AccumulatedNewCapacityplot.columns.tolist():
            del AccumulatedNewCapacityplot[str(s)]
    
    list1 = AccumulatedNewCapacityplot.columns.tolist()
    list1.remove('')

    fig = px.bar(AccumulatedNewCapacityplot, x='', y=list1)
    fig.update_layout(
        title="Accumulated New Capacity",
        title_x=0.45,
        xaxis_title="Year",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Capaciy in kW",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )


    #source wise graph creation

    AccumulatedNewCapacity['Assignment'] = Assignt1
    Techlist = AccumulatedNewCapacity["Assignment"].tolist()
    Assign4 = []
    for x in Techlist:
        if "Source" in x:
            Assign4.append("Source")
        else:
            Assign4.append('')

    AccumulatedNewCapacity['Classification'] = Assign4
    Classlist = AccumulatedNewCapacity["Classification"].tolist()
    AccumulatedNewCapacitySource = AccumulatedNewCapacity.loc[AccumulatedNewCapacity["Classification"] == "Source"]
    del AccumulatedNewCapacitySource['Classification']
    del AccumulatedNewCapacitySource['Assignment']
    Techlist = AccumulatedNewCapacitySource["TECHNOLOGY"].tolist()

    Assign5 = []

    for x in Techlist:
        for i in names:
            if str(str(names[str(i)])+ ' ') in x:
                    Assign5.append(names[str(i)])

    AccumulatedNewCapacitySource['Classification'] = Assign5
    ancsou = []    
    for i in names:
        if (names[str(i)]) in AccumulatedNewCapacitySource['Classification'].unique():
            df = AccumulatedNewCapacitySource.loc[AccumulatedNewCapacitySource["Classification"] == names[str(i)]]
            dfplot = df.pivot_table(df,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
            dfplot = dfplot.reset_index()
            dfplot = dfplot.droplevel(level=0, axis=1)
            list2 = dfplot.columns.tolist()
            list2.remove('')
            fig2 = px.bar(dfplot, x='', y=list2)
            fig2.update_layout(
                title=('Accumulated New Capacity for' + ' ' + str(names[str(i)])),
                title_x=0.45,
                xaxis_title="Year",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Capaciy in kW",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )

            ancsouel = plotly.io.to_html(fig2, full_html=False,include_plotlyjs=False)
            ancsou.append(ancsouel)

    # Sink wise graphs
    AccumulatedNewCapacity['Assignment'] = Assignt1
    Techlist = AccumulatedNewCapacity["Assignment"].tolist()
    Assign6 = []
    for x in Techlist:
        if "Sink" in x:
            Assign6.append("Sink")
        else:
            Assign6.append('')
    AccumulatedNewCapacity['Classification'] = Assign6
    Classlist = AccumulatedNewCapacity["Classification"].tolist()

    AccumulatedNewCapacitySink = AccumulatedNewCapacity.loc[AccumulatedNewCapacity["Classification"] == "Sink"]
    del AccumulatedNewCapacitySink['Classification']
    Techlist = AccumulatedNewCapacitySink["TECHNOLOGY"].tolist()

    Assign7 = []
    for x in Techlist:
        for i in names:
            if str(str(names[str(i)])+ ' ') in x:
                Assign7.append(names[str(i)]) 
    AccumulatedNewCapacitySink['Classification'] = Assign7

    ancsi = []          
    for i in names:
        if (names[str(i)]) in AccumulatedNewCapacitySink['Classification'].unique():
            df = AccumulatedNewCapacitySink.loc[AccumulatedNewCapacitySink["Classification"] == names[str(i)]]
            dfplot1 = df.pivot_table(df,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
            dfplot1 = dfplot1.reset_index()
            dfplot1 = dfplot1.droplevel(level=0, axis=1)
            list3 = dfplot1.columns.tolist()
            list3.remove('')
            fig3= px.bar(dfplot1, x='', y=list3)
            fig3.update_layout(
                title=('Accumulated New Capacity for' + ' ' + str(names[str(i)])),
                title_x=0.45,
                xaxis_title="Year",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Capaciy in kW",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            ancsiuel = plotly.io.to_html(fig3, full_html=False,include_plotlyjs=False)
            ancsi.append(ancsiuel)

    # Grid Specific
    Techlist = AccumulatedNewCapacity["TECHNOLOGY"].tolist()
    Assign8 = []
    for x in Techlist:
        if "Grid" in x:
            Assign8.append("Grid Specific")
        else:
            Assign8.append('')

    if "Grid Specific" in Assign8:
        AccumulatedNewCapacity['Classification'] = Assign8
        AccumulatedNewCapacityGrid = AccumulatedNewCapacity.loc[AccumulatedNewCapacity["Classification"] == "Grid Specific"]
        AccumulatedNewCapacityGridplot = AccumulatedNewCapacityGrid.pivot_table(AccumulatedNewCapacityGrid,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
        AccumulatedNewCapacityGridplot = AccumulatedNewCapacityGridplot.reset_index()
        AccumulatedNewCapacityGridplot = AccumulatedNewCapacityGridplot.droplevel(level=0, axis=1)
        list4 = AccumulatedNewCapacityGridplot.columns.tolist()
        list4.remove('')
        fig4 = px.bar(AccumulatedNewCapacityGridplot, x='', y=list4)
        fig4.update_layout(
            title=("Accumulated New Capacity for Grid Specific Technologies"),
            title_x=0.45,
            xaxis_title="Year",
            paper_bgcolor='#FFFFFF',
            yaxis_title="Capaciy in kW",
            legend_title="Technologies",
            font=dict(
                family="Times New Roman",
                size=12,
                color="Black"
            )
        )


    #AccumulatedNewStorageCapacity
    AccumulatedNewStorageCapacity = pd.DataFrame(a['AccumulatedNewStorageCapacity'])
    if len(AccumulatedNewStorageCapacity) != 0:
        AccumulatedNewStorageCapacityplot = AccumulatedNewStorageCapacity.pivot_table(AccumulatedNewStorageCapacity,index=['YEAR'],columns=['STORAGE'],aggfunc=np.sum)
        AccumulatedNewStorageCapacityplot = AccumulatedNewStorageCapacityplot.reset_index()
        AccumulatedNewStorageCapacityplot = AccumulatedNewStorageCapacityplot.droplevel(level=0, axis=1)
        liststo = AccumulatedNewStorageCapacityplot.columns.tolist()
        liststo.remove('')


        figsto = px.bar(AccumulatedNewStorageCapacityplot, x='', y=liststo)
        figsto.update_layout(
            title="Accumulated New Storage Capacity",
            title_x=0.45,
            xaxis_title="Year",
            paper_bgcolor='#FFFFFF',
            yaxis_title="Storage Capacity in kWh",
            legend_title="Storage",
            font=dict(
                family="Times New Roman",
                size=12,
                color="Black"
            )
        )
    else:
        figsto = ''


    #AnnualTechnologyEmission all combined, sink and source specific

    #AnnualTechnologyEmission all combined

    AnnualTechnologyEmission = pd.DataFrame(a['AnnualTechnologyEmission'])

    Tech_listem = AnnualTechnologyEmission['TECHNOLOGY'].tolist()
    Assignem1 = []
    Assignemt1 = []
    Assignem2 = []
    Assignem4 = []                
    for x in Tech_listem:
        if("grid") in x:
            Assignem1.append("Grid Specific")
            Assignemt1.append("Grid Specific")
            Assignem4.append('')
        elif ("dhn") in x:
            Assignem1.append("District Heating Network")
            Assignem4.append('')
        else:
            for j in names:
                i = int(j)
                if (','.join(["sou%dstr" % i ])) in x:
                    Assignem1.append(names[j])
                elif (','.join(["sink%dstr" % i ])) in x:
                    Assignem1.append(names[j])
            for i in sourcesinkidlistd:
                if (','.join(["sou%dstr" % i ])) in x:
                    Assignemt1.append(','.join(["Source%d" % i ]))            
                elif (','.join(["sink%dstr" % i ])) in x:
                    Assignemt1.append(','.join(["Sink%d" % i ]))
                elif x.endswith(','.join(["sou%d" % i ])) is True:
                    Assignemt1.append('stream')
            if "sou" or "sink" in x:
                res = re.findall('(\d+|[A-Za-z]+)', str(x))
                for i in streamidlistd:
                        if len(res) > 1 and res[0] != 'str':
                            if(','.join(["%d" % i ])) == str(res[3]):
                                Assignem4.append(','.join(["Stream%d" % i ]))
                        elif len(res) > 1 and res[0] == 'str':
                            if(','.join(["%d" % i ])) == str(res[1]):
                                Assignem4.append(','.join(["Stream%d" % i ]))
            else:
                Assignem4.append('')
            
            for i in streamidlistd:
                if(','.join(["str%dsou" % i ])) in x:
                    Assignem1.append(','.join(["Stream%d" % i ])) 

        if ("gridspecificngboiler") in x:
            Assignem2.append("Grid Specific Natural gas Boiler")
        elif ("gridspecificelboiler") in x:
            Assign2.append("Grid Specific Electric Boiler")
        elif ("gridspecificoilboiler") in x:
            Assignem2.append("Grid Specific Oil Boiler")
        elif ("gridspecificbioboiler") in x:
            Assignem2.append("Grid Specific Biomass Boiler")
        elif ("gridspecifichp") in x:
            Assignem2.append("Grid Specific Heat Pump")
        elif ("gridspecificsthp") in x:
            Assignem2.append("Grid Specific solar thermal with Heat Pump")
        elif ("dhn") in x:
            Assignem2.append("District Heating Network")
        elif ("she") in x:
            Assignem2.append("Single Heat Exchanger")      
        elif ("mhe") in x:
            Assignem2.append("Multiple Heat Exchanger")
        elif ("elwhrb") in x:
            Assignem2.append("Electric Waste Heat Recovery Boiler")
        elif ("ngwhrb") in x:
            Assignem2.append("Natural Gas Heat Recovery Boiler")
        elif ("oilwhrb") in x:
            Assignem2.append("Oil Heat Recovery Boiler")
        elif ("biowhrb") in x:
            Assignem2.append("Biomass Heat Recovery Boiler")
        elif ("chpng") in x:
            Assignem2.append("Natural Gas CHP")
        elif ("chpoil") in x:
            Assignem2.append("Oil CHP")
        elif ("chpbio") in x:
            Assignem2.append("Biomass CHP")
        elif ("boosthp") in x:
            Assignem2.append("Booster Heat Pump")
        elif ("sthp") in x:
            Assignem2.append("Solar thermal Heat Pump")
        elif ("stngboiler") in x:
            Assignem2.append("Solar thermal with Natural gas boiler")
        elif ("stoilboiler") in x:
            Assignem2.append("Solar thermal with oil boiler")
        elif ("stbioboiler") in x:
            Assignem2.append("Solar thermal with biomass boiler")
        elif ("stelboiler") in x:
            Assignem2.append("Solar thermal with el boiler")
        elif x.endswith('ac') is True:
            Assignem2.append("Absorption Chiller")
        elif x.endswith('acec') is True:
            Assignem2.append("Absorption Chiller with Electric Chiller")
        elif ("acngboiler") in x:
            Assignem2.append("Absorption Chiller with Natural gas boiler")
        elif ("acoilboiler") in x:
            Assignem2.append("Absorption Chiller with oil boiler")
        elif ("acbioboiler") in x:
            Assignem2.append("Absorption Chiller with biomass boiler")
        elif ("acelectricboiler") in x:
            Assignem2.append("Absorption Chiller with electric boiler")  
        elif ("acecngboiler") in x:
            Assignem2.append("Absorption Chiller and Electric Chiller with Natural gas boiler")
        elif ("acecoilboiler") in x:
            Assignem2.append("Absorption Chiller and Electric Chiller with oil boiler")
        elif ("acecbioboiler") in x:
            Assignem2.append("Absorption Chiller and Electric Chiller with biomass boiler")
        elif ("acecelectricboiler") in x:
            Assignem2.append("Absorption Chiller and Electric Chiller with electric boiler")
        elif ("acechp") in x:
            Assignem2.append("Absorption Chiller and Electric Chiller with heat pump")
        elif ("achp") in x:
            Assignem2.append("Absorption Chiller with heat pump")
        elif ("orc") in x:
            Assignem2.append("Organic Rankine Cycle")
        elif ("exgrid") in x:
            Assignem2.append("Existing Grid Technologies")        
        
        elif("hp") in x:
            for i in streamidlistd:
                if(','.join(["str%dhp" % i ])) in x:
                    Assignem2.append("Heat Pump") 
        else:
            Assignem2.append(" ")

    Assignem3= []

    for i in range(0, len(Assignem1)):
        if Assignem1[i] in Assignem2[i]:
            Assignem3.append(Assignem2[i])
        elif Assignem2[i] == '':
            Assignem3.append(str(str(Assignem1[i]) + str(Assignem2[i])))
        else:
            Assignem3.append(str(str(Assignem1[i]) + ' ' + str(Assignem4[i])+ ' ' + str(Assignem2[i])))
    Assignem3

    AnnualTechnologyEmission['Assignment'] = Assignem3
    AnnualTechnologyEmission = AnnualTechnologyEmission.drop(['TECHNOLOGY'], axis = 1)
    AnnualTechnologyEmission = AnnualTechnologyEmission.drop(['NAME'], axis = 1)
    AnnualTechnologyEmission.rename(columns={"Assignment": "TECHNOLOGY"}, inplace=True)
    AnnualTechnologyEmission = AnnualTechnologyEmission[['VALUE', 'TECHNOLOGY', 'YEAR']]
    AnnualTechnologyEmissionplot = AnnualTechnologyEmission.pivot_table(AnnualTechnologyEmission,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
    AnnualTechnologyEmissionplot = AnnualTechnologyEmissionplot.reset_index()
    AnnualTechnologyEmissionplot = AnnualTechnologyEmissionplot.droplevel(level=0, axis=1)
    listem = AnnualTechnologyEmissionplot.columns.tolist()
    listem.remove('')

    figem = px.bar(AnnualTechnologyEmissionplot, x='', y=listem)
    figem.update_layout(
        title="Annual Technology Emissions",
        title_x=0.45,
        xaxis_title="Year",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Emissions in Kg Co2eq",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )



    # source wise emissions graph creation

    AnnualTechnologyEmission["assigment"] = Assignemt1
    Techlist = AnnualTechnologyEmission["assigment"].tolist()
    Assignem4 = []
    for x in Techlist:
        if "Source" in x:
            Assignem4.append("Source")
        else:
            Assignem4.append('')
    AnnualTechnologyEmission['Classification'] = Assignem4
    AnnualTechnologyEmissionSource = AnnualTechnologyEmission.loc[AnnualTechnologyEmission["Classification"] == "Source"]
    del AnnualTechnologyEmissionSource['assigment']
    Techlist = AnnualTechnologyEmissionSource["TECHNOLOGY"].tolist()
    
    Assignem5 = []
    for x in Techlist:
        for i in names:
                if str(str(names[str(i)])+ ' ') in x:
                    Assignem5.append(names[str(i)]) 

    AnnualTechnologyEmissionSource['Classification'] = Assignem5

    emso = []
    for i in names:
        if (names[str(i)]) in AnnualTechnologyEmissionSource["Classification"].unique():
            df = AnnualTechnologyEmissionSource.loc[AnnualTechnologyEmissionSource["Classification"] == (names[str(i)])]
            dfplot = df.pivot_table(df,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
            dfplot = dfplot.reset_index()
            dfplot = dfplot.droplevel(level=0, axis=1)
            listem2 = dfplot.columns.tolist()
            listem2.remove('')
            figsoem = px.bar(dfplot, x='', y=listem2)
            figsoem.update_layout(
                title=(','.join(["Annual Technology Emissions for" + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Year",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Emissions in Kg Co2eq",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            emsouel = plotly.io.to_html(figsoem, full_html=False,include_plotlyjs=False)
            emso.append(emsouel)
    # Sink wise emission graphs

    AnnualTechnologyEmission["assigment"] = Assignemt1
    Techlist = AnnualTechnologyEmission["assigment"].tolist()
    Assign6em= []
    for x in Techlist:
        if "Sink" in x:
            Assign6em.append("Sink")
        else:
            Assign6em.append('')
    AnnualTechnologyEmission['Classification'] = Assign6em
    Classlist = AnnualTechnologyEmission["Classification"].tolist()

    AnnualTechnologyEmissionSink = AnnualTechnologyEmission.loc[AnnualTechnologyEmission["Classification"] == "Sink"]
    del AnnualTechnologyEmissionSink['Classification']
    Techlist = AnnualTechnologyEmissionSink["TECHNOLOGY"].tolist()

    Assign7em= []

    for x in Techlist:
        for i in names:
                if str(str(names[str(i)])+ ' ') in x:
                    Assign7em.append(names[str(i)])

    AnnualTechnologyEmissionSink['Classification'] = Assign7em

    emsi = []
    for i in names:
        if (names[str(i)]) in AnnualTechnologyEmissionSink['Classification'].unique():
            df = AnnualTechnologyEmissionSink.loc[AnnualTechnologyEmissionSink["Classification"] == (names[str(i)])]
            dfplot1 = df.pivot_table(df,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
            dfplot1 = dfplot1.reset_index()
            dfplot1 = dfplot1.droplevel(level=0, axis=1)
            list3siem = dfplot1.columns.tolist()
            list3siem.remove('')
            fig3siem= px.bar(dfplot1, x='', y=list3siem)
            fig3siem.update_layout(
                title=(','.join(["Annual Technology Emissions for" + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Year",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Emissions in Kg Co2eq",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            emsiuel = plotly.io.to_html(fig3siem, full_html=False,include_plotlyjs=False)
            emsi.append(emsiuel)        

    # Grid Specific Emissions
    AnnualTechnologyEmission
    Techlist = AnnualTechnologyEmission["TECHNOLOGY"].tolist()
    Assign8em = []
    for x in Techlist:
        if "Grid" in x:
            Assign8em.append("Grid Specific")
        else:
            Assign8em.append('')
    if "Grid Specific" in Assign8em:
        AnnualTechnologyEmission['Classification'] = Assign8em
        AnnualTechnologyEmissionGrid = AnnualTechnologyEmission.loc[AnnualTechnologyEmission["Classification"] == "Grid Specific"]
        AnnualTechnologyEmissionGridplot = AnnualTechnologyEmissionGrid.pivot_table(AnnualTechnologyEmissionGrid,index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
        AnnualTechnologyEmissionGridplot = AnnualTechnologyEmissionGridplot.reset_index()
        AnnualTechnologyEmissionGridplot = AnnualTechnologyEmissionGridplot.droplevel(level=0, axis=1)
        list4 = AnnualTechnologyEmissionGridplot.columns.tolist()
        list4.remove('')
        figemgrid= px.bar(AnnualTechnologyEmissionGridplot, x='', y=list4)
        figemgrid.update_layout(
            title=("Accumulated New Capacity for Grid Specific Technologies"),
            title_x=0.45,
            xaxis_title="Year",
            paper_bgcolor='#FFFFFF',
            yaxis_title="Capaciy in kW",
            legend_title="Technologies",
            font=dict(
                family="Times New Roman",
                size=12,
                color="Black"
            )
        )

    # Capital Investment combined, source and sink

    # Capital Investment
    CapitalInvestment = pd.DataFrame(a['DiscountedCapitalInvestmentByTechnology'])
    CapitalInvestment = CapitalInvestment.loc[CapitalInvestment["TECHNOLOGY"] != "dhn"]
    CapitalInvestment = CapitalInvestment.loc[CapitalInvestment["VALUE"] > 0.001]
    Tech_listem = CapitalInvestment['TECHNOLOGY'].tolist()
    AssignCI1 = []
    AssignCIt1 = []
    AssignCI2= []
    AssignCI4= []              
    for x in Tech_listem:
        if("grid") in x:
            AssignCI1.append("Grid Specific")
            AssignCIt1.append("Grid Specific")
            AssignCI4.append('')
        elif ("dhn") in x:
            AssignCI1.append("District Heating Network")
            AssignCI4.append('')                           
        else:
            for j in names:
                i = int(j)
                if (','.join(["sou%dstr" % i ])) in x:
                    AssignCI1.append(names[j])
                elif (','.join(["sink%dstr" % i ])) in x:
                    AssignCI1.append(names[j])
            for i in sourcesinkidlistd:
                if (','.join(["sou%dstr" % i ])) in x:
                    AssignCIt1.append(','.join(["Source%d" % i ]))            
                elif (','.join(["sink%dstr" % i ])) in x:
                    AssignCIt1.append(','.join(["Sink%d" % i ]))
                elif x.endswith(','.join(["sou%d" % i ])) is True:
                    AssignCIt1.append('stream')
            if "sou" or "sink" in x:
                res = re.findall('(\d+|[A-Za-z]+)', str(x))
                for i in streamidlistd:
                        if len(res) > 1 and res[0] != 'str':
                            if(','.join(["%d" % i ])) == str(res[3]):
                                AssignCI4.append(','.join(["Stream%d" % i ]))
                        elif len(res) > 1 and res[0] == 'str':
                            if(','.join(["%d" % i ])) == str(res[1]):
                                AssignCI4.append(','.join(["Stream%d" % i ]))
            else:
                AssignCI4.append('')
            for i in streamidlistd:
                if(','.join(["str%dsou" % i ])) in x:
                    AssignCI1.append(','.join(["Stream%d" % i ])) 


        if ("gridspecificngboiler") in x:
            AssignCI2.append("Grid Specific Natural gas Boiler")
        elif ("gridspecificelboiler") in x:
            Assign2.append("Grid Specific Electric Boiler")
        elif ("gridspecificoilboiler") in x:
            AssignCI2.append("Grid Specific Oil Boiler")
        elif ("gridspecificbioboiler") in x:
            AssignCI2.append("Grid Specific Biomass Boiler")
        elif ("gridspecifichp") in x:
            AssignCI2.append("Grid Specific Heat Pump")
        elif ("gridspecificsthp") in x:
            AssignCI2.append("Grid Specific solar thermal with Heat Pump")
        elif ("dhn") in x:
            AssignCI2.append("District Heating Network")
        elif ("she") in x:
            AssignCI2.append("Single Heat Exchanger")      
        elif ("mhe") in x:
            AssignCI2.append("Multiple Heat Exchanger")
        elif ("elwhrb") in x:
            AssignCI2.append("Electric Waste Heat Recovery Boiler")
        elif ("ngwhrb") in x:
            AssignCI2.append("Natural Gas Heat Recovery Boiler")
        elif ("oilwhrb") in x:
            AssignCI2.append("Oil Heat Recovery Boiler")
        elif ("biowhrb") in x:
            AssignCI2.append("Biomass Heat Recovery Boiler")
        elif ("chpng") in x:
            AssignCI2.append("Natural Gas CHP")
        elif ("chpoil") in x:
            AssignCI2.append("Oil CHP")
        elif ("chpbio") in x:
            AssignCI2.append("Biomass CHP")
        elif ("boosthp") in x:
            AssignCI2.append("Booster Heat Pump")
        elif ("sthp") in x:
            AssignCI2.append("Solar thermal Heat Pump")
        elif ("stngboiler") in x:
            AssignCI2.append("Solar thermal with Natural gas boiler")
        elif ("stoilboiler") in x:
            AssignCI2.append("Solar thermal with oil boiler")
        elif ("stbioboiler") in x:
            AssignCI2.append("Solar thermal with biomass boiler")
        elif ("stelboiler") in x:
            AssignCI2.append("Solar thermal with el boiler")
        elif x.endswith('ac') is True:
            AssignCI2.append("Absorption Chiller")
        elif x.endswith('acec') is True:
            AssignCI2.append("Absorption Chiller with Electric Chiller")
        elif ("acngboiler") in x:
            AssignCI2.append("Absorption Chiller with Natural gas boiler")
        elif ("acoilboiler") in x:
            AssignCI2.append("Absorption Chiller with oil boiler")
        elif ("acbioboiler") in x:
            AssignCI2.append("Absorption Chiller with biomass boiler")
        elif ("acelectricboiler") in x:
            AssignCI2.append("Absorption Chiller with electric boiler")  
        elif ("acecngboiler") in x:
            AssignCI2.append("Absorption Chiller and Electric Chiller with Natural gas boiler")
        elif ("acecoilboiler") in x:
            AssignCI2.append("Absorption Chiller and Electric Chiller with oil boiler")
        elif ("acecbioboiler") in x:
            AssignCI2.append("Absorption Chiller and Electric Chiller with biomass boiler")
        elif ("acecelectricboiler") in x:
            AssignCI2.append("Absorption Chiller and Electric Chiller with electric boiler")
        elif ("acechp") in x:
            AssignCI2.append("Absorption Chiller and Electric Chiller with heat pump")
        elif ("achp") in x:
            AssignCI2.append("Absorption Chiller with heat pump")
        elif ("orc") in x:
            AssignCI2.append("Organic Rankine Cycle")
        elif ("exgrid") in x:
            AssignCI2.append("Existing Grid Technologies")
        elif("hp") in x:
            for i in streamidlistd:
                if(','.join(["str%dhp" % i ])) in x:
                    AssignCI2.append("Heat Pump") 
        else:
            AssignCI2.append(" ")

    AssignCI3= []

    for i in range(0, len(AssignCI1)):
        if AssignCI1[i] in AssignCI2[i]:
            AssignCI3.append(AssignCI2[i])
        elif AssignCI2[i] == '':
            AssignCI3.append(str(str(AssignCI1[i]) + str(AssignCI2[i])))
        else:
            AssignCI3.append(str(str(AssignCI1[i]) + ' ' + str(AssignCI4[i])+ ' ' + str(AssignCI2[i])))
    AssignCI3

    CapitalInvestment['Assignment'] = AssignCI3
    CapitalInvestment = CapitalInvestment.drop(['TECHNOLOGY'], axis = 1)
    CapitalInvestment = CapitalInvestment.drop(['NAME'], axis = 1)
    CapitalInvestment.rename(columns={"Assignment": "TECHNOLOGY"}, inplace=True)
    CapitalInvestment = CapitalInvestment [['VALUE', 'TECHNOLOGY']]

    CapitalInvestment = CapitalInvestment.loc[CapitalInvestment["VALUE"] != 0] 

    figCI = px.bar(CapitalInvestment,x='TECHNOLOGY', y= 'VALUE')
    figCI.update_layout(
        title="Total Capital Investment",
        title_x=0.45,
        xaxis_title="Technologies",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Capital Investment in €",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )

    # source wise Capital Investment graph creation

    CapitalInvestment["assignment"] = AssignCIt1
    Techlist = CapitalInvestment["assignment"].tolist()

    AssignCI4 = []
    for x in Techlist:
        if "Source" in x:
            AssignCI4.append("Source")
        else:
            AssignCI4.append('')
    CapitalInvestment['Classification'] = AssignCI4
    Classlist = CapitalInvestment["Classification"].tolist()
    Classlist
    CapitalInvestmentSource = CapitalInvestment.loc[CapitalInvestment["Classification"] == "Source"]
    del CapitalInvestmentSource['Classification']
    Techlist = CapitalInvestmentSource["TECHNOLOGY"].tolist()
    AssignCI5 = []

    for x in Techlist:
        for i in names:
                if str(str(names[str(i)])+ ' ') in x:
                    AssignCI5.append(names[str(i)])
    CapitalInvestmentSource['Classification'] = AssignCI5

    ciso = []   
    for i in names:
        if (names[str(i)]) in CapitalInvestmentSource['Classification'].unique():
            df = CapitalInvestmentSource.loc[CapitalInvestmentSource["Classification"] == (names[str(i)])]
            figsoCI = px.bar(df,x='TECHNOLOGY', y= 'VALUE')
            figsoCI.update_layout(
                title=(','.join(["Total Capital Investment for" + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Technologies",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Capital Investment in €",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )

            cisouel = plotly.io.to_html(figsoCI, full_html=False,include_plotlyjs=False)
            ciso.append(cisouel)    
    # Sink wise graphs
    CapitalInvestment["assignment"] = AssignCIt1
    Techlist = CapitalInvestment["assignment"].tolist()
    Assign6CIsi= []
    for x in Techlist:
        if "Sink" in x:
            Assign6CIsi.append("Sink")
        else:
            Assign6CIsi.append('')
    CapitalInvestment['Classification'] = Assign6CIsi
    CapitalInvestmentSink = CapitalInvestment.loc[CapitalInvestment["Classification"] == "Sink"]
    del CapitalInvestmentSink['Classification']
    Techlist = CapitalInvestmentSink["TECHNOLOGY"].tolist()

    Assign7CIsi= []

    for x in Techlist:
        for i in names:
                if str(str(names[str(i)])+ ' ') in x:
                    Assign7CIsi.append(names[str(i)])
    CapitalInvestmentSink['Classification'] = Assign7CIsi

    cisi = []

    for i in names:
        if (names[str(i)]) in CapitalInvestmentSink['Classification'] .unique():
            df = CapitalInvestmentSink.loc[CapitalInvestmentSink["Classification"] == (names[str(i)])]
            fig3siCI= px.bar(df, x='TECHNOLOGY', y= 'VALUE')
            fig3siCI.update_layout(
                title=(','.join(["Total Capital Investment for" + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Technologies",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Capital Investment in €",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            cisiuel = plotly.io.to_html(fig3siCI, full_html=False,include_plotlyjs=False)
            cisi.append(cisiuel) 

    # capital investment storage
    CapitalInvestmentsto = pd.DataFrame(a['DiscountedCapitalInvestmentByStorage'])
    if len(CapitalInvestmentsto) != 0:
        CapitalInvestmentsto = CapitalInvestmentsto.loc[CapitalInvestmentsto["VALUE"] != 0] 
        del CapitalInvestmentsto['NAME']

        figCIS = px.bar(CapitalInvestmentsto,x='STORAGE', y= 'VALUE')
        figCIS.update_layout(
            title="Total Capital Investment Storage",
            title_x=0.45,
            xaxis_title="Storage",
            paper_bgcolor='#FFFFFF',
            yaxis_title="Capital Investment Storage in €",
            legend_title="Storage",
            font=dict(
                family="Times New Roman",
                size=12,
                color="Black"
            )
        )
    else:
        figCIS = ''

    # Total Operating Cost - Combined, source and sink specific

    # Combined

    OperatingCost = pd.DataFrame(a['TotalDiscountedFixedOperatingCost'])
    OperatingCost = OperatingCost.loc[OperatingCost["VALUE"] >= 0.001] 
    OperatingCost = OperatingCost.loc[OperatingCost["TECHNOLOGY"] != "dhn"]

    Tech_listem = OperatingCost['TECHNOLOGY'].tolist()
    AssignOC1 = []
    AssignOC1t = []
    AssignOC2= []
    AssignOC4= []  
    for x in Tech_listem:
        if("grid") in x:
            AssignOC1.append("Grid Specific")
            AssignOC1t.append("Grid Specific")
            AssignOC4.append('')
        elif ("dhn") in x:
            AssignOC1.append("District Heating Network")
            AssignOC4.append('')
        else:
            for j in names:
                i = int(j)
                if (','.join(["sou%dstr" % i ])) in x:
                    AssignOC1.append(names[j])
                elif (','.join(["sink%dstr" % i ])) in x:
                    AssignOC1.append(names[j])
            for i in sourcesinkidlistd:
                    if (','.join(["sou%dstr" % i ])) in x:
                        AssignOC1t.append(','.join(["Source%d" % i ]))            
                    elif (','.join(["sink%dstr" % i ])) in x:
                        AssignOC1t.append(','.join(["Sink%d" % i ]))
                    elif x.endswith(','.join(["sou%d" % i ])) is True:
                        AssignOC1t.append('stream')
            if "sou" or "sink" in x:
                res = re.findall('(\d+|[A-Za-z]+)', str(x))
                for i in streamidlistd:
                        if len(res) > 1 and res[0] != 'str':
                            if(','.join(["%d" % i ])) == str(res[3]):
                                AssignOC4.append(','.join(["Stream%d" % i ]))
                        elif len(res) > 1 and res[0] == 'str':
                            if(','.join(["%d" % i ])) == str(res[1]):
                                AssignOC4.append(','.join(["Stream%d" % i ]))
            else:
                AssignOC4.append('')

            for i in streamidlistd:
                if(','.join(["str%dsou" % i ])) in x:
                    AssignOC1.append(','.join(["Stream%d" % i ])) 

        if ("gridspecificngboiler") in x:
            AssignOC2.append("Grid Specific Natural gas Boiler")
        elif ("gridspecificelboiler") in x:
            Assign2.append("Grid Specific Electric Boiler")
        elif ("gridspecificoilboiler") in x:
            AssignOC2.append("Grid Specific Oil Boiler")
        elif ("gridspecificbioboiler") in x:
            AssignOC2.append("Grid Specific Biomass Boiler")
        elif ("gridspecifichp") in x:
            AssignOC2.append("Grid Specific Heat Pump")
        elif ("gridspecificsthp") in x:
            AssignOC2.append("Grid Specific solar thermal with Heat Pump")
        elif ("dhn") in x:
            AssignOC2.append("District Heating Network")
        elif ("she") in x:
            AssignOC2.append("Single Heat Exchanger")      
        elif ("mhe") in x:
            AssignOC2.append("Multiple Heat Exchanger")
        elif ("elwhrb") in x:
            AssignOC2.append("Electric Waste Heat Recovery Boiler")
        elif ("ngwhrb") in x:
            AssignOC2.append("Natural Gas Heat Recovery Boiler")
        elif ("oilwhrb") in x:
            AssignOC2.append("Oil Heat Recovery Boiler")
        elif ("biowhrb") in x:
            AssignOC2.append("Biomass Heat Recovery Boiler")
        elif ("chpng") in x:
            AssignOC2.append("Natural Gas CHP")
        elif ("chpoil") in x:
            AssignOC2.append("Oil CHP")
        elif ("chpbio") in x:
            AssignOC2.append("Biomass CHP")
        elif ("boosthp") in x:
            AssignOC2.append("Booster Heat Pump")
        elif ("sthp") in x:
            AssignOC2.append("Solar thermal Heat Pump")
        elif ("stngboiler") in x:
            AssignOC2.append("Solar thermal with Natural gas boiler")
        elif ("stoilboiler") in x:
            AssignOC2.append("Solar thermal with oil boiler")
        elif ("stbioboiler") in x:
            AssignOC2.append("Solar thermal with biomass boiler")
        elif ("stelboiler") in x:
            AssignOC2.append("Solar thermal with el boiler")
        elif x.endswith('ac') is True:
            AssignOC2.append("Absorption Chiller")
        elif x.endswith('acec') is True:
            AssignOC2.append("Absorption Chiller with Electric Chiller")
        elif ("acngboiler") in x:
            AssignOC2.append("Absorption Chiller with Natural gas boiler")
        elif ("acoilboiler") in x:
            AssignOC2.append("Absorption Chiller with oil boiler")
        elif ("acbioboiler") in x:
            AssignOC2.append("Absorption Chiller with biomass boiler")
        elif ("acelectricboiler") in x:
            AssignOC2.append("Absorption Chiller with electric boiler")  
        elif ("acecngboiler") in x:
            AssignOC2.append("Absorption Chiller and Electric Chiller with Natural gas boiler")
        elif ("acecoilboiler") in x:
            AssignOC2.append("Absorption Chiller and Electric Chiller with oil boiler")
        elif ("acecbioboiler") in x:
            AssignOC2.append("Absorption Chiller and Electric Chiller with biomass boiler")
        elif ("acecelectricboiler") in x:
            AssignOC2.append("Absorption Chiller and Electric Chiller with electric boiler")
        elif ("acechp") in x:
            AssignOC2.append("Absorption Chiller and Electric Chiller with heat pump")
        elif ("achp") in x:
            AssignOC2.append("Absorption Chiller with heat pump")
        elif ("orc") in x:
            AssignOC2.append("Organic Rankine Cycle")
        elif ("exgrid") in x:
            AssignOC2.append("Existing Grid Technologies")
        elif("hp") in x:
            for i in streamidlistd:
                if(','.join(["str%dhp" % i ])) in x:
                    AssignOC2.append("Heat Pump") 
        else:
            AssignOC2.append(" ")

    AssignOC3= []

    for i in range(0, len(AssignOC1)):
        if AssignOC1[i] in AssignOC2[i]:
            AssignOC3.append(AssignOC2[i])
        elif AssignOC2[i] == '':
            AssignOC3.append(str(str(AssignOC1[i]) + str(AssignOC2[i])))
        else:
            AssignOC3.append(str(str(AssignOC1[i]) + ' ' + str(AssignOC4[i])+ ' ' + str(AssignOC2[i])))

    OperatingCost['Assignment'] = AssignOC3
    OperatingCost = OperatingCost.drop(['TECHNOLOGY'], axis = 1)
    OperatingCost = OperatingCost.drop(['NAME'], axis = 1)
    OperatingCost.rename(columns={"Assignment": "TECHNOLOGY"}, inplace=True)
    OperatingCost = OperatingCost [['VALUE', 'TECHNOLOGY']]

    figOC = px.bar(OperatingCost,x='TECHNOLOGY', y= 'VALUE')
    figOC.update_layout(
        title="Total Operating Cost",
        title_x=0.45,
        xaxis_title="Technologies",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Operating Cost in €",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )


    # source wise Operating Cost creation
    OperatingCost["assignment"] = AssignOC1t
    Techlist = OperatingCost["assignment"].tolist()
    AssignOC4 = []
    for x in Techlist:
        if "Source" in x:
            AssignOC4.append("Source")
        else:
            AssignOC4.append('')

    OperatingCost['Classification'] = AssignOC4
    Classlist = OperatingCost["Classification"].tolist()
    OperatingCostSource = OperatingCost.loc[OperatingCost["Classification"] == "Source"]
    del OperatingCostSource['Classification']
    Techlist = OperatingCostSource["TECHNOLOGY"].tolist()

    AssignOC5 = []

    for x in Techlist:
        for i in names:
            if str(str(names[str(i)])+ ' ') in x:
                AssignOC5.append(names[str(i)])
    OperatingCostSource['Classification'] = AssignOC5

    ocso = []   
    for i in names:
        if (names[str(i)]) in OperatingCostSource['Classification'].unique():
            df = OperatingCostSource.loc[OperatingCostSource["Classification"] == (names[str(i)])]
            figsoOC = px.bar(df,x='TECHNOLOGY', y= 'VALUE')
            figsoOC.update_layout(
                title=(','.join(["Total Operating Cost for" + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Technologies",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Operating Cost in €",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )

            ocsouel = plotly.io.to_html(figsoOC, full_html=False,include_plotlyjs=False)
            ocso.append(ocsouel)


    # Sink wise graphs
    OperatingCost["assignment"] = AssignOC1t
    Techlist = OperatingCost["assignment"].tolist()
    Assign6OCsi= []
    for x in Techlist:
        if "Sink" in x:
            Assign6OCsi.append("Sink")
        else:
            Assign6OCsi.append('')
    OperatingCost['Classification'] = Assign6OCsi
    OperatingCostSink = OperatingCost.loc[OperatingCost["Classification"] == "Sink"]
    del OperatingCostSink['Classification']
    Techlist = OperatingCostSink["TECHNOLOGY"].tolist()
    Assign7OCsi= []

    for x in Techlist:
        for i in names:
            if str(str(names[str(i)])+ ' ') in x:
                Assign7OCsi.append(names[str(i)])
    OperatingCostSink['Classification'] = Assign7OCsi

    ocsi = []
    for i in names:
        if (names[str(i)]) in OperatingCostSink['Classification'].unique():
            df = OperatingCostSink.loc[OperatingCostSink["Classification"] == (names[str(i)])]
            fig3siOC= px.bar(df, x='TECHNOLOGY', y= 'VALUE')
            fig3siOC.update_layout(
                title=(','.join(["Total OperatingCost for" + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Technologies",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Operating Costt in €",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )     
            ocsiuel = plotly.io.to_html(fig3siOC, full_html=False,include_plotlyjs=False)
            ocsi.append(ocsiuel)  


    #Storage level

    StorageLevel = pd.DataFrame(a['StorageLevelTimesliceStart'])
    if len(StorageLevel) != 0:
        StorageLevel = StorageLevel.loc[StorageLevel['YEAR'] == StorageLevel['YEAR'].max()]
        Stolist = StorageLevel['STORAGE'].tolist()
        del StorageLevel['YEAR']
        del StorageLevel['NAME']
        TSlist = StorageLevel['TIMESLICE'].tolist()
        TSlistint= []
        for i in TSlist:
            TSlistint.append(int(i))
        StorageLevel['TIMESLICEINT'] = TSlistint
        del StorageLevel['TIMESLICE']
        StorageLevel.rename(columns={"TIMESLICEINT": "TIMESLICE"}, inplace=True)
        StorageLevelsorted = StorageLevel.sort_values(by=['TIMESLICE'], ascending=True)
        StorageLevelsorted
        Stolistd =[]
        for i in Stolist:
            if i not in Stolistd:
                Stolistd.append(i)

        stol = []
        for i in Stolistd:
            StorageLevelplot = StorageLevelsorted.loc[StorageLevel['STORAGE'] == str(i)]
            figsl = px.area(StorageLevelplot, x='TIMESLICE', y='VALUE', color_discrete_sequence=px.colors.qualitative.Alphabet, markers=True)
            figsl.update_layout(
                title="Intra annual Storage level for {sto}".format(sto = i),
                title_x=0.45,
                xaxis_title="Timeslice",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Storage Level in kWh",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            stoluel = plotly.io.to_html(figsl, full_html=False,include_plotlyjs=False)
            stol.append(stoluel) 
        
    else:
        stol = []

    stocd = []
    if len(StorageLevel) != 0:
        for k in Stolistd:
            storageLevelplot = StorageLevelsorted.loc[StorageLevel['STORAGE'] == k]
            valuelist = storageLevelplot['VALUE'].tolist()
            differencelist = []
            for i in range(0, int(len(valuelist))):
                if i == 0:
                    differencelist.append(valuelist[i])
                else:
                    differencelist.append(valuelist[i] - valuelist[i-1])
            storageLevelplot['Charging_and_Discharging'] = differencelist
            del storageLevelplot['VALUE']
            figslcd = px.line(storageLevelplot, x='TIMESLICE', y='Charging_and_Discharging', color_discrete_sequence=px.colors.qualitative.Alphabet, markers=True)
            figslcd.update_layout(
                title="Intra annual Storage charge and discharge for {sto}".format(sto = k),
                title_x=0.45,
                xaxis_title="Timeslice",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Storage charge and discharge in kWh",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            stocduel = plotly.io.to_html(figslcd, full_html=False,include_plotlyjs=False)
            stocd.append(stocduel)  
    else:
        stocd = []

    #PBT
    productionbytechnology = pd.DataFrame(a['ProductionByTechnology'])
    productionbytechnology = productionbytechnology.loc[productionbytechnology['YEAR'] == productionbytechnology['YEAR'].max()]
    Tech_listPBT = productionbytechnology['TECHNOLOGY'].tolist()
    AssignPBT1 = []
    AssignPBT1t = []
    AssignPBT2= []
    AssignPBT4= []
    for x in Tech_listPBT:
        if("grid") in x:
            AssignPBT1.append("Grid Specific")
            AssignPBT1t.append("Grid Specific")
            AssignPBT4.append('')
        elif ("dhn") in x:
            AssignPBT1.append("District Heating Network")
            AssignPBT1t.append("District Heating Network")
            AssignPBT4.append('')                           
        else:
            for j in names:
                i = int(j)
                if (','.join(["sou%dstr" % i ])) in x:
                    AssignPBT1.append(names[j])
                elif (','.join(["sink%dstr" % i ])) in x:
                    AssignPBT1.append(names[j])
            for i in sourcesinkidlistd:
                    if (','.join(["sou%dstr" % i ])) in x:
                        AssignPBT1t.append(','.join(["Source%d" % i ]))            
                    elif (','.join(["sink%dstr" % i ])) in x:
                        AssignPBT1t.append(','.join(["Sink%d" % i ]))
                    elif x.endswith(','.join(["sou%d" % i ])) is True:
                        AssignPBT1t.append('stream')
            if "sou" or "sink" in x:
                res = re.findall('(\d+|[A-Za-z]+)', str(x))
                for i in streamidlistd:
                        if len(res) > 1 and res[0] != 'str':
                            if(','.join(["%d" % i ])) == str(res[3]):
                                AssignPBT4.append(','.join(["Stream%d" % i ]))
                        elif len(res) > 1 and res[0] == 'str':
                            if(','.join(["%d" % i ])) == str(res[1]):
                                AssignPBT4.append(','.join(["Stream%d" % i ]))
            else:
                AssignPBT4.append('')
                           
            for i in streamidlistd:
                if(','.join(["str%dsou" % i ])) in x:
                    AssignPBT1.append(','.join(["Stream%d" % i ])) 

        if ("gridspecificngboiler") in x:
            AssignPBT2.append("Grid Specific Natural gas Boiler")
        elif ("gridspecificelboiler") in x:
            Assign2.append("Grid Specific Electric Boiler")
        elif ("gridspecificoilboiler") in x:
            AssignPBT2.append("Grid Specific Oil Boiler")
        elif ("gridspecificbioboiler") in x:
            AssignPBT2.append("Grid Specific Biomass Boiler")
        elif ("gridspecifichp") in x:
            AssignPBT2.append("Grid Specific Heat Pump")
        elif ("gridspecificsthp") in x:
            AssignPBT2.append("Grid Specific solar thermal with Heat Pump")
        elif ("dhn") in x:
            AssignPBT2.append("District Heating Network")
        elif ("she") in x:
            AssignPBT2.append("Single Heat Exchanger")      
        elif ("mhe") in x:
            AssignPBT2.append("Multiple Heat Exchanger")
        elif ("elwhrb") in x:
            AssignPBT2.append("Electric Waste Heat Recovery Boiler")
        elif ("ngwhrb") in x:
            AssignPBT2.append("Natural Gas Heat Recovery Boiler")
        elif ("oilwhrb") in x:
            AssignPBT2.append("Oil Heat Recovery Boiler")
        elif ("biowhrb") in x:
            AssignPBT2.append("Biomass Heat Recovery Boiler")
        elif ("chpng") in x:
            AssignPBT2.append("Natural Gas CHP")
        elif ("chpoil") in x:
            AssignPBT2.append("Oil CHP")
        elif ("chpbio") in x:
            AssignPBT2.append("Biomass CHP")
        elif ("boosthp") in x:
            AssignPBT2.append("Booster Heat Pump")
        elif ("sthp") in x:
            AssignPBT2.append("Solar thermal Heat Pump")
        elif ("stngboiler") in x:
            AssignPBT2.append("Solar thermal with Natural gas boiler")
        elif ("stoilboiler") in x:
            AssignPBT2.append("Solar thermal with oil boiler")
        elif ("stbioboiler") in x:
            AssignPBT2.append("Solar thermal with biomass boiler")
        elif ("stelboiler") in x:
            AssignPBT2.append("Solar thermal with el boiler")
        elif x.endswith('ac') is True:
            AssignPBT2.append("Absorption Chiller")
        elif x.endswith('acec') is True:
            AssignPBT2.append("Absorption Chiller with Electric Chiller")
        elif ("acngboiler") in x:
            AssignPBT2.append("Absorption Chiller with Natural gas boiler")
        elif ("acoilboiler") in x:
            AssignPBT2.append("Absorption Chiller with oil boiler")
        elif ("acbioboiler") in x:
            AssignPBT2.append("Absorption Chiller with biomass boiler")
        elif ("acelectricboiler") in x:
            AssignPBT2.append("Absorption Chiller with electric boiler")  
        elif ("acecngboiler") in x:
            AssignPBT2.append("Absorption Chiller and Electric Chiller with Natural gas boiler")
        elif ("acecoilboiler") in x:
            AssignPBT2.append("Absorption Chiller and Electric Chiller with oil boiler")
        elif ("acecbioboiler") in x:
            AssignPBT2.append("Absorption Chiller and Electric Chiller with biomass boiler")
        elif ("acecelectricboiler") in x:
            AssignPBT2.append("Absorption Chiller and Electric Chiller with electric boiler")
        elif ("acechp") in x:
            AssignPBT2.append("Absorption Chiller and Electric Chiller with heat pump")
        elif ("achp") in x:
            AssignPBT2.append("Absorption Chiller with heat pump")
        elif ("orc") in x:
            AssignPBT2.append("Organic Rankine Cycle")
        elif ("exgrid") in x:
            AssignPBT2.append("Existing Grid Technologies")
        elif("hp") in x:
            for i in streamidlistd:
                if(','.join(["str%dhp" % i ])) in x:
                    AssignPBT2.append("Heat Pump") 
        else:
            AssignPBT2.append(" ")

    AssignPBT3= []

    for i in range(0, len(AssignPBT1)):
        if AssignPBT1[i] in AssignPBT2[i]:
            AssignPBT3.append(AssignPBT2[i])
        elif AssignPBT2[i] == '':
            AssignPBT3.append(str(str(AssignPBT1[i]) + str(AssignPBT2[i])))
        else:
            AssignPBT3.append(str(str(AssignPBT1[i]) + ' ' + str(AssignPBT4[i])+ ' ' + str(AssignPBT2[i])))
    
    productionbytechnology['Assignment'] = AssignPBT3
    productionbytechnology = productionbytechnology.drop(['TECHNOLOGY'], axis = 1)
    productionbytechnology = productionbytechnology.drop(['NAME'], axis = 1)
    productionbytechnology.rename(columns={"Assignment": "TECHNOLOGY"}, inplace=True)
    productionbytechnology = productionbytechnology [['VALUE', 'TECHNOLOGY', 'TIMESLICE']]
    productionbytechnology['Assignment'] = AssignPBT1t
    #Aggregated Source side PBT

    productionbytechnologysource = productionbytechnology
    Techlist4PBTsource = productionbytechnologysource["Assignment"].tolist()
    Assign4PBT = []
    for x in Techlist4PBTsource:
        if "Source" in x:
            Assign4PBT.append("Source")
        else:
            Assign4PBT.append('')

    productionbytechnologysource['Classification'] = Assign4PBT
    productionbytechnologysource = productionbytechnologysource.loc[productionbytechnologysource["Classification"] == "Source"]
    TSlistPBTsource = productionbytechnologysource['TIMESLICE'].tolist()
    TSlistPBTsourceint= []
    for i in TSlistPBTsource:
        TSlistPBTsourceint.append(int(i))
    productionbytechnologysource['TIMESLICEINT'] = TSlistPBTsourceint
    del productionbytechnologysource['TIMESLICE']
    productionbytechnologysource.rename(columns={"TIMESLICEINT": "TIMESLICE"}, inplace=True)
    productionbytechnologysource = productionbytechnologysource.sort_values(by=['TIMESLICE'], ascending=True)
    del productionbytechnologysource['Classification']
    del productionbytechnologysource['Assignment']
    productionbytechnologysourceplot = productionbytechnologysource.pivot_table(productionbytechnologysource,index=['TIMESLICE'],columns=['TECHNOLOGY'],aggfunc=np.sum)
    productionbytechnologysourceplot = productionbytechnologysourceplot.reset_index()
    productionbytechnologysourceplot = productionbytechnologysourceplot.droplevel(level=0, axis=1)
    productionbytechnologysourceplot
    list4PBTplotsource = productionbytechnologysourceplot.columns.tolist()
    list4PBTplotsource.remove('')
    figsPBTsource = px.area(productionbytechnologysourceplot, x='', y=list4PBTplotsource, color_discrete_sequence=px.colors.qualitative.Alphabet, markers=True)
    figsPBTsource.update_layout(
        title="Intra annual heat generation for sources",
        title_x=0.45,
        xaxis_title="Timeslice",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Production in kWh",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )
    #Aggregated Sink side PBT

    productionbytechnologySink = productionbytechnology
    Techlist4PBTSink = productionbytechnologySink["Assignment"].tolist()
    Assign4PBTsink = []
    for x in Techlist4PBTSink:
        if "Sink" in x:
            Assign4PBTsink.append("Sink")
        else:
            Assign4PBTsink.append('')

    productionbytechnologySink['Classification'] = Assign4PBTsink
    productionbytechnologySink = productionbytechnologySink.loc[productionbytechnologySink["Classification"] == "Sink"]
    TSlistPBTSink = productionbytechnologySink['TIMESLICE'].tolist()
    TSlistPBTSinkint= []
    for i in TSlistPBTSink:
        TSlistPBTSinkint.append(int(i))
    productionbytechnologySink['TIMESLICEINT'] = TSlistPBTSinkint
    del productionbytechnologySink['TIMESLICE']
    productionbytechnologySink.rename(columns={"TIMESLICEINT": "TIMESLICE"}, inplace=True)
    productionbytechnologySink = productionbytechnologySink.sort_values(by=['TIMESLICE'], ascending=True)
    del productionbytechnologySink['Classification']
    del productionbytechnologySink['Assignment']
    productionbytechnologySinkplot = productionbytechnologySink.pivot_table(productionbytechnologySink,index=['TIMESLICE'],columns=['TECHNOLOGY'],aggfunc=np.sum)
    productionbytechnologySinkplot = productionbytechnologySinkplot.reset_index()
    productionbytechnologySinkplot = productionbytechnologySinkplot.droplevel(level=0, axis=1)
    productionbytechnologySinkplot
    list4PBTplotSink = productionbytechnologySinkplot.columns.tolist()
    list4PBTplotSink.remove('')
    figsPBTSink = px.area(productionbytechnologySinkplot, x='', y=list4PBTplotSink, color_discrete_sequence=px.colors.qualitative.Alphabet, markers=True)
    figsPBTSink.update_layout(
        title="Intra heat or cold consumption for Sinks",
        title_x=0.45,
        xaxis_title="Timeslice",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Production in kWh",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )

    #Each Source PBT

    TechlistPBTsourceclass = productionbytechnologysource["TECHNOLOGY"].tolist()
    sourcelistPBT = []
    for x in TechlistPBTsourceclass:
        for i in names:
                if str(str(names[str(i)])+ ' ') in x:
                    sourcelistPBT.append(names[str(i)])

    productionbytechnologysource['Classification'] = sourcelistPBT

    TSlistPBTeachsource = productionbytechnologysource['TIMESLICE'].tolist()
    TSlistPBTeachsourceint= []
    for i in TSlistPBTeachsource:
        TSlistPBTeachsourceint.append(int(i))

    productionbytechnologysource['TIMESLICEINT'] = TSlistPBTeachsourceint
    del productionbytechnologysource['TIMESLICE']
    productionbytechnologysource.rename(columns={"TIMESLICEINT": "TIMESLICE"}, inplace=True)
    productionbytechnologysourcesorted = productionbytechnologysource.sort_values(by=['TIMESLICE'], ascending=True)
    productionbytechnologysourcesorted
    sourcelistPBTd = []

    for i in sourcelistPBT:
        if i not in sourcelistPBTd:
            sourcelistPBTd.append(i)

    pbtso = []

    for i in names:
        if (names[str(i)]) in productionbytechnologysourcesorted['Classification'].unique():
            productionbytechnologysourcesorted1 = productionbytechnologysourcesorted.loc[productionbytechnologysourcesorted["Classification"] == (names[str(i)])]
            productionbytechnologysourcesortedplot = productionbytechnologysourcesorted1.pivot_table(productionbytechnologysourcesorted1,index=['TIMESLICE'],columns=['TECHNOLOGY'],aggfunc=np.sum)

            productionbytechnologysourcesortedplot = productionbytechnologysourcesorted1.pivot_table(productionbytechnologysourcesorted1,index=['TIMESLICE'],columns=['TECHNOLOGY'],aggfunc=np.sum)
            productionbytechnologysourcesortedplot = productionbytechnologysourcesortedplot.reset_index()
            productionbytechnologysourcesortedplot = productionbytechnologysourcesortedplot.droplevel(level=0, axis=1)
            listPBTeachsource = productionbytechnologysourcesortedplot.columns.tolist()
            listPBTeachsource.remove('')
            figsPBTeachsource = px.area(productionbytechnologysourcesortedplot, x='', y=listPBTeachsource, color_discrete_sequence=px.colors.qualitative.Alphabet, markers=True)
            figsPBTeachsource.update_layout(
                title=(','.join(["Intra annual heat generation for"  + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Timeslice",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Production in kWh",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            pbtsoel = plotly.io.to_html(figsPBTeachsource, full_html=False,include_plotlyjs=False)
            pbtso.append(pbtsoel)  

    #Each Sink PBT

    TechlistPBTSinkclass = productionbytechnologySink["TECHNOLOGY"].tolist()
    SinklistPBT = []
    for x in TechlistPBTSinkclass:
        for i in names:
                if str(str(names[str(i)])+ ' ') in x:
                    SinklistPBT.append(names[str(i)])

    productionbytechnologySink['Classification'] = SinklistPBT

    TSlistPBTeachSink = productionbytechnologySink['TIMESLICE'].tolist()
    TSlistPBTeachSinkint= []
    for i in TSlistPBTeachSink:
        TSlistPBTeachSinkint.append(int(i))

    productionbytechnologySink['TIMESLICEINT'] = TSlistPBTeachSinkint
    del productionbytechnologySink['TIMESLICE']
    productionbytechnologySink.rename(columns={"TIMESLICEINT": "TIMESLICE"}, inplace=True)
    productionbytechnologySinksorted = productionbytechnologySink.sort_values(by=['TIMESLICE'], ascending=True)
    productionbytechnologySinksorted
    SinklistPBTd = []

    for i in SinklistPBT:
        if i not in SinklistPBTd:
            SinklistPBTd.append(i)

    pbtsin = []

    for i in names:
        if (names[str(i)]) in productionbytechnologySinksorted['Classification'].unique():
            productionbytechnologySinksortedclassified = productionbytechnologySinksorted.loc[productionbytechnologySinksorted["Classification"] == (names[str(i)])]
            productionbytechnologySinksortedplot = productionbytechnologySinksortedclassified.pivot_table(productionbytechnologySinksortedclassified,index=['TIMESLICE'],columns=['TECHNOLOGY'],aggfunc=np.sum)
            productionbytechnologySinksortedplot = productionbytechnologySinksortedplot.reset_index()
            productionbytechnologySinksortedplot = productionbytechnologySinksortedplot.droplevel(level=0, axis=1)
            listPBTeachSink = productionbytechnologySinksortedplot.columns.tolist()
            listPBTeachSink.remove('')
            figsPBTeachSink = px.area(productionbytechnologySinksortedplot, x='', y=listPBTeachSink, color_discrete_sequence=px.colors.qualitative.Alphabet, markers=True)
            figsPBTeachSink.update_layout(
                title=(','.join(["Intra annual heat generation for"  + ' ' + str((names[str(i)]))])),
                title_x=0.45,
                xaxis_title="Timeslice",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Production in kWh",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            pbtsiel = plotly.io.to_html(figsPBTeachSink, full_html=False,include_plotlyjs=False)
            pbtsin.append(pbtsiel)  

    #Intial setup for production annual
    productionannualt = pd.DataFrame(a['ProductionByTechnology'])
    productionannual = productionannualt.pivot_table(values=['VALUE'], index=['YEAR'],columns=['TECHNOLOGY'],aggfunc=np.sum)
    productionannual = productionannual.reset_index()
    productionannual = productionannual.droplevel(level=0, axis=1)

    Tech_listPA = []
    Tech_listPA = productionannual.columns.tolist()
    Tech_listPA.remove('')
    Tech_listPA
    AssignPA1 = []
    AssignPA1t = []
    AssignPA2= []
    AssignPA4 = []
    
    
    for x in Tech_listPA:
        if("grid") in x:
            AssignPA1.append("Grid Specific")
            AssignPA4.append('')
            AssignPA1t.append("Grid Specific")
        elif ("dhn") in x:
            AssignPA1.append("District Heating Network")
            AssignPA1t.append("District Heating Network")
            AssignPA4.append('')
        else:
            for j in names:
                i = int(j)
                if (','.join(["sou%dstr" % i ])) in x:
                    AssignPA1.append(names[j])
                elif (','.join(["sink%dstr" % i ])) in x:
                    AssignPA1.append(names[j])
            for i in sourcesinkidlistd:
                if (','.join(["sou%dstr" % i ])) in x:
                    AssignPA1t.append(','.join(["Source%d" % i ]))            
                elif (','.join(["sink%dstr" % i ])) in x:
                    AssignPA1t.append(','.join(["Sink%d" % i ]))
                elif x.endswith(','.join(["sou%d" % i ])) is True:
                    AssignPA1t.append('stream')
            if "sou" or "sink" in x:
                res = re.findall('(\d+|[A-Za-z]+)', str(x))
                for i in streamidlistd:
                        if len(res) > 1 and res[0] != 'str':
                            if(','.join(["%d" % i ])) == str(res[3]):
                                AssignPA4.append(','.join(["Stream%d" % i ]))
                        elif len(res) > 1 and res[0] == 'str':
                            if(','.join(["%d" % i ])) == str(res[1]):
                                AssignPA4.append(','.join(["Stream%d" % i ]))
            else:
                AssignPA4.append('')
            for i in streamidlistd:
                if(','.join(["str%dsou" % i])) in x:
                    AssignPA1.append(','.join(["SourceStream%d" % i]))               

        if ("gridspecificngboiler") in x:
            AssignPA2.append("Grid Specific Natural gas Boiler")
        elif ("gridspecificelboiler") in x:
            Assign2.append("Grid Specific Electric Boiler")
        elif ("gridspecificoilboiler") in x:
            AssignPA2.append("Grid Specific Oil Boiler")
        elif ("gridspecificbioboiler") in x:
            AssignPA2.append("Grid Specific Biomass Boiler")
        elif ("gridspecifichp") in x:
            AssignPA2.append("Grid Specific Heat Pump")
        elif ("gridspecificsthp") in x:
            AssignPA2.append("Grid Specific solar thermal with Heat Pump")
        elif ("dhn") in x:
            AssignPA2.append("District Heating Network")
        elif ("she") in x:
            AssignPA2.append("Single Heat Exchanger")      
        elif ("mhe") in x:
            AssignPA2.append("Multiple Heat Exchanger")
        elif ("elwhrb") in x:
            AssignPA2.append("Electric Waste Heat Recovery Boiler")
        elif ("ngwhrb") in x:
            AssignPA2.append("Natural Gas Heat Recovery Boiler")
        elif ("oilwhrb") in x:
            AssignPA2.append("Oil Heat Recovery Boiler")
        elif ("biowhrb") in x:
            AssignPA2.append("Biomass Heat Recovery Boiler")
        elif ("chpng") in x:
            AssignPA2.append("Natural Gas CHP")
        elif ("chpoil") in x:
            AssignPA2.append("Oil CHP")
        elif ("chpbio") in x:
            AssignPA2.append("Biomass CHP")
        elif ("boosthp") in x:
            AssignPA2.append("Booster Heat Pump")
        elif ("sthp") in x:
            AssignPA2.append("Solar thermal Heat Pump")
        elif ("stngboiler") in x:
            AssignPA2.append("Solar thermal with Natural gas boiler")
        elif ("stoilboiler") in x:
            AssignPA2.append("Solar thermal with oil boiler")
        elif ("stbioboiler") in x:
            AssignPA2.append("Solar thermal with biomass boiler")
        elif ("stelboiler") in x:
            AssignPA2.append("Solar thermal with el boiler")
        elif x.endswith('ac') is True:
            AssignPA2.append("Absorption Chiller")
        elif x.endswith('acec') is True:
            AssignPA2.append("Absorption Chiller with Electric Chiller")
        elif ("acngboiler") in x:
            AssignPA2.append("Absorption Chiller with Natural gas boiler")
        elif ("acoilboiler") in x:
            AssignPA2.append("Absorption Chiller with oil boiler")
        elif ("acbioboiler") in x:
            AssignPA2.append("Absorption Chiller with biomass boiler")
        elif ("acelectricboiler") in x:
            AssignPA2.append("Absorption Chiller with electric boiler")  
        elif ("acecngboiler") in x:
            AssignPA2.append("Absorption Chiller and Electric Chiller with Natural gas boiler")
        elif ("acecoilboiler") in x:
            AssignPA2.append("Absorption Chiller and Electric Chiller with oil boiler")
        elif ("acecbioboiler") in x:
            AssignPA2.append("Absorption Chiller and Electric Chiller with biomass boiler")
        elif ("acecelectricboiler") in x:
            AssignPA2.append("Absorption Chiller and Electric Chiller with electric boiler")
        elif ("acechp") in x:
            AssignPA2.append("Absorption Chiller and Electric Chiller with heat pump")
        elif ("achp") in x:
            AssignPA2.append("Absorption Chiller with heat pump")
        elif ("orc") in x:
            AssignPA2.append("Organic Rankine Cycle")
        elif ("exgrid") in x:
            AssignPA2.append("Existing Grid Technologies")
        elif("hp") in x:
            for i in streamidlistd:
                if(','.join(["str%dhp" % i ])) in x:
                    AssignPA2.append("Heat Pump") 
        else:
            AssignPA2.append(" ")
    AssignPA3= ['']

    for i in range(0, len(AssignPA1)):
        if AssignPA1[i] in AssignPA2[i]:
            AssignPA3.append(AssignPA2[i])
        elif AssignPA2[i] == ' ':
            AssignPA3.append(str(str(AssignPA1[i]) + str(AssignPA2[i])))
        else:
            AssignPA3.append(str(str(AssignPA1[i]) + ' ' + str(AssignPA4[i])+ ' '+ str(AssignPA2[i])))


    productionannual.columns = AssignPA3


    #Production annual source aggregated
    
    newsourcelist = []
    for i in AssignPA1t:
        if 'Source' in i:
            newsourcelist.append(i)
    sourcenamelist = []
    for j in newsourcelist:
        for i in names:
            if i in j:
                sourcenamelist.append(str(names[i]))
    finalsourcenamelist = ['']

    for j in sourcenamelist:
        for i in AssignPA3:
            if j in i:
                finalsourcenamelist.append(i)
    finalsourcenamelist
    finalsourcenamelistd = []

    for i in finalsourcenamelist:
        if i not in finalsourcenamelistd:
            finalsourcenamelistd.append(i)
    productionannualsourceplot = productionannual[finalsourcenamelistd]


    list4PAplotsource = productionannualsourceplot.columns.tolist()
    list4PAplotsource.remove('')
    figsPAsource = px.bar(productionannualsourceplot, x ='', y=list4PAplotsource)
    figsPAsource.update_layout(
        title="Annual heat generation for sources",
        title_x=0.45,
        xaxis_title="Year",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Production in kWh",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )

    #Production annual sink aggregated

    newsinklist = []
    for i in AssignPA1t:
        if 'Sink' in i:
            newsinklist.append(i)
    sinknamelist = []
    for j in newsinklist:
        for i in names:
            if i in j:
                sinknamelist.append(str(names[i]))
    finalsinknamelist = ['']

    for j in sinknamelist:
        for i in AssignPA3:
            if j in i:
                finalsinknamelist.append(i)
    finalsinknamelist
    finalsinknamelistd = []

    for i in finalsinknamelist:
        if i not in finalsinknamelistd:
            finalsinknamelistd.append(i)
    productionannualsinkplot = productionannual[finalsinknamelistd]
    
    list4PAplotsink = productionannualsinkplot.columns.tolist()
    list4PAplotsink.remove('')
    figsPAsink = px.bar(productionannualsinkplot, x='', y=list4PAplotsink)
    figsPAsink.update_layout(
        title="Annual heat or cold consumption for sinks",
        title_x=0.45,
        xaxis_title="Timeslice",
        paper_bgcolor='#FFFFFF',
        yaxis_title="Production in kWh",
        legend_title="Technologies",
        font=dict(
            family="Times New Roman",
            size=12,
            color="Black"
        )
    )

    #Production annual each source

    pagso = []

    for i in names:
        eachsouPAlist = ['']
        for x in list4PAplotsource:
            if str(str(names[str(i)])+ ' ') in x:
                eachsouPAlist.append(x)  
        if len(eachsouPAlist) > 1:
            productionannualeachsourceplot = productionannualsourceplot[eachsouPAlist]
            listPAeachsource = productionannualeachsourceplot.columns.tolist()
            listPAeachsource.remove('')
            figsPAeachsource = px.bar(productionannualeachsourceplot, x='', y=listPAeachsource)
            figsPAeachsource.update_layout(
                title=(','.join(["Annual heat generation for" + ' ' + str(names[i])])),
                title_x=0.45,
                xaxis_title="Year",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Production in kWh",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            pasoel = plotly.io.to_html(figsPAeachsource, full_html=False,include_plotlyjs=False)
            pagso.append(pasoel)


    #Production annual each sink

    pagsi = []

    for i in names:
        eachsinkPAlist = ['']
        for x in list4PAplotsink:
            if str(str(names[str(i)])+ ' ') in x:
                eachsinkPAlist.append(x)  
        if len(eachsinkPAlist) > 1:
            productionannualeachsinkplot = productionannualsinkplot[eachsinkPAlist]
            listPAeachSink = productionannualeachsinkplot.columns.tolist()
            listPAeachSink.remove('')
            figsPAeachSink = px.bar(productionannualsinkplot, x='', y=listPAeachSink)
            figsPAeachSink.update_layout(
                title=(','.join(["Annual heat generation for" + ' ' + str(names[i])])),
                title_x=0.45,
                xaxis_title="Year",
                paper_bgcolor='#FFFFFF',
                yaxis_title="Production in kWh",
                legend_title="Technologies",
                font=dict(
                    family="Times New Roman",
                    size=12,
                    color="Black"
                )
            )
            pasiel = plotly.io.to_html(figsPAeachSink, full_html=False,include_plotlyjs=False)
            pagsi.append(pasiel)

    #Pie charts
    #SOurce Pie

    productionannualpie = productionannualt.pivot_table(values=['VALUE'], index=['TECHNOLOGY'],aggfunc=np.sum)
    techlist = productionannualpie.index.tolist()

    productionannualpie['Tech'] = techlist
    productionannualpie = productionannualpie.reset_index()
    productionannualpie.drop('Tech', inplace=True, axis=1)
    techlist = productionannualpie['TECHNOLOGY'].tolist()
    classlist = []
    for x in techlist:
        if 'sink' in x:
            classlist.append('Sink')
        elif 'sou' in x:
            classlist.append('Source')
        else:
            classlist.append(' ')
    productionannualpie['Class'] = classlist
    productionannualpie

    productionannualsourcepie = productionannualpie.loc[productionannualpie['Class'] == 'Source']
    productionannualsourcepie

    sourcelist1 = productionannualsourcepie['TECHNOLOGY'].tolist()
    Assignpiesou = []
    for x in sourcelist1:
        for i in sourcesinkidlistd:
                if (','.join(["sou%dstr" % i ])) in x:
                    Assignpiesou.append(','.join(["Source%d" % i ]))
                elif x.endswith(','.join(["sou%d" % i ])) is True:
                    Assignpiesou.append('stream')
    productionannualsourcepie['source'] = Assignpiesou
    productionannualsourcepie = productionannualsourcepie.loc[productionannualsourcepie['source'] != 'stream']
    productionannualsourcepie = productionannualsourcepie.pivot_table(productionannualsourcepie,columns=['source'],aggfunc=np.sum)

    piecollistsource = productionannualsourcepie.columns.tolist()
    pievallistsource = productionannualsourcepie.values.tolist()
    pievalflatlistsource = []
    for sublist in pievallistsource:
        for item in sublist:
            pievalflatlistsource.append(item)
    productionannualsourcepieplot = pd.DataFrame()
    productionannualsourcepieplot['Total Production'] =  pievalflatlistsource
    productionannualsourcepieplot['Sources'] =  piecollistsource
    pienamelist = []
    for x in productionannualsourcepieplot['Sources']:
        for j in names:
            i = int(j)
            if (','.join(["Source%d " % i ])) == str(str(x) + ' '):
                pienamelist.append(names[j])
    productionannualsourcepieplot['Sourcesnew'] = pienamelist
    del productionannualsourcepieplot['Sources']
    productionannualsourcepieplot.rename(columns={"Sourcesnew": "Sources"}, inplace=True)
    productionannualsourcepieplot.rename(columns={"Sourcesnew": "Sources"}, inplace=True)
    figpiesource = px.pie(productionannualsourcepieplot, values='Total Production', names='Sources', title='Share of excess heat generation')

    productionannualsinkpie = productionannualpie.loc[productionannualpie['Class'] == 'Sink']
    sinklist1 = productionannualsinkpie['TECHNOLOGY'].tolist()
    Assignpiesink = []
    for x in sinklist1:
        for i in sourcesinkidlistd:
                if (','.join(["sink%dstr" % i ])) in x:
                    Assignpiesink.append(','.join(["Sink%d" % i ]))
    productionannualsinkpie['sink'] = Assignpiesink
    productionannualsinkpie = productionannualsinkpie.pivot_table(productionannualsinkpie,columns=['sink'],aggfunc=np.sum)

    piecollistsink = productionannualsinkpie.columns.tolist()
    pievallistsink = productionannualsinkpie.values.tolist()
    pievalflatlistsink = []
    for sublist in pievallistsink:
        for item in sublist:
            pievalflatlistsink.append(item)
    productionannualsinkpieplot = pd.DataFrame()
    productionannualsinkpieplot['Total Production'] =  pievalflatlistsink
    productionannualsinkpieplot['Sinks'] =  piecollistsink
    pienamelist = []
    for x in productionannualsinkpieplot['Sinks']:
        for j in names:
            i = int(j)
            if (','.join(["Sink%d " % i ])) == str(str(x) + ' '):
                pienamelist.append(names[j])
    productionannualsinkpieplot['Sinksnew'] = pienamelist
    del productionannualsinkpieplot['Sinks']
    productionannualsinkpieplot.rename(columns={"Sinksnew": "Sinks"}, inplace=True)
    figpiesink = px.pie(productionannualsinkpieplot, values='Total Production', names='Sinks', title='Share of excess heat consumption')
    
        # Accumulated new capacity table

    AccumulatedNewCapacitydf = AccumulatedNewCapacityplot.loc[AccumulatedNewCapacityplot[''] == AccumulatedNewCapacityplot[''].max()]
    del AccumulatedNewCapacitydf['']
    AccumulatedNewCapacitydf = AccumulatedNewCapacitydf.rename(index={0: 'Installed capacity (kW)'})
    AccumulatedNewCapacitydf = AccumulatedNewCapacitydf.transpose()
    AccumulatedNewCapacitydf = AccumulatedNewCapacitydf.round(decimals=2)
    AccumulatedNewCapacitydf.reset_index(inplace=True)
    AccumulatedNewCapacitydf1 = AccumulatedNewCapacitydf.to_html(index=False, col_space= 100, justify='center')
    AccumulatedNewCapacitytable = AccumulatedNewCapacitydf1.replace('<tr>', '<tr align="center">')

    # Annual Emissions table

    AnnualTechnologyEmissiondf = AnnualTechnologyEmission.pivot_table(AnnualTechnologyEmission,columns=['TECHNOLOGY'],aggfunc=np.sum)
    AnnualTechnologyEmissiondf.reset_index(drop=True, inplace=True)
    AnnualTechnologyEmissiondf = AnnualTechnologyEmissiondf.rename_axis(None, axis=1)
    AnnualTechnologyEmissiondf = AnnualTechnologyEmissiondf.round(decimals=2)
    AnnualTechnologyEmissiondf = AnnualTechnologyEmissiondf.transpose()
    AnnualTechnologyEmissiondf.reset_index(inplace=True)
    AnnualTechnologyEmissiondf.rename(columns={'index': 'Technology',0: 'Emissions (kg CO2)'}, inplace=True)
    AnnualTechnologyEmissiondf1 = AnnualTechnologyEmissiondf.to_html(index=False, col_space= 100, justify='center')
    AnnualTechnologyEmissiondtable = AnnualTechnologyEmissiondf1.replace('<tr>', '<tr align="center">')
    

    # Accumulated new Storage capacity table
    if len(AccumulatedNewStorageCapacity) != 0:
        AccumulatedNewStorageCapacitydf  = AccumulatedNewStorageCapacityplot.loc[AccumulatedNewStorageCapacityplot[''] == AccumulatedNewStorageCapacityplot[''].max()]
        del AccumulatedNewStorageCapacitydf['']
        AccumulatedNewStorageCapacitydf.reset_index(drop=True)
        AccumulatedNewStorageCapacitydf.reset_index(drop=True, inplace=True)
        AccumulatedNewStorageCapacitydf = AccumulatedNewStorageCapacitydf.rename_axis(None, axis=1)
        AccumulatedNewStorageCapacitydf = AccumulatedNewStorageCapacitydf.round(decimals=2)
        AccumulatedNewStorageCapacitydf = AccumulatedNewStorageCapacitydf.transpose()
        AccumulatedNewStorageCapacitydf.reset_index(inplace=True)
        AccumulatedNewStorageCapacitydf.rename(columns={'index': 'Storage',0: 'Installed storage capacity (kWh)'}, inplace=True)
        AccumulatedNewStorageCapacitydf1 = AccumulatedNewStorageCapacitydf.to_html(index=False, col_space= 100, justify='center')
        AccumulatedNewStorageCapacitytable = AccumulatedNewStorageCapacitydf1.replace('<tr>', '<tr align="center">')

    else:
        AccumulatedNewStorageCapacitytable = ''

    # Capital costs table
    # del CapitalInvestment['Classification']
    CapitalInvestmenttable1 = CapitalInvestment.pivot_table(CapitalInvestment,columns=['TECHNOLOGY'],aggfunc=np.sum)
    CapitalInvestmenttable1.reset_index(drop=True)
    CapitalInvestmenttable1.reset_index(drop=True, inplace=True)
    CapitalInvestmenttable1 = CapitalInvestmenttable1.rename_axis(None, axis=1)
    CapitalInvestmenttable1 = CapitalInvestmenttable1.round(decimals=2)
    CapitalInvestmenttable1 = CapitalInvestmenttable1.transpose()
    CapitalInvestmenttable1.reset_index(inplace=True)
    CapitalInvestmenttable1.rename(columns={'index': 'Technology',0: 'Capital costs (Euros)'}, inplace=True)
    CapitalInvestmenttabledf1 =  CapitalInvestmenttable1.to_html(index=False, col_space= 100, justify='center')
    CapitalInvestmenttable = CapitalInvestmenttabledf1.replace('<tr>', '<tr align="center">')

    # Operating costs table
    #del OperatingCost['Classification']
    OperatingCostTable1 = OperatingCost.pivot_table(OperatingCost,columns=['TECHNOLOGY'],aggfunc=np.sum)
    OperatingCostTable1.reset_index(drop=True)
    OperatingCostTable1.reset_index(drop=True, inplace=True)
    OperatingCostTable1 = OperatingCostTable1.rename_axis(None, axis=1)
    OperatingCostTable1 = OperatingCostTable1.round(decimals=2)
    OperatingCostTable1 = OperatingCostTable1.transpose()
    OperatingCostTable1.reset_index(inplace=True)
    OperatingCostTable1.rename(columns={'index': 'Technology',0: 'Operating costs (Euros)'}, inplace=True)
    OperatingCostTabledf1 =  OperatingCostTable1.to_html(index=False, col_space= 100, justify='center')
    OperatingCosttable = OperatingCostTabledf1.replace('<tr>', '<tr align="center">')

    # Capital costs storage table
    if len(CapitalInvestmentsto) != 0:
        CapitalInvestmentsto1 = CapitalInvestmentsto.pivot_table(CapitalInvestmentsto,columns=['STORAGE'],aggfunc=np.sum)
        CapitalInvestmentsto1.reset_index(drop=True)
        CapitalInvestmentsto1.reset_index(drop=True, inplace=True)
        CapitalInvestmentsto1 = CapitalInvestmentsto1.rename_axis(None, axis=1)
        CapitalInvestmentsto1 = CapitalInvestmentsto1.round(decimals=2)
        CapitalInvestmentsto1 = CapitalInvestmentsto1.transpose()
        CapitalInvestmentsto1.reset_index(inplace=True)
        CapitalInvestmentsto1.rename(columns={'index': 'Storage',0: 'Capital costs (Euros)'}, inplace=True)
        CapitalInvestmentstodf1 =  CapitalInvestmentsto1.to_html(index=False, col_space= 100, justify='center')
        CapitalInvestmentstotable = CapitalInvestmentstodf1.replace('<tr>', '<tr align="center">')
    else:
        CapitalInvestmentstotable = ''
    # Production annual sources table
    productionannualsourceplot.reset_index(drop=True)
    productionannualsourceplot.reset_index(drop=True, inplace=True)
    productionannualsourceplot = productionannualsourceplot.rename_axis(None, axis=1)
    productionannualsourceplot = productionannualsourceplot.round(decimals=2)
    productionannualsourceplot.rename(columns={"": "YEAR"}, inplace=True)
    productionannualsourceplot1 = productionannualsourceplot.transpose()
    productionannualsourceplot1.columns = productionannualsourceplot1.iloc[0]
    productionannualsourceplot1.reset_index(inplace=True)
    productionannualsourceplot1 = productionannualsourceplot1.rename(columns = {'index':'Technology'})
    productionannualsourceplot1 = productionannualsourceplot1.drop(0)
    productionannualsourceplot1 = productionannualsourceplot1.rename_axis(None, axis=1)
    productionannualsourceplotdf1 =  productionannualsourceplot1.to_html(index=False, col_space= 100, justify='center')
    productionannualsourcetable = productionannualsourceplotdf1.replace('<tr>', '<tr align="center">')

    # Production annual sinks table
    productionannualsinkplot.reset_index(drop=True)
    productionannualsinkplot.reset_index(drop=True, inplace=True)
    productionannualsinkplot = productionannualsinkplot.rename_axis(None, axis=1)
    productionannualsinkplot = productionannualsinkplot.round(decimals=2)
    productionannualsinkplot.rename(columns={"": "YEAR"}, inplace=True)
    productionannualsinkplot1 = productionannualsinkplot.transpose()
    productionannualsinkplot1.columns = productionannualsinkplot1.iloc[0]
    productionannualsinkplot1.reset_index(inplace=True)
    productionannualsinkplot1 = productionannualsinkplot1.rename(columns = {'index':'Technology'})
    productionannualsinkplot1 = productionannualsinkplot1.drop(0)
    productionannualsinkplot1 = productionannualsinkplot1.rename_axis(None, axis=1)
    productionannualsinkplotdf1 =  productionannualsinkplot1.to_html(index=False, col_space= 100, justify='center')
    productionannualsinkplottable = productionannualsinkplotdf1.replace('<tr>', '<tr align="center">')

    #Total excess heat production

    productionannualsourcepieplot.reset_index(drop=True)
    productionannualsourcepieplot.reset_index(drop=True, inplace=True)
    productionannualsourcepieplot = productionannualsourcepieplot.rename_axis(None, axis=1)
    productionannualsourcepieplot = productionannualsourcepieplot.round(decimals=2)
    productionannualsourcepieplot.rename(columns={"Total Production": "Total production in kWh"}, inplace=True)
    productionannualsourcepieplot.rename(columns={"Sources": "Source"}, inplace=True)
    productionannualsourcepiedf1 =  productionannualsourcepieplot.to_html(index=False, col_space= 100, justify='center')
    productionannualsourcepietable = productionannualsourcepiedf1.replace('<tr>', '<tr align="center">')


    #Total excess heat consumption

    productionannualsinkpieplot.reset_index(drop=True)
    productionannualsinkpieplot.reset_index(drop=True, inplace=True)
    productionannualsinkpieplot = productionannualsinkpieplot.rename_axis(None, axis=1)
    productionannualsinkpieplot = productionannualsinkpieplot.round(decimals=2)
    productionannualsinkpieplot.rename(columns={"Total Production": "Total Consumption in kWh"}, inplace=True)
    productionannualsinkpieplot.rename(columns={"Sinks": "Sink"}, inplace=True)
    productionannualsinkpieplotdf1 =  productionannualsinkpieplot.to_html(index=False, col_space= 100, justify='center')
    productionannualsinkpieplottable = productionannualsinkpieplotdf1.replace('<tr>', '<tr align="center">')
    
#Reference System
    reference_assign_name = []
    reference_assign_streamid = []
    for x in reference_system_df['name']:
        for i in names:
                if str('sink'+ str(str(i))+ 'str') in x:
                    reference_assign_name.append(names[str(i)])
        for i in streamidlistd:
                    if(','.join(["str%d " % i ])) in str(str(x) + ' '):
                        reference_assign_streamid.append(','.join(["Stream%d" % i ]))
    reference_assign_name_2 = []

    for i in range(0, len(reference_assign_name)):
        reference_assign_name_2.append(str(str(reference_assign_name[i]) + ' ' + str(reference_assign_streamid[i])))
    reference_system_df['Sink Name'] = reference_assign_name_2
    reference_system_df = reference_system_df[['Sink Name', 'Cost (Euros)', 'Emissions (Kg CO2)']]

    reference_system_df.reset_index(drop=True)
    reference_system_df.reset_index(drop=True, inplace=True)
    reference_system_df = reference_system_df.rename_axis(None, axis=1)
    reference_system_df = reference_system_df.round(decimals=2)
    reference_system_df1 =  reference_system_df.to_html(index=False, col_space= 100, justify='center')
    reference_system_dftable = reference_system_df1.replace('<tr>', '<tr align="center">')

     #Savings
    Savings_df = pd.DataFrame()
    OperatingCostTableS = OperatingCostTable1

    TechlistCS = OperatingCostTableS['Technology']
    ValuelistCS = OperatingCostTableS['Operating costs (Euros)']

    for i in range(0,len(TechlistCS)):
        if 'Grid Specific'in TechlistCS[i]:
            del(TechlistCS[i])
            del(ValuelistCS[i])
    OperatingCostTableS['Technology'] = TechlistCS
    OperatingCostTableS['Operating costs (Euros)'] = ValuelistCS
    CostSavings = reference_system_df['Cost (Euros)'].sum() - OperatingCostTable1['Operating costs (Euros)'].sum()

    if CostSavings >=0:
        Savings_df['Cost Savings (Euros)'] = [CostSavings]
    else:
        Savings_df['Cost Increase (Euros)'] = [CostSavings * -1]

    AnnualTechnologyEmissiondfS = AnnualTechnologyEmissiondf

    TechlistCS = AnnualTechnologyEmissiondfS['Technology']
    ValuelistCS = AnnualTechnologyEmissiondfS['Emissions (kg CO2)']

    for i in range(0,len(TechlistCS)):
        if 'Grid Specific'in TechlistCS[i]:
            del(TechlistCS[i])
            del(ValuelistCS[i])
    AnnualTechnologyEmissiondfS['Technology'] = TechlistCS
    AnnualTechnologyEmissiondfS['Emissions (kg CO2)'] = ValuelistCS
    
    EmissionSavings = reference_system_df['Emissions (Kg CO2)'].sum() - AnnualTechnologyEmissiondf['Emissions (kg CO2)'].sum()

    if EmissionSavings >=0:
        Savings_df['Emission Savings (kg CO2)'] = [EmissionSavings]
    else:
        Savings_df['Emission Increase (kg CO2)'] = [EmissionSavings * -1]

    Savings_df.reset_index(drop=True)
    Savings_df.reset_index(drop=True, inplace=True)
    Savings_df = Savings_df.rename_axis(None, axis=1)
    Savings_df = Savings_df.round(decimals=2)
    Savings_df1 =  Savings_df.to_html(index=False, col_space= 100, justify='center')
    Savings_dftable = Savings_df1.replace('<tr>', '<tr align="center">')
        

    combinedaccnewcap = plotly.io.to_html(fig, full_html=False,include_plotlyjs=False)
    if "Grid Specific" in Assign8:
        gridaccnewcap = plotly.io.to_html(fig4, full_html=False,include_plotlyjs=False)
    else:
        gridaccnewcap = ''    
    if len(AccumulatedNewStorageCapacity) != 0:
        accsto = plotly.io.to_html(figsto, full_html=False,include_plotlyjs=False)
    else:
        accsto = ''
    
    emallcomb = plotly.io.to_html(figem, full_html=False,include_plotlyjs=False)
    if "Grid Specific" in Assign8em:
        emgridspec = plotly.io.to_html(figemgrid, full_html=False,include_plotlyjs=False)
    else:
        emgridspec = ''
    ciac = plotly.io.to_html(figCI, full_html=False,include_plotlyjs=False)
    if len(CapitalInvestmentsto) != 0:
        cisto = plotly.io.to_html(figCIS, full_html=False,include_plotlyjs=False)
    else:
        cisto = ''
    cioc = plotly.io.to_html(figOC, full_html=False,include_plotlyjs=False)
    pbtsor = plotly.io.to_html(figsPBTsource, full_html=False,include_plotlyjs=False) 
    pbtsi = plotly.io.to_html(figsPBTSink, full_html=False,include_plotlyjs=False) 
    pasou = plotly.io.to_html(figsPAsource, full_html=False,include_plotlyjs=False) 
    pasi = plotly.io.to_html(figsPAsink, full_html=False,include_plotlyjs=False) 
    piesou = plotly.io.to_html(figpiesource, full_html=False,include_plotlyjs=False) 
    piesi =  plotly.io.to_html(figpiesink, full_html=False,include_plotlyjs=False) 

    ### REPORT_RENDERING_CODE [BEGIN]

    script_dir = os.path.dirname(__file__)

    env = Environment(
        loader=FileSystemLoader(os.path.join(script_dir, "asset")),
        autoescape=False
    )

    template = env.get_template('index.template.html')
    template_content = template.render(ANCT_df=AccumulatedNewCapacitytable,PIESOU=piesou, ANCSOU=ancsou, ANCSI=ancsi, EMSO=emso, EMSI=emsi, CISO=ciso, CICI=cisi, OCSO=ocso, OCSI=ocsi, STOL=stol, STOCD=stocd, PBTGSO=pbtso, PBTGSI=pbtsin, PEISI=piesi, PAGSO=pagso, PAGSI=pagsi, PASOU=pasou, ANCAC=combinedaccnewcap,PASI=pasi, PBTSI=pbtsi, CIOC=cioc, PBTSOU=pbtsor, ACSTO=accsto,CISTO=cisto, EMALLCOMB=emallcomb, EMGRIDSPEC=emgridspec,CIAC=ciac, ANCGS=gridaccnewcap, ANST_df=AccumulatedNewStorageCapacitytable, AHTSO_df=productionannualsourcetable, AHTSI_df=productionannualsinkplottable, TOTSO_df=productionannualsourcepietable, TOTSI_df=productionannualsinkpieplottable, CISTO_df=CapitalInvestmentstotable, TOTEM_df=AnnualTechnologyEmissiondtable, CI_df=CapitalInvestmenttable, OC_df=OperatingCosttable, Ref_df = reference_system_dftable, Sav_df=Savings_dftable)

    
    return(template_content)
    
    