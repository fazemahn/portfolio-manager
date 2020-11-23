from Monte import Monte
import datetime as dt

"""
Example to show how a Monte object can be created with user inputs and made 
to output the plots to an html and json file.
"""

# Placeholder example to show Monte object method implementation
mon = Monte('AMD', 100, 30, start=dt.datetime(2018,1,1), end=dt.datetime.now(), data_source='yahoo')
mon.create_DataFrame()
mon.simulate()

# creates html file of the Monte object's figure
html_str1 = mon.plot_history()
html_file1 = open("plots1.html","w") # writes string to html file
html_file1.write(html_str1)
html_file1.close()

html_str2 = mon.plot_pdf()
html_file2 = open("plots2.html","w") # writes string to html file
html_file2.write(html_str2)
html_file2.close()

html_str3 = mon.plot_single()
html_file3 = open("plots3.html","w") # writes string to html file
html_file3.write(html_str3)
html_file3.close()

html_str4 = mon.plot_multi()
html_file4 = open("plots4.html","w") # writes string to html file
html_file4.write(html_str4)
html_file4.close()

html_str = mon.get_json(html_str1, html_str2, html_str3, html_str4)
html_file = open("plots.html","w") # writes string to html file
html_file.write(html_str)
html_file.close()

# creates json file of the Monte object's figure
plot_json = mon.get_json(html_str, html_str2, html_str3, html_str4)
json_file = open("plots.json","w")
json_file.write(plot_json)
json_file.close()
