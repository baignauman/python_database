import pandas as pd
import csv
import json
import os
import mpld3
import matplotlib.pyplot as plt
path = os.path.dirname(os.path.abspath(__file__))


def csv_json(csv_filepath, json_filepath, fieldnames):
    jsonfile = open(json_filepath, 'w')
    with open(csv_filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames)
        out = json.dumps([row for row in reader])
        jsonfile.write(out)
    jsonfile.close()
    return out


if __name__ == "__main__":
    csv_filename = 'data.csv'
    json_filename = 'data.json'
    csv_filepath = os.path.join(path, csv_filename)
    json_filepath = os.path.join(path, json_filename)

    fieldnames = ("Date", "Price_Nauman", "Price_Naveed")
    out = csv_json(csv_filepath, json_filepath, fieldnames)
    pd_frame = pd.DataFrame(json.loads(out))
    # change index from sequential to Date
    pd_frame.set_index('Date', inplace=True)
    print(pd_frame)
    pd_frame1 = pd_frame.astype(float)  # convert all columns datatype to float
    print(pd_frame1.dtypes)

    # matplotlib figure object
    fig = plt.figure(figsize=(18, 8))

    # box plot
    plt.subplot(2, 1, 1)
    plt.boxplot(pd_frame1)
    ticks = range(1, len(pd_frame1.columns)+1)
    labels = list(pd_frame.columns)
    plt.xticks(ticks, labels)
    plt.savefig(os.path.join(path, 'box.png'))
    # plt.show()
    print("see Graph")

    # scatter plot
    dates = pd_frame1.index.to_series()  # index which is date create
    xx = [pd.to_datetime(xdata) for xdata in dates]
    yy = pd_frame1['Price_Naveed']
    plt.subplot(2, 1, 2)
    plt.scatter(xx, yy)
    plt.xlabel('Year')
    plt.ylabel("Price Naveed")
    plt.tight_layout()

    # plt.show()
    plt.savefig(os.path.join(path, 'scatter.png'))

    # figure to html code
    html_str = mpld3.fig_to_html(fig)  # matplotlib fig object as input
    with open(os.path.join(path, "templates", "fig.html"), "w") as Html_file:
        Html_file.write(html_str)
