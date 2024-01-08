#! /usr/bin/env python3

# libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("darkgrid")

SAVE = False  # True to save each figure


# Read datasets
df_show = pd.read_csv("show.csv")
df_noshow = pd.read_csv("noshow.csv")
# calculate ration of no shows
num_shows = df_show.shape[0]
num_noshows = df_noshow.shape[0]
num_total = num_shows + num_noshows
print("Percent of no shows:", num_noshows / num_shows * 100, "%")
print("Number of shows:", num_shows)
print("Number of no shows:", num_noshows)


# Explore appointment/schedule times
print("Time ranges")
# new columns
for df in [df_show, df_noshow]:
    df["scheduled_day"] = pd.to_datetime(
        df["scheduled_day"]
    )  # str -> timestamp
    print(df["scheduled_day"].describe())
    df["appointment_day"] = pd.to_datetime(
        df["appointment_day"]
    )  # str -> timestamp
    print(df["appointment_day"].describe())
    # calculate days scheduled ahead
    df["days_ahead"] = df["appointment_day"].apply(lambda x: x.dayofyear) - df[
        "scheduled_day"
    ].apply(lambda x: x.dayofyear)
    df["days_ahead"] = df["appointment_day"].apply(lambda x: x.date) - df[
        "scheduled_day"
    ].apply(lambda x: x.date)
    df["days_ahead"] = df["days_ahead"].apply(lambda x: x.days)
    df.drop(
        df.loc[df["days_ahead"] < 0].index, inplace=True
    )  # remove entries with schedule date after appointment
    print(df["days_ahead"].describe())
    bin_names = [
        "Same day",
        "Short wait",
        "Moderate wait",
        "Long wait",
        "Extended wait",
    ]
    # bin days_ahead
    bins = [-1, 0, 4, 11, 23, 180]
    df["day_bins"] = pd.cut(df["days_ahead"], bins, labels=bin_names)
    df["scheduled_weekday"] = df["scheduled_day"].apply(lambda x: x.dayofweek)
    df["appointment_weekday"] = df["appointment_day"].apply(
        lambda x: x.dayofweek
    )
    df["scheduled_jday"] = df["scheduled_day"].apply(lambda x: x.dayofyear)
    df["appointment_jday"] = df["appointment_day"].apply(lambda x: x.dayofyear)
    df["scheduled_time"] = df["scheduled_day"].apply(lambda x: x.time)
    df["hour_of_day"] = df["scheduled_time"].apply(
        lambda x: float(x.hour) + float(x.minute) / 60
    )
    df["scheduled_day"] = df["scheduled_day"].apply(lambda x: x.date)
    df["appointment_day"] = df["appointment_day"].apply(lambda x: x.date)

# plot times
fig, ax = plt.subplots(2, 3, figsize=(10, 7))
sns.histplot(
    df_show["days_ahead"],
    ax=ax[0, 0],
    stat="percent",
    binwidth=5,
    color="r",
    alpha=1,
)
sns.histplot(
    df_noshow["days_ahead"],
    ax=ax[0, 0],
    stat="percent",
    binwidth=5,
    color="b",
    fill=False,
)
ax[0, 0].set_xlim(0, 180)
sns.histplot(
    df_show["hour_of_day"],
    ax=ax[1, 0],
    stat="percent",
    binwidth=1,
    binrange=[0, 24],
    color="r",
    alpha=1,
)
sns.histplot(
    df_noshow["hour_of_day"],
    ax=ax[1, 0],
    stat="percent",
    binwidth=1,
    binrange=[0, 24],
    color="b",
    fill=False,
)
ax[1, 0].set_xlim(0, 24)
sns.histplot(
    df_show["scheduled_weekday"],
    ax=ax[0, 1],
    stat="percent",
    binwidth=1,
    binrange=[0, 7],
    color="r",
    alpha=1,
)
sns.histplot(
    df_noshow["scheduled_weekday"],
    ax=ax[0, 1],
    stat="percent",
    binwidth=1,
    binrange=[0, 7],
    color="b",
    fill=False,
)
ax[0, 1].set_xlim(0, 7)
sns.histplot(
    df_show["appointment_weekday"],
    ax=ax[1, 1],
    stat="percent",
    binwidth=1,
    binrange=[0, 7],
    color="r",
    alpha=1,
)
sns.histplot(
    df_noshow["appointment_weekday"],
    ax=ax[1, 1],
    stat="percent",
    binwidth=1,
    binrange=[0, 7],
    color="b",
    fill=False,
)
ax[1, 1].set_xlim(0, 7)
sns.histplot(
    df_show["scheduled_jday"],
    ax=ax[0, 2],
    stat="percent",
    binwidth=5,
    color="r",
    alpha=1,
)
sns.histplot(
    df_noshow["scheduled_jday"],
    ax=ax[0, 2],
    stat="percent",
    binwidth=5,
    color="b",
    fill=False,
)
sns.histplot(
    df_show["appointment_jday"],
    ax=ax[1, 2],
    stat="percent",
    binwidth=5,
    color="r",
    alpha=1,
    label="Shows",
)
sns.histplot(
    df_noshow["appointment_jday"],
    ax=ax[1, 2],
    stat="percent",
    binwidth=5,
    color="b",
    fill=False,
    label="No Shows",
)
plt.legend()
plt.tight_layout()
if SAVE:
    plt.savefig("figs/schd-appt_times.png")  # save into figs directory
plt.show()
# plot day_bins
sns.histplot(
    df_show["day_bins"],
    stat="percent",
    binwidth=2,
    color="r",
    alpha=1,
    label="Shows",
)
sns.histplot(
    df_noshow["day_bins"],
    stat="percent",
    binwidth=2,
    color="b",
    fill=False,
    label="No Shows",
)
# plt.xlim(0,180)
plt.legend()
if SAVE:
    plt.savefig("figs/day_bins.png")  # save into figs directory
plt.show()


# Explore Patient Attributes
print("attributes")
pos = df_show.columns[7:13]
# make new df from proportion of True values
df_attr = pd.DataFrame()
df_tmp = df_show[pos].apply(pd.value_counts) / num_shows
df_attr["show"] = df_tmp.iloc[[1]].T
# add column of Trues for no shows
df_tmp = df_noshow[pos].apply(pd.value_counts) / num_noshows
df_attr["noshow"] = df_tmp.iloc[[1]].T
print(df_attr)
# plot
ax = df_attr.plot.bar(rot=15, color={"show": "r", "noshow": "b"})
ax.set_ylabel("Proportion")
if SAVE:
    plt.savefig("figs/patient_attr.png")  # save into figs directory
plt.show()


# Explore Ages
print("ages")
for df in [df_show, df_noshow]:
    print(df["age"].describe())
    df.drop(
        df.loc[df["age"] < 0].index, inplace=True
    )  # remove entries with schedule date after appointment
    print(df["days_ahead"].describe())
    # binned ages
    bin_names = [
        "Baby",
        "Adolecent",
        "Young Adult",
        "Middle-aged Adult",
        "Elderly Adult",
    ]
    bins = [-1, 0, 17, 36, 54, 115]
    df["age_bins"] = pd.cut(df["age"], bins, labels=bin_names)
# plot ages
fig, ax = plt.subplots(2, 1, figsize=(7, 8))
sns.histplot(
    df_show["age"],
    ax=ax[0],
    stat="percent",
    binwidth=5,
    color="r",
    alpha=1,
    label="show",
)
sns.histplot(
    df_noshow["age"],
    ax=ax[0],
    stat="percent",
    binwidth=5,
    color="b",
    fill=False,
    label="no show",
)
ax[0].legend()
sns.histplot(
    df_show["age_bins"],
    ax=ax[1],
    stat="percent",
    binwidth=2,
    color="r",
    alpha=1,
    label="show",
)
sns.histplot(
    df_noshow["age_bins"],
    ax=ax[1],
    stat="percent",
    binwidth=2,
    color="b",
    fill=False,
    label="no show",
)
if SAVE:
    plt.savefig("figs/patient_ages.png")  # save into figs directory
plt.show()


# Neighbourhood
print("neighbourhoods")
# make new df from value counts
df_neig = pd.DataFrame()
df_neig["show"] = df_show["neighbourhood"].value_counts()
# add column for no shows
df_neig["noshow"] = df_noshow["neighbourhood"].value_counts()
# new column of No Show ratio
df_neig["ratio"] = df_neig["noshow"] / (df_neig["show"] + df_neig["noshow"])
print("Ratios")
print(df_neig["ratio"].describe())
std = df_neig["ratio"].std()
mean = df_neig["ratio"].mean()
df_hr_neig = df_neig[df_neig.ratio > mean + std]
print(df_hr_neig.to_string())
# plot
fig, ax = plt.subplots(figsize=(14, 5))
df_neig["ratio"].plot.bar(rot=15, color="purple")
ax.set_xticklabels(ax.get_xticklabels(), rotation=55, ha="right")
ax.set_ylabel("No Show Ratio")
plt.tight_layout()
if SAVE:
    plt.savefig("figs/neighborhoods.png")  # save into figs directory
plt.show()

fig, ax = plt.subplots(figsize=(14, 5))
input(df_hr_neig)
df_hr_neig["ratio"].plot.bar(rot=15, color="purple")
ax.set_xticklabels(ax.get_xticklabels(), rotation=55, ha="right")
ax.set_ylabel("No Show Ratio")
plt.tight_layout()
if SAVE:
    plt.savefig(
        "figs/high_ratio_neighborhoods.png"
    )  # save into figs directory
plt.show()
