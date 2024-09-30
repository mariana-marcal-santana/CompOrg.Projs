import pandas as pd

df = pd.DataFrame()
for i in range(1,6):
    df = pd.concat((df, pd.read_csv(f"spark{i}.csv", delim_whitespace=True)))

df = df.reset_index()

df_avg = df.groupby('size').mean().reset_index()

df_avg["accesses"] = df_avg["size"]*100
df_avg["mean_access_time"] = df_avg["elapsed(s)"] / df_avg["accesses"]
df_avg["mean_access_time (ns)"] = df_avg["mean_access_time"].apply(
    lambda x: x * 10**9
)
df_avg["size (KiB)"] = df_avg["size"].apply(lambda x: x >> 10)
     
df_avg.sort_values("size")[
    ["size (KiB)", "elapsed(s)", "accesses", "mean_access_time (ns)"]
].head(6)

print(df_avg)