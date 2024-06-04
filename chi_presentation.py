import pandas

labels = ["xallarapPath","pathParaxall","parallaxPath"]
data = pandas.read_csv("sim30/chi2_with_paraxall.csv",index_col=0)
data = data.drop(axis=1, labels=labels )
presentation_data = data[data["better"] == "xallarap"]

label = ["better"]
presentation_data = presentation_data.drop(axis=1, labels=label)

print(presentation_data)
presentation_data.to_csv(path_or_buf="Presentation/tabelka.csv")



