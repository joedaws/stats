"""
Create visualizations of the personal statistics in this project
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import calmap

from stats.constants import DATA_DIR, IMAGE_DIR, POUNDS_LOST_PER_WEEK


def add_goal_weight(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trying to lose 2 lb per week means

    starting_weight - POUNDS_LOST_PER_WEEK * (number of weeks since start)
    """
    starting_weight = df["weight"].iloc[0]
    starting_date = df["recorded_at"].iloc[0]
    df["goal_weight"] = df["recorded_at"].apply(
        lambda x: starting_weight - POUNDS_LOST_PER_WEEK * (x - starting_date).days / 7
    )

    return df


def create_weight_plot():
    weight_data = pd.read_csv(os.path.abspath(os.path.join(DATA_DIR, "weight.csv")))
    weight_data["recorded_at"] = pd.to_datetime(weight_data["recorded_at"])
    weight_data = add_goal_weight(weight_data)
    fig, ax = plt.subplots()
    weight_data.plot(x="recorded_at", y="weight", ax=ax)
    weight_data.plot(x="recorded_at", y="goal_weight", ax=ax)

    plt.title("My Weight")
    plt.plot()
    plt.savefig(os.path.abspath(os.path.join(IMAGE_DIR, "weight.png")))


def create_training_days_plot():
    activity_data = pd.read_csv(
        os.path.abspath(os.path.join(DATA_DIR, "training/heart_rate.csv"))
    )
    activity_data["recorded_at"] = pd.to_datetime(activity_data["recorded_at"])
    dates = activity_data["recorded_at"]
    activities = activity_data["z3"].apply(lambda x: int(x[3:5]))
    activities.index = dates
    fig, ax = plt.subplots()

    calmap.calendarplot(
        activities,
        monthticks=3,
        daylabels="MTWTFSS",
        dayticks=[0, 2, 4, 6],
        cmap="YlGn",
        fillcolor="grey",
        linewidth=0,
    )

    plt.title("Heart Rate Z3")
    plt.plot()
    plt.savefig(os.path.abspath(os.path.join(IMAGE_DIR, "training.png")))


if __name__ == "__main__":
    create_weight_plot()
    create_training_days_plot()
